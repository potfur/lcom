from mock import patch

from src.command import FileSystem, STDOut, LCOMFactory, PrinterFactory, \
    Runner, Printer
from src.lcom import LCOM4, LCOMAlgorithm
from src.reflection import Reflection


class FakeReflection(Reflection):
    def module_name(self):
        return 'foo'

    def name(self):
        return 'FakeReflection'

    def classes(self):
        return [self]


class FakeFileSystem(object):
    def __init__(self):
        self.result = []

    def find(self, path, filename=None):
        return self.result


class FakeLCOM(LCOMAlgorithm):
    def __init__(self):
        self.result = 1

    def name(self):
        return 'FakeLCOM'

    def calculate(self, ref):
        return self.result


class FakePrinter(Printer):
    def __init__(self):
        self.output = []

    def render(self, algorithm, classes, average):
        self.output.append((
            algorithm,
            classes,
            average
        ))


class TestFileSystem(object):
    def setup_method(self):
        self.fs = FileSystem()

    def test_find_scans_directory(self):
        result = self.fs.find('src/')
        result = {ref.name() for ref in result}

        assert result == {
            'src',
            'src.command',
            'src.lcom',
            'src.reflection'
        }

    def test_find_can_filter_by_file_name(self):
        result = self.fs.find('src/', 'command.py')
        result = {ref.name() for ref in result}

        assert result == {'src.command'}


class TestLCOMAlgorithmFactory(object):
    def test_create_lcom4(self):
        result = LCOMFactory.create(LCOMFactory.LCOM4)

        assert isinstance(result, LCOM4)


class TestSTDOutPrinter(object):
    def test_print(self):
        output = list()

        def fnc(text):
            output.append(text)

        with patch('sys.stdout') as stdout:
            stdout.write = fnc

            STDOut().render('lcom0', [('Foo', 1)], 1.0)

        expected = 'Calculating LCOM using lcom0\n  Foo : 1\nAverage: 1.00\n'
        assert "".join(output) == expected


class TestPrinterFactory(object):
    def test_create_std(self):
        result = PrinterFactory.create(PrinterFactory.STD)

        assert isinstance(result, STDOut)


class TestRunner(object):
    def setup_method(self):
        self.fs = FakeFileSystem()
        self.lcom = FakeLCOM()
        self.printer = FakePrinter()

    def test_handle_without_classes(self):
        runner = Runner(self.fs, self.lcom, self.printer)
        runner.handle('/foo')

        assert self.printer.output == [('FakeLCOM', [], 0)]

    def test_handle_with_classes(self):
        self.fs.result = [FakeReflection()]

        runner = Runner(self.fs, self.lcom, self.printer)
        runner.handle(['/foo'])

        assert self.printer.output == [(
            'FakeLCOM',
            [('FakeReflection', 1)],
            1.0
        )]
