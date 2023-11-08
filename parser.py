def parse_assembly_instructions(asm_instructions):
    parsed_assembly_instructions = []
    for line_counter, line in enumerate(asm_instructions):
        if len(line) == 1 and line[0] == "\n":
            continue
        else:
            temp_line = line.replace(",", "")
            parsed_assembly_instructions.append(temp_line.strip())

    return parsed_assembly_instructions
