
file_to_compile = input("Enter the file to compile: ")
file_output_name = input("Output file: ")


mode = 'default'
mode_value = 0


class Modes:
    """Class containing all possible compile mods"""
    def __init__(self):
        self.load = 'load'
        self.default = 'default'
        self.printing = 'printing'
        self.defining = 'defining'


modes = Modes()

def tokenize(code):
    """turns a string into a list of tokens"""
    split_chars = ['(', ')', '{', '}', '[', ']', ',', ';', '.', '+', '-', '*', '/', ' ', "'", '"', '\n']
    list_append_value = ''
    return_list = []
    notokenchars = ['', ' ']
    for char in code:
        if char in split_chars:
            if list_append_value not in notokenchars:
                return_list.append(list_append_value)
            list_append_value = ''
            if char not in notokenchars:
                return_list.append(char)
            continue
        if char not in notokenchars:
            list_append_value += char

    return return_list


def deal_with_code(code):
    global mode, mode_value
    with open(file_output_name, 'w') as out_file:
        for token in tokenize(code):
            print(token)
            if mode == 'load':
                mode = modes.default
                out_file.write('#include <iostream>')
                continue
            if mode == 'default':
                if token == 'nota':
                    out_file.write('std::cout << ')
                    mode = 'printing'
                    mode_value = 0
                    continue
                if token == 'def':
                    mode = modes.defining

                continue
            if mode == modes.defining:
                mode = 'default'
            if mode == 'printing':
                if token == '"':
                    out_file.write(token)
                    continue
                if token == '(':
                    continue
                if token == ')':
                    mode = 'default'
                    mode_value = 0
                    out_file.write(';\n')
                    continue
                else:
                    out_file.write(token)
                continue






with open(file_to_compile, "r", encoding='utf-8') as f:
    code = f.read()
    deal_with_code(code)
