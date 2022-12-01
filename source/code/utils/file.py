# Simplify working with data files
import os

from .ENV_VARS import PATH


class DataFile:

    def __init__(self, filename):
        """
        Required parameter: filename (string, lower or
        uppercase, supports also filename without extension).
        Get absolute path for the file using get_filepath().
        """

        self.filename = filename
        self.filepath = self.get_filepath()

        self.read()
        self.get_version()

    def read(self):
        """
        Simplify reading data from a specified 
        filename and return it in a dictionary format.
        """

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.data = self.scsv_to_dict(lines[1:])

    def save_data(self):
        """
        Convert data to semi-colon separated 
        values and save it to the [filename].txt.
        Update version number of the saved [filename].
        """

        self.update_version()

        scsv_data = self.dict_to_scsv(self.data)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(scsv_data)

    def lock(self):
        """Simplify locking files that are currently in use."""

        lock_path = self.filepath.split('.')[0]+'_LOCK.txt'
        open(lock_path, 'w', encoding='utf-8').close()

    def unlock(self):
        """
        Simplify unlocking files that are currently not
        in use (delete lock file if it exists).
        """

        lock_path = self.filepath.split('.')[0]+'_LOCK.txt'

        if os.path.exists(lock_path):
            os.remove(lock_path)

    def is_locked(self):
        """Returns True if lock file exists else False."""

        lock_path = self.filepath.split('.')[0]+'_LOCK.txt'
        return os.path.exists(lock_path)

    def update_version(self):
        """
        Simplify incrementing version number in
        a filename_VERZIA.txt file.
        """

        version_path = self.filepath.split('.')[0]+'_VERZIA.txt'

        with open(version_path, 'w', encoding='utf-8') as file:
            self.version += 1
            file.write(str(self.version))

    def get_version(self):
        """Return version integer from [filename]_VERZIA.txt."""

        version_path = self.filepath.split('.t')[0]+'_VERZIA.txt'

        with open(version_path, 'r', encoding='utf-8') as file:
            line = file.read().rstrip('\n')
            if line == '' or not line.isdigit():
                self.version = 0
                self.update_version()
            else:
                self.version = int(line)

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
    def dict_to_scsv(data: dict):
        """
        Converts data in dictionary format:
        {'code': [name, image], ...}

        to semi-colon separated values in a list:
        ['length', 'code;name;image', ...]
        """

        length = len(data)
        scsv_data = [str(length)+'\n']

        for key, values in data.items():
            datapoint = ';'.join([key]+[str(val)
                                 for val in values]) + '\n'
            scsv_data.append(datapoint)

        return scsv_data

    @staticmethod
    def scsv_to_dict(data: list):
        """
        Converts data in semi-colon separated format:
        ['code;name;image', ...]

        to dictionary:
        {'code': [name, image], ...}
        """

        result_dict = {}

        for line in data:
            datapoint = line.rstrip('\n').split(';')
            result_dict[datapoint[0]] = datapoint[1:]

        return result_dict
