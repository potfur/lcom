import ast

from src.lcom import LCOMAggregate, LCOMAlgorithm, LCOM4
from src.reflection import Reflection, ClassReflection
from tests.conftest import LCOMTestCase


class FakeLCOM(LCOMAlgorithm):
    def __init__(self, results):
        self.__results = results

    def calculate(self, ref):
        return self.__results.pop(0)


class FakeReflection(Reflection):
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name


class TestLCOMAggregate(object):
    def test_calculates_lcom_for_each_ref(self):
        result = LCOMAggregate(FakeLCOM([1])) \
            .calculate([FakeReflection('ref.name')])

        assert result == ({'ref.name': 1}, 1.0)


class TestLCOM4(LCOMTestCase):
    def cls_ref(self, fixture, cls_name):
        node = self._find_node(fixture, ast.ClassDef, cls_name)
        return ClassReflection(node)

    def test_calculate_for_zero(self):
        fixture = '''
class Zero:
    pass
        '''

        ref = self.cls_ref(fixture, 'Zero')
        lcom = LCOM4().calculate(ref)

        assert lcom == 0

    def test_calculate_for_one(self):
        fixture = '''
class One:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def a(self):
        self.b()

    def b(self):
        return self.x

    def c(self):
        return self.x + self.y

    def d(self):
        return self.e(self.y)

    def e(self, n):
        return n * 2
        '''

        ref = self.cls_ref(fixture, 'One')
        lcom = LCOM4().calculate(ref)

        assert lcom == 1

    def test_calculate_for_two(self):
        fixture = '''
class Two:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def a(self):
        self.b()

    def b(self):
        return self.x

    def c(self):
        return self.y

    def d(self):
        return self.e(self.y)

    def e(self, n):
        return n * 2
        '''

        ref = self.cls_ref(fixture, 'Two')
        lcom = LCOM4().calculate(ref)

        assert lcom == 2

    def test_calculate_for_three(self):
        fixture = '''
class Three:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y

    def a(self):
        return self.x

    def b(self):
        return self.y

    def c(self):
        return self.z
        '''

        ref = self.cls_ref(fixture, 'Three')
        lcom = LCOM4().calculate(ref)

        assert lcom == 3
