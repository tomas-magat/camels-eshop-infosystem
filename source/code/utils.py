import random
import threading
import time

from ENV_VARS import *


# Working with files

def read_file(filename):
    """Simplify reading data from a specified 
       filename and get it in a list form."""

    filepath = get_filepath(filename, '.txt')

    with open(filepath, 'r') as file:
        lines = file.readlines()
        data = scsv_to_list(lines[1:])
                    
    return data


def save_to_file(filename, data):
    """Simplify saving data entries in format [[],[],...]."""

    update_version(filename)

    filepath = get_filepath(filename, '.txt')
    scsv_data = list_to_scsv(data)
    
    with open(filepath, 'w') as file:
        file.writelines(scsv_data)


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


# File versions

def update_version(filename):
    """Simplify incrementing version number in
       a filename_VERZIA.txt file."""
    
    filepath = get_filepath(filename, '_VERZIA.txt')

    with open(filepath, 'r+') as file:
        line = file.read().rstrip('\n')
        version = int(line)+1 if line.isdigit() else 1
        
        file.seek(0)
        file.truncate()
        file.write(str(version))


def get_version(filename):
    """Return version integer from [filename]_VERZIA.txt."""

    filepath = get_filepath(filename, '_VERZIA.txt')

    with open(filepath, 'r') as file:
        version = int(file.read().rstrip('\n'))
        return version


# Background periodical function calling

def run_periodically(function, delay=5):
    """Use threading and time.sleep() to run function
       with delay while not affecting the runtime of app."""

    background_thread = threading.Thread(target=
        lambda: callback(function, delay))
    background_thread.start()


def callback(function, delay):
    """Run function forever with delays between each run."""

    while True:
        function()
        time.sleep(delay)


# Data converting

def list_to_scsv(data):
    """
    Converts data in format:
    [[val,val2],...] 
    
    to valid semi-colon separated values in a list:
    ['length', 'val;val', ...]
    """

    length = len(data)
    scsv_data = [str(length)+'\n']

    for item in data:
        datapoint = ';'.join(item) + '\n'
        scsv_data.append(datapoint)

    return scsv_data


def scsv_to_list(data):
    """
    Converts data in semi-colon separated format:
    ['length', 'val;val', ...]
    
    to list:
    [[val,val2],...]
    """
    
    for i, line in enumerate(data):
        datapoint = line.rstrip('\n').split(';')
        data[i] = datapoint

    return data
    

# PATH generating

def get_filepath(filename, ending='.txt'):
    """Get absolute path of data txt file. 
       Supports also filenames without extension."""

    file_format = filename.split('.')

    if len(file_format) > 1 and file_format[1] != 'txt':
        print("'filename' must be valid txt filename")
        return

    filename = file_format[0].upper() + ending 
    filepath = os.path.join(PATH, 'source', 'data', filename)

    return filepath
