import ast
from abc import ABCMeta, abstractmethod


class ReflectionError(Exception):
    pass


class Reflection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def name(self):
        raise NotImplementedError()


class ModuleReflection(Reflection):
    @classmethod
    def from_file(cls, file):
        with open(file, 'r') as handle:
            content = handle.read()

        return cls.from_string(file, content)

    @classmethod
    def from_string(cls, name, content):
        return cls(name, ast.parse(content))

    def __init__(self, name, node):
        self.__name = name
        self.__node = node

    def name(self):
        return self.__name

    def class_by_name(self, name):
        for elem in self.classes():
            if elem.name() == name:
                return elem
        raise ReflectionError('Unknown class %s' % name)

    def classes(self):
        return [
            ClassReflection(node)
            for node in ast.walk(self.__node)
            if isinstance(node, ast.ClassDef)
        ]


class ClassReflection(Reflection):
    def __init__(self, node):
        self.__node = node

    def name(self):
        return self.__node.name

    def method_by_name(self, name):
        for method in self.methods():
            if method.name() == name:
                return method

        raise ReflectionError('Unknown method %s' % name)

    def methods(self):
        return [MethodReflection(node) for node in self.__class_methods()]

    def vars(self):
        result = self.__class_vars()
        result |= self.__instance_vars()
        result -= {node.name for node in self.__class_methods()}
        return list(result)

    def __class_vars(self):
        return {
            target.id
            for node in self.__node.body
            if isinstance(node, ast.Assign)
            for target in node.targets
        }

    def __instance_vars(self):
        return {
            node.attr
            for node in ast.walk(self.__node)
            if isinstance(node, ast.Attribute) and node.value.id == 'self'
        }

    def __class_methods(self):
        return {
            node
            for node in self.__node.body
            if isinstance(node, ast.FunctionDef)
        }


class MethodReflection(Reflection):
    def __init__(self, node):
        self.__node = node

    def name(self):
        return self.__node.name

    def is_constructor(self):
        return self.__node.name == '__init__'

    def calls(self):
        return list(self.__calls())

    def vars(self):
        return list(self.__vars() - self.__calls())

    def __vars(self):
        return {
            node.attr
            for node in ast.walk(self.__node)
            if isinstance(node, ast.Attribute)
               and hasattr(node.value, 'id')
               and node.value.id in ('cls', 'self')
        }

    def __calls(self):
        return {
            node.func.attr
            for node in ast.walk(self.__node)
            if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Attribute)
               and hasattr(node.func.value, 'id')
               and node.func.value.id in ('cls', 'self')
        }

    def __call_name(self, node):
        if isinstance(node.func, ast.Attribute):
            return node.func.value.id
        return node.func.id
