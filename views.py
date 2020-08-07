from copy import deepcopy
import itertools
from DataTypes import Pos
from Tokens import VerticesTokens


class Vertex:
    _status = VerticesTokens.isDefault
    lastIntersection = None

    def __init__(self, idKey: int, pos: Pos):
        self.isMoved = True
        self.idKey: int = idKey
        self.pos: Pos = pos

    @property
    def status(self):
        if self.isMoved:
            return VerticesTokens.isMoving
        else:
            return self._status

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

    def moveAwayFrom(self, v, intersection):
        if intersection == self.lastIntersection:
            self.moveItAway()
        diffX = v.pos.x - self.pos.x
        diffY = v.pos.y - self.pos.y
        self.pos.x += diffX * intersection / 10000
        self.pos.y += diffY * intersection / 10000
        self.isMoved = True
        self.lastIntersection = intersection

    def moveItAway(self):
        for (wtfX, wtfY) in self.randomThingIDoNotKnowWhatToNameItForNow():
            self.pos.x += wtfX
            self.pos.y += wtfY
            break

    @staticmethod
    def randomThingIDoNotKnowWhatToNameItForNow():
        for bla in list(sorted(itertools.permutations([-5, 0, 5], 2))):
            yield bla
