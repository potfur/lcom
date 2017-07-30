import ast

from src.reflection import ModuleReflection, ClassReflection, MethodReflection
from tests.conftest import LCOMTestCase


class ReflectionTestCase(LCOMTestCase):
    @classmethod
    def setup_class(cls):
        cls.fixture = '''
class ModuleReflection:
    EXTENSION = '.py'

    @classmethod
    def from_file(cls, file):
        with open(file, 'r') as handle:
            content = handle.read()

        return cls.from_string(file.rstrip(cls.EXTENSION), content)

    @classmethod
    def from_string(cls, name, content):
        return cls(name, ast.parse(content))

    def __init__(self, name, node):
        self.__name = name
        self.__node = node

    def __repr__(self):
        return self.__name

    def classes(self):
        return [
            ClassReflection(node)
            for node in ast.walk(self.__node)
            if isinstance(node, ast.ClassDef)
        ]
        '''


class TestModuleReflection(ReflectionTestCase):
    def test_can_be_instantiated_from_file(self):
        ref = ModuleReflection.from_file('src/reflection.py')

        assert repr(ref) == 'src/reflection.py'

    def test_can_be_instantiated_from_string(self):
        ref = ModuleReflection.from_string('reflection', self.fixture)
        assert repr(ref) == 'reflection'

    def test_lists_classes(self):
        ref = ModuleReflection.from_string('reflection', self.fixture)

        result = {repr(cls) for cls in ref.classes()}
        assert result == {'ModuleReflection'}


class TestClassReflection(ReflectionTestCase):
    @classmethod
    def setup_class(cls):
        super(TestClassReflection, cls).setup_class()
        cls.node = cls._find_node(
            cls.fixture,
            ast.ClassDef,
            ModuleReflection.__name__
        )

    def test_list_variables(self):
        ref = ClassReflection(self.node)

        result = {var for var in ref.vars()}
        assert result == {
            'EXTENSION',
            '__name',
            '__node'
        }

    def test_list_class_methods(self):
        ref = ClassReflection(self.node)

        result = {repr(method) for method in ref.methods()}
        assert result == {
            'from_file',
            'from_string',
            '__init__',
            '__repr__',
            'classes'
        }

    def test_method_by_name(self):
        ref = ClassReflection(self.node)

        assert repr(ref.method('from_file')) == 'from_file'


class TestMethodReflection(ReflectionTestCase):
    def test_list_used_methods(self):
        node = self._find_node(self.fixture, ast.FunctionDef, 'from_file')
        ref = MethodReflection(node)

        assert set(ref.calls()) == {'from_string'}

    def test_list_used_class_variables(self):
        node = self._find_node(self.fixture, ast.FunctionDef, 'from_file')
        ref = MethodReflection(node)

        assert set(ref.vars()) == {'EXTENSION'}

    def test_list_used_instance_variables(self):
        node = self._find_node(self.fixture, ast.FunctionDef, 'classes')
        ref = MethodReflection(node)

        assert set(ref.vars()) == {'__node'}

    def test_is_a_constructor(self):
        node = self._find_node(self.fixture, ast.FunctionDef, '__init__')
        ref = MethodReflection(node)

        assert ref.is_constructor() is True

    def test_is_not_a_constructor(self):
        node = self._find_node(self.fixture, ast.FunctionDef, 'classes')
        ref = MethodReflection(node)

        assert ref.is_constructor() is False
