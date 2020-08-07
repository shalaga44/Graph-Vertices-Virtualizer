from DataTypes import Pos


class Vertex:
    status = "default"

    def __init__(self, idKey: int, pos: Pos):
        self.idKey: int = idKey
        self.pos: Pos = pos
