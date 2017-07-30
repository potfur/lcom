import os

from src.reflection import ModuleReflection


class FileSystem(object):
    def __init__(self, extension='py', separator='.'):
        self.__extension = extension
        self.__separator = separator

    def find(self, path, filename=None):
        result = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file = os.path.join(root, file)
                if not self.__has_extension(file):
                    continue
                if not self.__matches(file, filename):
                    continue
                result.append(ModuleReflection.from_file(file))
        return result

    def __has_extension(self, file):
        return file.split(self.__separator)[-1] == self.__extension

    def __matches(self, file, filename):
        return filename is None or filename in file
