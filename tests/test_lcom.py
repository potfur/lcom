from src.lcom import LCOM4
from src.reflection import ModuleReflection


class LCOMTestCase(object):
    @classmethod
    def setup_class(cls):
        cls.fixtures = ModuleReflection.from_file('./tests/fixtures.py')


class TestLCOM4(LCOMTestCase):
    def test_calculate_for_zero(self):
        ref = self.fixtures.class_by_name('tests.fixtures.Zero')
        lcom = LCOM4().calculate(ref)

        assert lcom == 0

    def test_calculate_for_one(self):
        ref = self.fixtures.class_by_name('tests.fixtures.One')
        lcom = LCOM4().calculate(ref)

        assert lcom == 1

    def test_calculate_for_two(self):
        ref = self.fixtures.class_by_name('tests.fixtures.Two')
        lcom = LCOM4().calculate(ref)

        assert lcom == 2

    def test_calculate_for_three(self):
        ref = self.fixtures.class_by_name('tests.fixtures.Three')
        lcom = LCOM4().calculate(ref)

        assert lcom == 3

    def test_calculate_for_deep(self):
        ref = self.fixtures.class_by_name('tests.fixtures.DeepOne')
        lcom = LCOM4().calculate(ref)

        assert lcom == 1

    def test_calculate_for_loose(self):
        ref = self.fixtures.class_by_name('tests.fixtures.Loose')
        lcom = LCOM4().calculate(ref)

        assert lcom == 0
