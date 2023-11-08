from registers import registers
import operations

global_symbol_table = {}


def assemble_parsed_instructions(asm_parsed_instructions):
    line_components_list = []
    machine_code_output = []
    for line in asm_parsed_instructions:
        line_components = line.split()
        for component in line_components:
            if component == "":
                line_components.remove(component)
        line_components_list.append(line_components)

    # FIRST STEP: On the first pass, the assembler assigns
    # instruction addresses and finds all the symbols, such as labels and global
    # variable names.

    for line_components_counter, line_components_item in enumerate(line_components_list):
        if '.data' in line_components_item:
            global_data_processing(line_components_list, line_components_counter)
            break

    line_components_list.remove(line_components_list[0])
    label_processing(line_components_list)

    # SECOND STEP: On the second pass through the code, the assembler produces the
    # machine language code. Addresses for the global variables and labels are
    # taken from the symbol table.
    line_number = 0
    for line_components_item in line_components_list:
        machine_code_operation = str
        if line_components_item[0] in operations.r_type_operations.keys():
            machine_code_operation = r_type_operations_processing(line_components_item)
        if line_components_item[0] in operations.i_type_operations.keys():
            machine_code_operation = i_type_operations_processing(line_components_item, line_number)
        if line_components_item[0] in operations.j_type_operations.keys():
            machine_code_operation = j_type_operations_processing(line_components_item)
        machine_code_output.append(convert_bin_string_to_hex_string(machine_code_operation))
        line_number += 1
    return machine_code_output


def global_data_processing(line_components_list, global_data_index):
    global_symbol_address = 0x8000
    line_components_list.remove(line_components_list[global_data_index])
    while global_data_index < len(line_components_list) and line_components_list[global_data_index][0] != ".text":
        global_key = line_components_list[global_data_index][0].replace(":", "")
        global_symbol_table[global_key] = global_symbol_address
        global_symbol_address += 4
        line_components_list.remove(line_components_list[global_data_index])


def label_processing(line_components_list):
    label_address = 0
    for line_components_item in line_components_list:
        if len(line_components_item) == 1 and line_components_item[0][len(line_components_item[0]) - 1] == ':':
            global_symbol_table[line_components_item[0].replace(":", "")] = label_address
            label_address -= 1
        label_address += 1

    for line_components_item in line_components_list:
        if len(line_components_item) == 1 and line_components_item[0][len(line_components_item[0]) - 1] == ':':
            line_components_list.remove(line_components_item)


def r_type_operations_processing(asm_operation):
    machine_code_operation = "000000"
    if asm_operation[0] == "jr":
        machine_code_operation += registers["$ra"]
        machine_code_operation += "000000000000000"
        machine_code_operation += operations.r_type_operations[asm_operation[0]]
    else:
        machine_code_operation += registers[asm_operation[2]]
        machine_code_operation += registers[asm_operation[3]]
        machine_code_operation += registers[asm_operation[1]]
        if asm_operation[0] == "sll":
            pass
        else:
            machine_code_operation += "00000"
        machine_code_operation += operations.r_type_operations[asm_operation[0]]
    return machine_code_operation


def i_type_operations_processing(asm_operation, line_number):
    machine_code_operation = operations.i_type_operations[asm_operation[0]]
    if asm_operation[0] == "lw" or asm_operation[0] == "sw":
        if asm_operation[2][len(asm_operation[2])-1] == ")":
            open_par_index = asm_operation[2].index("(")
            rt_regis = ""
            while asm_operation[2][open_par_index+1] != ")":
                open_par_index += 1
                rt_regis += asm_operation[2][open_par_index]
            machine_code_operation += registers[rt_regis]
            machine_code_operation += registers[asm_operation[1]]
            num_index = 0
            num_str = ""
            while asm_operation[2][num_index] != "(":
                num_str += asm_operation[2][num_index]
                num_index += 1

            imm_bin = sign_extend_to_16bits(convert_integer_to_binary_complement_of_2_string(convert_str_to_int(num_str)))
            machine_code_operation += imm_bin
        else:
            machine_code_operation += registers["$gp"]
            machine_code_operation += registers[asm_operation[1]]
            imm_bin = str(bin(global_symbol_table[asm_operation[2]])).replace("0b", "")
            machine_code_operation += ((16 - len(imm_bin)) * "0") + imm_bin
    else:
        if asm_operation[0] == 'beq':
            machine_code_operation += registers[asm_operation[1]]
            machine_code_operation += registers[asm_operation[2]]
            beq_imm = global_symbol_table[asm_operation[3]] - line_number - 1
            if beq_imm < 0:
                imm_bin = sign_extend_to_16bits(convert_integer_to_binary_complement_of_2_string(beq_imm))
            else:
                imm_bin = str(bin(beq_imm)).replace("0b", "")
                imm_bin = (16 - len(imm_bin)) * "0" + imm_bin
            machine_code_operation += imm_bin
        else:
            machine_code_operation += registers[asm_operation[2]]
            machine_code_operation += registers[asm_operation[1]]
            imm_bin = convert_integer_to_binary_complement_of_2_string(convert_str_to_int(asm_operation[3]))
            imm_16bit = sign_extend_to_16bits(imm_bin)
            machine_code_operation += imm_16bit
    return machine_code_operation


def j_type_operations_processing(asm_operation):
    machine_code_operation = operations.j_type_operations[asm_operation[0]]
    label_address = str(bin(global_symbol_table[asm_operation[1]])).replace("0b", "")
    front_zero = (26 - len(label_address)) * "0"
    machine_code_operation += front_zero + label_address
    return machine_code_operation


def convert_bin_string_to_hex_string(bin_str):
    hex_str = str(hex(int(bin(int(bin_str, 2)), 2))).replace("0x", "")
    if len(hex_str) < 8:
        front_zero = (8 - len(hex_str)) * "0"
        hex_str = front_zero + hex_str
    return hex_str


def convert_integer_to_binary_complement_of_2_string(integer):
    integer_bits = integer.bit_length() + 1
    return f"{integer & ((1 << integer_bits) - 1):0{integer_bits}b}"


def sign_extend_to_16bits(bin_str):
    bin_str_16bit = (16 - len(bin_str)) * bin_str[0]
    return bin_str_16bit + bin_str


def convert_str_to_int(string):
    if string[0] == "-":
        unsigned_string_integer = string.replace("-", "")
        is_signed = True
    else:
        unsigned_string_integer = string
        is_signed = False
    integer = int(unsigned_string_integer)
    if is_signed:
        integer = -integer

    return integer
