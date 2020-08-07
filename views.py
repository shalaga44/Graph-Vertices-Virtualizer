from copy import deepcopy

from DataTypes import Pos


class Vertex:
    status = "default"

    def __init__(self, idKey: int, pos: Pos):
        self.idKey: int = idKey
        self.pos: Pos = pos

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __str__(self):
        return f"id:{self.idKey}, pos:{self.pos}"

    def __repr__(self):
        return self.__str__()
