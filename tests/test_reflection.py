from pytest import raises

from src.reflection import ModuleReflection, ReflectionError


class ReflectionTestCase(object):
    @classmethod
    def setup_class(cls):
        cls.module = ModuleReflection.from_file('./tests/fixtures.py')


class TestModuleReflection(ReflectionTestCase):
    def test_lists_classes(self):
        result = {cls.name() for cls in self.module.classes()}
        assert result == {'Zero', 'One', 'Two', 'Three', 'Reflection'}


class TestClassReflection(ReflectionTestCase):
    def test_list_variables(self):
        ref = self.module.class_by_name('Reflection')

        result = {var for var in ref.vars()}
        assert result == {
            'CONST',
            '__x',
            '__y'
        }

    def test_list_class_methods(self):
        ref = self.module.class_by_name('Reflection')

        result = {method.name() for method in ref.methods()}
        assert result == {
            '__init__',
            'get_x',
            'get_y',
            'methods',
            'vars',
            'consts',
        }

    def test_method_by_name(self):
        ref = self.module.class_by_name('Reflection')

        assert ref.method_by_name('get_x').name() == 'get_x'

    def test_unknown_method_by_name(self):
        ref = self.module.class_by_name('Reflection')

        with raises(ReflectionError) as e:
            ref.method_by_name('foobar')

        msg = 'Unknown method %s'
        assert str(e.value) == msg % 'foobar'


class TestMethodReflection(ReflectionTestCase):
    def test_list_used_methods(self):
        ref = self.module.class_by_name('Reflection') \
            .method_by_name('methods')

        assert set(ref.calls()) == {'get_x', 'get_y'}

    def test_list_used_class_variables(self):
        ref = self.module.class_by_name('Reflection') \
            .method_by_name('consts')

        assert set(ref.vars()) == {'CONST'}

    def test_list_used_instance_variables(self):
        ref = self.module.class_by_name('Reflection') \
            .method_by_name('vars')

        assert set(ref.vars()) == {'__x', '__y'}

    def test_is_a_constructor(self):
        ref = self.module.class_by_name('Reflection') \
            .method_by_name('__init__')

        assert ref.is_constructor() is True

    def test_is_not_a_constructor(self):
        ref = self.module.class_by_name('Reflection') \
            .method_by_name('methods')

        assert ref.is_constructor() is False
