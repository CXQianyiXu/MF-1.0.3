from iotool import *
from math_tool import *
from pkg_resources import resource_filename
from pretool import *


def put_spaces(equation: str, sep=None):
    if sep is None:
        sep = operators
    equation = equation.split(' ')
    text = ''
    for string in equation:
        text += string
    equation = text
    is_operator = True
    i = 0
    while i < len(equation):
        if not equation[i] in sep:
            is_operator = False
        elif not is_operator:
            is_operator = True
            equation = f'{equation[:i]} {equation[i]} {equation[i + 1:]}'
            i += 2
        i += 1
    return equation


def prepare():
    with open(resource_filename(__name__, 'prepare.txt')) as f:
        print(f.read())
    return [], [], [], put_spaces(input())


def check_string(equation: str):
    if equation.count('=') != 1:
        error('E0000')
    unknown_list = []
    is_unk = False
    for char in equation:
        if char not in chars:
            error('E0002')
        if (char != ' ') and is_unk:
            error('E0001')
        if char not in alphabet:
            is_unk = False
        else:
            unknown_list.append(char)
            is_unk = True
    if not unknown_list:
        error('E0003')
    return unknown_list


def check_strings_between_spaces(equation: str):
    equation_list = equation.split(' ')
    if not equation_list[-1]:
        error('E0004')
    for terms_or_operators in equation_list:
        if terms_or_operators.count('/') > 1:
            error('E0005')
    return equation_list


def check_char_beside_division(char: str, string: str):
    if char == '/' and (string.index('/') + 1 == len(string) or string[string.index('/') + 1] not in numbers[1:]
                        or not string.index('/') or string[string.index('/') - 1] not in numbers):
        error('E0007')


def check_terms(string_term: str):
    for char in string_term:
        error('E0006') if char == '=' else check_char_beside_division(
            char, string_term)


def check_first_terms(string_term: str):
    for char in string_term:
        if char not in primary:
            break
    else:
        error('E0006')
    check_terms(string_term)


def check_signs(string_sign: str):
    error('E0008') if string_sign not in operators else None


def check_equation(equation_list: list):
    is_first_term = True
    is_sign = False
    for terms_or_operators in equation_list:
        if is_sign:
            check_signs(terms_or_operators)
            if terms_or_operators == '=':
                is_first_term = True
            is_sign = False
        else:
            if is_first_term:
                check_first_terms(terms_or_operators)
                is_first_term = False
            else:
                check_terms(terms_or_operators)
            is_sign = True


def append_new(new_equation: str, new_unknowns: list, new_equ_list: list,
               equations_list: list, unknowns_list: list, sys_equ_list: list):
    equations_list.append(new_equation)
    for unk in new_unknowns:
        unknowns_list.append(unk)
    sys_equ_list.append(new_equ_list)


def input_equation(equation: str, equations_list: list, unknowns_list: list, sys_equ_list: list):
    unknown = check_string(equation)
    equation_list = check_strings_between_spaces(equation)
    check_equation(equation_list)
    append_new(equation, unknown, equation_list,
               equations_list, unknowns_list, sys_equ_list)
    return put_spaces(input())


def check_number_equations_unknowns(equations_list: list, unknowns_list: list):
    unknowns_list = sorted(list(set(unknowns_list)),
                           key=lambda letter: alphabet.index(letter))
    if len(equations_list) != len(unknowns_list):
        error('E0101')
    return unknowns_list


def unite_terms_operators(sys_equ_list: list):
    equation_list = []
    for equation in sys_equ_list:
        terms_or_operators_list = []
        string_term = ''
        for string in equation:
            if string in operators:
                if string == '-':
                    string_term = string
                if string == '=':
                    terms_or_operators_list.append(string)
            else:
                for i in range(len(string)):
                    if string[i] not in primary:
                        string_term += string[i:]
                        break
                    elif string[i] == '-':
                        string_term = '' if string_term else '-'
                terms_or_operators_list.append(string_term)
                string_term = ''
        equation_list.append(terms_or_operators_list)
    return equation_list.copy()


def move_terms(sys_equ_list: list):
    equation_list = []
    for equation in sys_equ_list:
        will_move_term = [[], []]
        after_equ = False
        for string in equation:
            if string == '=':
                after_equ = True
            else:
                t_i_a = string[-1] in alphabet
                if t_i_a if after_equ else (not t_i_a):
                    will_move_term[0 if after_equ else 1].append(string)
        after_equ = False
        for side in will_move_term:
            for string in side:
                for i in range(len(equation)):
                    if equation[i] == string and int(i > equation.index('=')) + int(after_equ) == 1:
                        equation.pop(i)
                        break
                equation.insert(int(after_equ) * len(equation),
                                string[1:] if string[0] == '-' else '-' + string)
            after_equ = True
        equation_list.append(equation)
    return equation_list.copy()


def unite_terms(sys_equ_list: list, unknowns_list: list):
    equation_list = []
    for equation in sys_equ_list:
        ind = equation.index('=')
        equation_left = equation[:ind]
        equation_right = equation[ind + 1:]
        will_unite_coefficient = []
        will_unite_unknown = []
        for string in equation_left:
            if string[-1] not in will_unite_unknown:
                will_unite_unknown.append(string[-1])
                will_unite_coefficient.append(
                    [string[:-1] + ('' if string[:-1] and string[:-1] != '-' else '1')])
            else:
                will_unite_coefficient[will_unite_unknown.index(string[-1])].append(
                    string[:-1] + ('' if string[:-1] and string[:-1] != '-' else '1'))
        for i in range(len(will_unite_coefficient)):
            will_unite_coefficient[i] = num_list(will_unite_coefficient[i])
        equation_left = list(zip(will_unite_coefficient, will_unite_unknown))
        for unk in unknowns_list:
            if unk not in will_unite_unknown:
                equation_left.append(('0', unk))
        equation_left = sorted(
            equation_left, key=lambda item: unknowns_list.index(item[1]))
        for i in range(len(equation_left)):
            equation_left[i] = equation_left[i][0]
        equation_right = num_list(equation_right) if equation_right else '0'
        equation_list.append([equation_left, equation_right])
    return equation_list.copy()


def equality_property(equation: list, multiplier: str):
    equation_list = [[]]
    for i in range(len(equation[0])):
        equation_list[0].append(multiple(equation[0][i], multiplier))
    equation_list.append(multiple(equation[1], multiplier))
    return equation_list


def plus_equation(equation1: list, equation2: list):
    equation = [[]]
    for i in range(len(equation1[0])):
        equation[0].append(num_list([equation1[0][i], equation2[0][i]]))
    equation.append(num_list([equation1[1], equation2[1]]))
    return equation


def gaussian_elimination(sys_equ_list: list, unknowns_list: list):
    for i in range(len(unknowns_list) - 1):
        for j in range(i, len(unknowns_list)):
            for k in range(i, len(unknowns_list)):
                if sys_equ_list[k][0][j] != '0':
                    break
            else:
                error('E0102')
        for j in range(i, len(unknowns_list)):
            if sys_equ_list[j][0][i] != '0':
                sys_equ_list.insert(i, sys_equ_list.pop(j))
                break
        for j in range(i + 1, len(unknowns_list)):
            sys_equ_list[j] = plus_equation(sys_equ_list[j], equality_property(
                sys_equ_list[i], coefficient_elimination(sys_equ_list[i][0][i], sys_equ_list[j][0][i])))
    return sys_equ_list


def solve_equations(sys_equ_list: list, unknowns_list: list):
    equation_list = []
    for i in range(len(unknowns_list)):
        for j in range(i):
            sys_equ_list[-i - 1][1] = primary_operation(sys_equ_list[-i - 1][1],
                                                        multiple(
                                                            sys_equ_list[-i - 1][0].pop(), equation_list[-j - 1]),
                                                        False)
        error('E0102') if sys_equ_list[-i - 1][0][-1] == '0' \
            else equation_list.insert(0, divided(sys_equ_list[-i - 1][0][-1], sys_equ_list[-i - 1][1]))
    for i in range(len(equation_list)):
        equation_list[i] = unknowns_list[i] + ' = ' + equation_list[i]
    return equation_list.copy()
