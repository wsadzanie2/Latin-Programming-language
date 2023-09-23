file_to_compile = input("Enter the file to compile: ")
file_output_name = input("Output file: ")

mode = 'load'
mode_value = 0
mode_buffer = []
mode_buffer2 = []
mode_dict = {}
mode_string = ''
mode_bool = False
mode_spaces = 0

def reset_mode_values():
    global mode_value, mode_buffer, mode_buffer2, mode_string, mode_dict, mode_bool
    mode_value = 0
    mode_buffer = []
    mode_buffer2 = []
    mode_dict = {}
    mode_string = ''
    mode_bool = False


class Modes:
    """Class containing all possible compile mods"""
    def __init__(self):
        self.load = 'load'
        self.default = 'default'
        self.printing = 'printing'
        self.defining = 'defining'
        self.getting_type = 'getting_type'

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
    global mode, mode_value, mode_string, mode_bool, mode_dict, mode_spaces
    with open(file_output_name, 'w') as out_file:
        for index, token in enumerate(tokenize(code)):
            # load mode (loads the compiler and necessary things)
            if mode == 'load':
                mode = modes.default
                out_file.write('#include <iostream>' + '\n')
            # default mode (used for detecting commands)
            if mode == 'default':
                if mode_spaces > 0 and token == '\n':
                    out_file.write(' '*mode_spaces)
                if token == 'nota':
                    out_file.write('std::cout << ')
                    mode = 'printing'
                    mode_value = 0
                    continue
                if token == 'def':
                    reset_mode_values()
                    mode = modes.defining
                if token == '}':
                    mode_spaces -= 4
                    out_file.write('\n}')

                # Later it might raise an error here ;)
                continue
                # mode used for defining classes and functions
            if mode == modes.defining:
                mode_buffer.append(token)
                current_token = len(mode_buffer)
                if current_token == 1:
                    mode_string = token
                if current_token == 2:
                    if token != '(':
                        raise Exception(f"Jesteś Debilem! Zapomniałeś o nawiasie! (token {index})")
                    continue
                if token != ')':
                    if token != ',' and (not mode_bool):
                        mode_buffer2.append(token)
                else:
                    mode_bool = True
                if token == '>':
                    mode = modes.getting_type
                    continue
                if token == '{':
                    mode = 'default'
                    temp_string = '('
                    for var in mode_buffer2:
                        temp_string += var + ', '
                    temp_string = temp_string[:-2] + ')'

                    out_file.write(f'{mode_buffer2[1]} {mode_buffer2[0]} ' + temp_string + '{' + '\n')
                    mode_spaces += 4
                    continue

            if mode == modes.getting_type:
                mode_buffer2.insert(1, token)
                mode = modes.defining
                continue

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
                    out_file.write(token + ' ')
                continue


with open(file_to_compile, "r", encoding='utf-8') as f:
    code = f.read()
    deal_with_code(code)
