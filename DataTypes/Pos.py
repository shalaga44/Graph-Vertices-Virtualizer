class Pos:

    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    def location(self):
        return [int(self.x), int(self.y)]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = int(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = int(y)
