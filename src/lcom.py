from abc import ABCMeta, abstractmethod
from collections import defaultdict


class LCOMAlgorithm(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate(self, ref):
        raise NotImplementedError()


class LCOM4(LCOMAlgorithm):
    def calculate(self, ref):
        paths = self.__call_paths(ref)

        groups = self.__match_groups(paths.values())
        groups = self.__match_groups(groups)

        return len(groups)

    def __call_paths(self, ref):
        result = defaultdict(set)
        for method in ref.methods():
            if method.is_constructor():
                continue

            name = method.name()
            result[name] |= set([name] + method.vars())
            for call in method.calls():
                result[name].add(call)
                result[call].add(name)
                result[name] |= self.__follow_call(ref, call)

        return result

    def __follow_call(self, ref, name):
        method = ref.method(name)
        result = set(method.vars() + method.calls())

        for call in method.calls():
            result |= self.__follow_call(ref, call)

        return result

    def __match_groups(self, groups):
        result = list()

        for group in groups:
            match = self.__find_matching_group(group, result)
            match |= group

        return result

    def __find_matching_group(self, path, groups):
        for other in groups:
            if other & path:
                return other

        other = set()
        groups.append(other)
        return other
