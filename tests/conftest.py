import ast


class LCOMTestCase(object):
    @classmethod
    def _find_node(cls, fixture, type, name):
        for node in ast.walk(ast.parse(fixture)):
            if isinstance(node, type) and node.name == name:
                return node
