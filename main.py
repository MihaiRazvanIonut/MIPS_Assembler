# MIPS Assembler made for AMD Autumn Practice 2023
# Project made by Mihai Razvan-Ionut
# Assembler follows the MIPS Standard for notations described in "David Harris, Sarah Harris - Digital Design and Co"

# How to use: - Copy and paste desired MIPS Assembly code into "mips_assembly.txt"
#             - Run "main.py" script
#             - Wait until the script is done
#             - The machine code is now found in "mips_machine_code.txt"

# Implemented instructions:
#                          lw, sw, beq, addi, add, sub, and, or, slt, xor, jr, j, jal

import assembler
import parser
import syntax_checker

asm_input_file = open("mips_assembly.txt")
asm_instructions = asm_input_file.readlines()
asm_input_file.close()
asm_parsed_instructions = parser.parse_assembly_instructions(asm_instructions)
asm_parsed_and_syntax_checked_instructions = syntax_checker.syntax_checking(asm_parsed_instructions)
machine_code_hex_instructions_list = assembler.assemble_parsed_instructions(asm_parsed_instructions)
machine_code_output_file = open("mips_machine_code.txt", "w")
for hex_instruction in machine_code_hex_instructions_list:
    machine_code_output_file.write(hex_instruction + '\n')
