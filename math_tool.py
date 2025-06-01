def coefficient_elimination(num1: str, num2: str):
    num = divided(num1, num2)
    if num == '0':
        return '0'
    if num[0] == '-':
        return num[1:]
    return f'-{num}'


def divided(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num1.reverse()
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction(f'{int(num1[0]) * int(num2[0])}/{int(num1[1]) * int(num2[1])}')
    return num


def factorization(num: int):
    if num == 1:
        return []
    if num == 0:
        return [0]
    if num == -1:
        return [-1]
    factors = []
    primes = []
    if num < 0:
        factors = [-1]
        num *= -1
    for i in range(2, num + 1):
        for j in range(2, int(i ** 0.5) + 1):
            if i / j % 1 == 0:
                break
        else:
            primes.append(i)
    while num not in primes:
        for prime in primes:
            if num / prime % 1 == 0:
                num = int(num / prime)
                factors.append(prime)
                break
    factors.append(num)
    return factors


def multiple(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction(f'{int(num1[0]) * int(num2[0])}/{int(num1[1]) * int(num2[1])}')
    return num


def num_list(nums: list):
    plus_list = nums
    while len(plus_list) > 1:
        plus_list.insert(0, primary_operation(plus_list.pop(0), plus_list.pop(0)))
    if '/' not in plus_list[0]:
        plus_list[0] += '/1'
    return reduction(plus_list[0])


def primary_operation(num1: str, num2: str, plus=True):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = 1 if plus else -1
    return reduction(f'{int(num1[0]) * int(num2[1]) + int(num1[1]) * int(num2[0]) * num}/{int(num1[1]) * int(num2[1])}')


def reduction(fraction: str):
    fraction = list(map(int, fraction.split('/')))
    if fraction[0] == 0:
        return '0'
    if fraction[1] == 0:
        raise ZeroDivisionError('division by zero')
    plus_or_minus = int(abs(fraction[0]) * abs(fraction[1]) / fraction[0] / fraction[1])
    fraction[0] = abs(fraction[0])
    fraction[1] = abs(fraction[1])
    numerator = factorization(fraction[0])
    denominator = factorization(fraction[1])
    will_move_factor = []
    for factor_numerator in numerator:
        for factor_denominator in denominator:
            if factor_numerator == factor_denominator:
                will_move_factor.append(factor_numerator)
                denominator.remove(factor_denominator)
                break
    for factor in will_move_factor:
        numerator.remove(factor)
    if len(numerator):
        while len(numerator) > 1:
            numerator.insert(0, numerator.pop(0) * numerator.pop(0))
        numerator = numerator[0]
    else:
        numerator = 1
    if len(denominator):
        while len(denominator) > 1:
            denominator.insert(0, denominator.pop(0) * denominator.pop(0))
        denominator = denominator[0]
    else:
        denominator = 1
    if denominator == 1:
        return str(numerator * plus_or_minus)
    return str(numerator * plus_or_minus) + '/' + str(denominator)


if __name__ == '__main__':
    pass
