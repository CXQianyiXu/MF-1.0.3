from string import ascii_letters, digits


alphabet = list(ascii_letters)
numbers = list(digits)
primary = ['+', '-']
operators = primary + ['=']
chars = numbers + alphabet + ['/'] + operators + [' ']

if __name__ == '__main__':
    pass
