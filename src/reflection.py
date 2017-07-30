import ast
from abc import ABCMeta, abstractmethod


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

    def method(self, name):
        nodes = [
            node
            for node in self.__node.body
            if isinstance(node, ast.FunctionDef) and node.name == name
        ]

        return MethodReflection(nodes[0])

    def methods(self):
        return [
            MethodReflection(node)
            for node in self.__node.body
            if isinstance(node, ast.FunctionDef)
        ]

    def vars(self):
        return list(self.__class_vars() | self.__instance_vars())

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
            and node.value.id in ('cls', 'self')
        }

    def __calls(self):
        return {
            node.func.attr
            for node in ast.walk(self.__node)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.value.id in ('cls', 'self')
        }

    def __call_name(self, node):
        if isinstance(node.func, ast.Attribute):
            return node.func.value.id
        return node.func.id
