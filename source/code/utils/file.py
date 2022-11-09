# Simplify working with data files
import os

from .ENV_VARS import *


class DataFile:

    def __init__(self, filename):
        """
        Required parameter: filename (string, lower or
        uppercase, supports also filename without extension).
        Get absolute path for the file using get_filepath().
        """

        self.filename = filename
        self.filepath = self.get_filepath()

    def read(self):
        """
        Simplify reading data from a specified 
        filename and return it in a 2D list format.
        """

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            data = self.scsv_to_list(lines[1:])

        return data

    def save_data(self, data):
        """
        Convert data entry to semi-colon separated 
        values and save it to [filename].txt.
        Update version number of the saved [filename].
        """

        self.update_version()

        scsv_data = self.list_to_scsv(data)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(scsv_data)

    def lock(self):
        """Simplify locking files that are currently in use."""

        lockpath = self.filepath.split('.')[0]+'_LOCK.txt'
        open(lockpath, 'w', encoding='utf-8').close()

    def unlock(self):
        """
        Simplify unlocking files that are currently not
        in use (delete lock file if it exists).
        """

        lockpath = self.filepath.split('.')[0]+'_LOCK.txt'

        if os.path.exists(lockpath):
            os.remove(lockpath)

    def is_locked(self):
        """Returns True if lock file exists else False."""

        lockpath = self.filepath.split('.')[0]+'_LOCK.txt'
        return os.path.exists(lockpath)

    def update_version(self):
        """
        Simplify incrementing version number in
        a filename_VERZIA.txt file.
        """

        versionpath = self.filepath.split('.')[0]+'_VERZIA.txt'

        with open(versionpath, 'r+', encoding='utf-8') as file:
            line = file.read().rstrip('\n')
            version = int(line)+1 if line.isdigit() else 1

            file.seek(0)
            file.truncate()
            file.write(str(version))

    def get_version(self):
        """Return version integer from [filename]_VERZIA.txt."""

        versionpath = self.filepath.split('.')[0]+'_VERZIA.txt'

        with open(versionpath, 'r', encoding='utf-8') as file:
            version = int(file.read().rstrip('\n'))
            return version

    def get_filepath(self, ending='.txt'):
        """
        Get absolute path of data txt file. 
        """

        file_format = self.filename.split('.')

        if len(file_format) > 1 and file_format[1] != 'txt':
            print("'filename' must be valid txt filename")
            return

        filename = file_format[0].upper() + ending
        filepath = os.path.join(PATH, 'source', 'data', filename)

        return filepath

    @staticmethod
    def list_to_scsv(data):
        """
        Converts data in 2D list format:
        [[val,val2],...] 

        to semi-colon separated values in a list:
        ['length', 'val;val', ...]
        """

        length = len(data)
        scsv_data = [str(length)+'\n']

        for item in data:
            datapoint = ';'.join(item) + '\n'
            scsv_data.append(datapoint)

        return scsv_data

    @staticmethod
    def scsv_to_list(data):
        """
        Converts data in semi-colon separated format:
        ['length', 'val;val', ...]

        to 2D list:
        [[val,val2],...]
        """

        for i, line in enumerate(data):
            datapoint = line.rstrip('\n').split(';')
            data[i] = datapoint

        return data
