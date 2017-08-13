import os
from abc import ABCMeta, abstractmethod

import click
from terminaltables.ascii_table import AsciiTable

from src.lcom import LCOM4
from src.reflection import ModuleReflection


class FileSystem(object):
    def __init__(self, extension='py', separator='.'):
        self.__extension = extension
        self.__separator = separator

    def find(self, path, filename=None):
        if os.path.isfile(path):
            return self.__find_in_file(path, filename)
        return self.__find_in_directory(path, filename)

    def __find_in_directory(self, path, filename=None):
        result = []
        for root, dirs, files in os.walk(path):
            for file in files:
                result += self.__find_in_file(
                    os.path.join(root, file),
                    filename
                )
        return result

    def __find_in_file(self, path, filename=None):
        if self.__has_extension(path) and self.__matches(path, filename):
            return [ModuleReflection.from_file(path)]
        return []

    def __has_extension(self, file):
        return file.split(self.__separator)[-1] == self.__extension

    def __matches(self, file, filename):
        return filename is None or filename in file


class LCOMFactory(object):
    LCOM4 = 'LCOM4'

    @classmethod
    def create(cls, alg):
        if alg == cls.LCOM4:
            return LCOM4()
        raise Exception('Unknown algorithm %s' % alg)


class Printer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, algorithm, classes, average):
        raise NotImplementedError()


class STDOut(Printer):
    def render(self, algorithm, classes, average):
        print('%sCalculating LCOM using %s' % (os.linesep, algorithm))

        header = [('Method', 'LCOM')]
        classes = sorted(classes, key=lambda x: x[0])
        summary = [('Average', "%.2f" % average)]

        table = AsciiTable(header + classes + summary)
        table.inner_heading_row_border = True
        table.inner_footing_row_border = True

        print(table.table)


class PrinterFactory(object):
    STD = 'STDOut'

    @classmethod
    def create(cls, printer):
        if printer == cls.STD:
            return STDOut()
        raise Exception('Unknown printer %s' % printer)


class Runner(object):
    def __init__(self, fs, lcom, printer):
        self.__fs = fs
        self.__lcom = lcom
        self.__printer = printer

    def handle(self, paths, filter=None):
        refs = list()
        for path in paths:
            refs += self.__gather_refs(path, filter)

        cls, avg = self.__aggregate(refs)
        self.__printer.render(self.__lcom.name(), cls, avg)

    def __aggregate(self, refs):
        result = list()

        if not refs:
            return result, 0

        for ref in refs:
            result.append((
                ref.name(),
                self.__lcom.calculate(ref)
            ))

        average = sum([elem[1] for elem in result]) / len(result)
        return result, average

    def __gather_refs(self, path, filter):
        refs = list()
        for mod in self.__fs.find(path, filter):
            refs += mod.classes()
        return refs


@click.command()
@click.argument('paths', nargs=-1)
@click.option('--algorithm', default=LCOMFactory.LCOM4)
@click.option('--printer', default=PrinterFactory.STD)
def cmd(paths, algorithm, printer):
    Runner(
        FileSystem(),
        LCOMFactory.create(algorithm),
        PrinterFactory.create(printer)
    ).handle(paths)
