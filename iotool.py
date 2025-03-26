import json


with open('error.json') as file:
    errors = json.load(file)


def error(code: str, errors_dict=None):
    if errors_dict is None:
        errors_dict = errors
    print(f'{errors_dict[code]}({code})')
    input()
    exit()


def print_list(lst: list):
    for v in lst:
        print(v)


if __name__ == '__main__':
    pass
