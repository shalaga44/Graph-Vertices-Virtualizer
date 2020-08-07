class Pos:

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __iter__(self):
        return [self.x, self.y]
