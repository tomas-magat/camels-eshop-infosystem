import random
from ENV_VARS import *


# Working with files

def read_file(filename):
    """Simplify reading data from a specified 
       filename and get it in a list form."""

    filepath = get_filepath(filename, '.txt')

    with open(filepath, 'r') as file:
        data = [line.rstrip('\n') for line in file.readlines()]
        data[0] = int(data[0])
        
        for i, line in enumerate(data[1:]):
            datapoint = line.split(';')
            data[i+1] = datapoint
            
    return data


def get_filepath(filename, ending='.txt'):
    """Get absolute path of data txt file. 
       Supports also filenames without extension."""

    file_format = filename.split('.')

    if len(file_format) > 1:
        if file_format[1] != 'txt':
            print("'filename' must be valid txt filename")
            return

    filename = file_format[0].upper() + ending 
    filepath = os.path.join(PATH, 'source', 'data', filename)

    return filepath


# ID Generating

def random_id(type='N'):
    """Simplify generating random ids in format:
       [type]XXXXXXXXXX (type = 'N'/'P')"""
    
    return type + str(random.randint(1000000000, 9999999999))


# File locks

def lock_file(filename):
    """Simplify locking files that are currently in use."""

    filepath = get_filepath(filename, '_LOCK.txt')
    open(filepath, 'w').close()


def unlock_file(filename):
    """Simplify unlocking files that are currently not
       in use (delete lock file)."""

    filepath = get_filepath(filename, '_LOCK.txt')

    if os.path.exists(filepath):
        os.remove(filepath)


def is_locked(filename):
    """Returns True if lock file exists else False."""

    filepath = get_filepath(filename, '_LOCK.txt')
    return os.path.exists(filepath)

