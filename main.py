file_to_compile = input("Enter the file to compile: ")
file_output_name = input("Output file: ")


def tokenize(code):
    """turns a string into a list of tokens"""
    split_chars = ['(', ')', '{', '}', '[', ']', ',', ';', '.', '+', '-', '*', '/', ' ', "'", '"', '\n']
    list_append_value = ''
    return_list = []
    notokenchars = ['', ' ', '\n']
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
    with open(file_output_name, 'w') as out_file:
        for token in tokenize(code):
            print(token)
            # example
            # if token == 'def':
            #     out_file.write('def')

            # out_file.write('\n')


with open(file_to_compile, "r", encoding='utf-8') as f:
    code = f.read()
    deal_with_code(code)
