import operations
from registers import registers


def syntax_checking(instructions):
    flag_text_notation = False
    flag_data_notation = False

    standard_parsed_asm_code = []
    global_data_table = []
    for instruction in instructions:
        instruction_elements = instruction.split()
        for element in instruction_elements:
            if element == "":
                instruction_elements.remove(element)
        if len(instruction_elements) == 1 and instruction_elements[0][len(instruction_elements[0]) - 1] == ":":
            global_data_table.append(instruction_elements[0].replace(":", ""))
        standard_parsed_asm_code.append(instruction_elements)

    for line in standard_parsed_asm_code:
        if line[0] == ".text":
            flag_text_notation = True

        if line[0] == ".data":
            flag_data_notation = True
        if len(line) > 1:
            flag_recognised_operation = False
            if line[0] in operations.r_type_operations.keys():
                if line[0] == "jr":
                    if len(line) != 2:
                        raise Exception("Syntax Error 2!: The following:", line,
                                        "is an r-type operation that should have 1 register as argument")
                    if line[1] != "$ra" and line[1] != "$31":
                        raise Exception("Error!: You can only use $ra or $31 as argument for jr instruction")
                else:
                    if len(line) != 4:
                        raise Exception("Syntax Error 2!: The following:", line,
                                        "is an r-type operation that should have 3 registers as arguments")
                    line_counter = 1
                    if line[1] == "$0":
                        raise Exception("Error!: You cannot modify register $0")
                    while line_counter < 4:
                        if line[line_counter] not in registers.keys():
                            raise Exception("Syntax Error 3!: Register", line[line_counter],
                                            "is not a recognised register")
                        line_counter += 1
                flag_recognised_operation = True
            if line[0] in operations.i_type_operations.keys():
                flag_recognised_operation = True
            if line[0] in operations.j_type_operations.keys():
                if len(line) != 2:
                    raise Exception("Syntax Error 2!: The following:", line,
                                    "is an j-type operation that should have one label as argument")
                if line[1] not in global_data_table:
                    raise Exception("Syntax Error 4!: This is an invalid label", line[1],
                                    "is not found anywhere in the code")
                flag_recognised_operation = True
            if not flag_recognised_operation:
                raise Exception("Syntax Error 0!: The following operation is not recognised", line[0])

    if not flag_text_notation:
        raise Exception("Syntax Error 1!: Code does not contain \".text\" notation to indicate where the code starts")

    if not flag_data_notation:
        print("Warning!: Code does not have \".data\" notation to indicate global data")
