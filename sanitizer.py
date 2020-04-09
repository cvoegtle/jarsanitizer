import os
import sys
from os.path import isdir, isfile, join
from zipfile import ZipFile


class FileFinder:
    base_directory = "."

    def __init__(self, directory="."):
        self.base_directory = directory

    def find(self, extension=".jar"):
        files = os.listdir(self.base_directory)

        found_files = [join(self.base_directory, file) for file in files if isfile(join(self.base_directory, file)) and file.endswith(extension)]

        for dir in [join(self.base_directory, file) for file in files if isdir(join(self.base_directory, file))]:
            found_files.extend(FileFinder(dir).find(extension))

        return found_files


class Sanitizer:
    TEMP_EXTENSION = '.tmp'

    def __init__(self, remove_filename='module-info.class'):
        self.remove_filename = remove_filename

    def clean(self, zip_filename):
        temp_filename = zip_filename + self.TEMP_EXTENSION
        removed = False

        zip_in = ZipFile(zip_filename)
        zip_out = ZipFile(temp_filename, 'w')
        for item in zip_in.infolist():
            is_file = not item.is_dir()
            if is_file and item.filename != self.remove_filename:
                buffer = zip_in.read(item.filename)
                zip_out.writestr(item.filename, buffer)
            elif is_file:
                removed = True
        zip_out.close()
        zip_in.close()

        if removed:
            os.remove(zip_filename)
            os.rename(temp_filename, zip_filename)
        else:
            os.remove(temp_filename)

        return removed


def identify_working_directory():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return join(home_directory(), '.m2/repository')


def home_directory():
    if 'HOME' in os.environ:
        return os.environ['HOME'] # Unix
    else:
        return os.environ['HOMEPATH'] # must be windows


def sanitize():
    filefinder = FileFinder(identify_working_directory())
    sanitizer = Sanitizer()
    files = filefinder.find()
    for filename in files:
        if sanitizer.clean(filename):
            print(filename)


if __name__ == '__main__':
    sanitize()
