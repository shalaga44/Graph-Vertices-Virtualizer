from pygame import Vector2


class Pos(Vector2):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x: int = x
        self.y: int = y

    def location(self):
        return [int(self.x), int(self.y)]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()
