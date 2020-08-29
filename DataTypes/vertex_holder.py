from typing import Any

from DataTypes.pos import Pos


class VertexHolder:
    def __init__(self, name: Any, pos: tuple = None):
        self.name = name
        self.pos = pos if pos is None else Pos(*pos)
