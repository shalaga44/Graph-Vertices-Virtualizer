class Pos:

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __iter__(self):
        return [self.x, self.y]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()
