from collections import defaultdict


class LCOM4:
    def calculate(self, cls_ref):
        paths = self.__access_paths(cls_ref)

        groups = list()
        for path in paths.values():
            group = self.__find_matching_group(path, groups)
            group |= path

        return len(groups)

    def __access_paths(self, ref):
        result = defaultdict(set)
        for method in ref.methods():
            if method.is_constructor():
                continue

            name = repr(method)
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

    def __find_matching_group(self, path, groups):
        for other in groups:
            if other & path:
                return other

        other = set()
        groups.append(other)
        return other
