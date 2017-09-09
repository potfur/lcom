import ast
from abc import ABCMeta, abstractmethod

import os


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
        file = file.replace('/', os.path.sep).replace('\\', os.path.sep)
        with open(file, 'r') as handle:
            content = handle.read()

        name = file.rsplit('.', 1)[0]
        replacements = (
            (os.path.sep, '.'),
            ('__init__', ''),
            ('__main__', ''),
        )
        for needle, replace in replacements:
            name = name.replace(needle, replace)

        return cls.from_string(name.strip('.'), content)

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
            ClassReflection(self.__name, node)
            for node in ast.walk(self.__node)
            if isinstance(node, ast.ClassDef)
        ]


class ClassReflection(Reflection):
    def __init__(self, module_name, node):
        self.__module_name = module_name
        self.__node = node

    def name(self):
        return '%s.%s' % (
            self.__module_name,
            self.__node.name
        )

    def method_by_name(self, name):
        nodes = [
            node
            for node in self.__class_methods()
            if node.name == name
        ]

        try:
            return MethodReflection(
                self.__module_name,
                self.__node.name,
                nodes[0]
            )
        except IndexError:
            raise ReflectionError('Unknown method %s' % name)

    def methods(self):
        return [
            MethodReflection(self.__module_name, self.__node.name, node)
            for node in self.__class_methods()
        ]

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
    def __init__(self, module_name, class_name, node):
        self.__module_name = module_name
        self.__class_name = class_name
        self.__node = node

    def name(self):
        return self.__call_name(self.__node.name)

    def is_constructor(self):
        return self.__node.name == '__init__'

    def is_loose(self):
        return not (self.__calls() | self.__vars())

    def has_decorator(self, decorator_name):
        if not hasattr(self.__node, 'decorator_list'):
            return False

        for decorator in self.__node.decorator_list:
            if decorator.id == decorator_name:
                return True
        return False

    def calls(self):
        return [
            self.__call_name(call)
            for call in self.__calls()
        ]

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

    def __call_name(self, node_name):
        return '%s.%s::%s' % (
            self.__module_name,
            self.__class_name,
            node_name
        )
