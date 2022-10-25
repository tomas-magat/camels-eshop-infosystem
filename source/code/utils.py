from ENV_VARS import *


def read_file(filename):
    """Simplify reading data from a specified filename 
       and get it in a dictionary form."""

    data_dict = {}

    file_format = filename.split('.')
    if len(file_format) > 1:
        if file_format[1] != 'txt':
            print("'filename' should be name of valid txt filename")
    else:
        filename = file_format[0] + '.txt' 

    filepath = os.path.join(PATH, 'source', 'data', filename)

    with open(filepath, 'r') as file:
        lines = file.readlines()
        data_dict['lines'] = len(lines)-1
        data_dict['data'] = []

        for line in lines[1:]:
            data_dict['data'].append(line)
            
    return data_dict
