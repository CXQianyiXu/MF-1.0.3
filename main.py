# version=1.0.3
# coding=utf-8

"""
Something new:
    Set up some modules.
"""


from solving import *


equations, unknowns, sys_equ, equ = prepare()

while equ:
    equ = input_equation(equ, equations, unknowns, sys_equ)

unknowns = check_number_equations_unknowns(equations, unknowns)

# print(equations)
# print(unknowns)
# print(sys_equ)

sys_equ = unite_terms_operators(sys_equ)

# print(sys_equ)

sys_equ = move_terms(sys_equ)

# print(sys_equ)

sys_equ = unite_terms(sys_equ, unknowns)

# print(sys_equ)

sys_equ = gaussian_elimination(sys_equ, unknowns)

# print(sys_equ)

sys_equ = solve_equations(sys_equ, unknowns)

print_list(sys_equ)
input()
