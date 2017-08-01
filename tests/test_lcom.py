from src.lcom import LCOMAggregate, LCOMAlgorithm, LCOM4
from src.reflection import Reflection, ModuleReflection


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


class LCOMTestCase(object):
    @classmethod
    def setup_class(cls):
        cls.fixtures = ModuleReflection.from_file('./tests/fixtures.py')


class TestLCOM4(LCOMTestCase):
    def test_calculate_for_zero(self):
        ref = self.fixtures.class_by_name('Zero')
        lcom = LCOM4().calculate(ref)

        assert lcom == 0

    def test_calculate_for_one(self):
        ref = self.fixtures.class_by_name('One')
        lcom = LCOM4().calculate(ref)

        assert lcom == 1

    def test_calculate_for_two(self):
        ref = self.fixtures.class_by_name('Two')
        lcom = LCOM4().calculate(ref)

        assert lcom == 2

    def test_calculate_for_three(self):
        ref = self.fixtures.class_by_name('Three')
        lcom = LCOM4().calculate(ref)

        assert lcom == 3
