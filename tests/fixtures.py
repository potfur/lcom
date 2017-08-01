class Zero:
    pass


class One:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def a(self):
        self.b()

    def b(self):
        return self.x

    def c(self):
        return self.x + self.y

    def d(self):
        return self.e(self.y)

    def e(self, n):
        return n * 2


class Two:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def a(self):
        self.b()

    def b(self):
        return self.x

    def c(self):
        return self.y

    def d(self):
        return self.e(self.y)

    def e(self, n):
        return n * 2


class Three:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def a(self):
        return self.x

    def b(self):
        return self.y

    def c(self):
        return self.z


class Reflection:
    CONST = 'const'

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def methods(self):
        return self.get_x() + self.get_y()

    def vars(self):
        return self.__x + self.__y

    def consts(self):
        return self.CONST