from pytest import raises

from src.reflection import ModuleReflection, ReflectionError


class ReflectionTestCase(object):
    @classmethod
    def setup_class(cls):
        cls.module = ModuleReflection.from_file('./tests/fixtures.py')


class TestModuleReflection(ReflectionTestCase):
    def test_filename_handles_slashes(self):
        ref = ModuleReflection.from_file('./tests/fixtures.py')
        assert ref.class_by_name('tests.fixtures.Reflection')

    def test_filename_handles_backslashes(self):
        ref = ModuleReflection.from_file('.\\tests\\fixtures.py')
        assert ref.class_by_name('tests.fixtures.Reflection')

    def test_lists_classes(self):
        result = {cls.name() for cls in self.module.classes()}
        assert result == {
            'tests.fixtures.Zero',
            'tests.fixtures.One',
            'tests.fixtures.DeepOne',
            'tests.fixtures.Two',
            'tests.fixtures.Three',
            'tests.fixtures.Loose',
            'tests.fixtures.Reflection',
        }


class TestClassReflection(ReflectionTestCase):
    def setup_method(self):
        self.ref = self.module.class_by_name('tests.fixtures.Reflection')

    def test_list_variables(self):
        result = {var for var in self.ref.vars()}
        assert result == {
            'CONST',
            '__x',
            '__y'
        }

    def test_list_class_methods(self):
        result = {method.name() for method in self.ref.methods()}
        assert result == {
            'tests.fixtures.Reflection::decorated',
            'tests.fixtures.Reflection::__init__',
            'tests.fixtures.Reflection::get_x',
            'tests.fixtures.Reflection::get_y',
            'tests.fixtures.Reflection::loose',
            'tests.fixtures.Reflection::methods',
            'tests.fixtures.Reflection::vars',
            'tests.fixtures.Reflection::consts',
        }

    def test_method_by_name(self):
        expected = 'tests.fixtures.Reflection::get_x'
        assert self.ref.method_by_name('get_x').name() == expected

    def test_unknown_method_by_name(self):
        with raises(ReflectionError) as e:
            self.ref.method_by_name('foobar')

        msg = 'Unknown method %s'
        assert str(e.value) == msg % 'foobar'


class TestMethodReflection(ReflectionTestCase):
    def setup_method(self):
        self.ref = self.module.class_by_name('tests.fixtures.Reflection')

    def test_list_used_methods(self):
        ref = self.ref.method_by_name('methods')

        assert set(ref.calls()) == {
            'tests.fixtures.Reflection::get_x',
            'tests.fixtures.Reflection::get_y'
        }

    def test_list_used_class_variables(self):
        ref = self.ref.method_by_name('consts')

        assert set(ref.vars()) == {'CONST'}

    def test_list_used_instance_variables(self):
        ref = self.ref.method_by_name('vars')

        assert set(ref.vars()) == {'__x', '__y'}

    def test_is_a_constructor(self):
        ref = self.ref.method_by_name('__init__')

        assert ref.is_constructor() is True

    def test_is_not_a_constructor(self):
        ref = self.ref.method_by_name('methods')

        assert ref.is_constructor() is False

    def test_is_loose_method(self):
        ref = self.ref.method_by_name('loose')

        assert ref.is_loose() is True

    def test_is_not_a_loose_method(self):
        ref = self.ref.method_by_name('methods')

        assert ref.is_loose() is False

    def test_has_decorator(self):
        ref = self.ref.method_by_name('decorated')

        assert ref.has_decorator('classmethod') is True
        assert ref.has_decorator('foobar') is False

    def test_has_not_decorator(self):
        ref = self.ref.method_by_name('methods')

        assert ref.has_decorator('foo') is False
