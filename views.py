import itertools
from copy import deepcopy

from pygame.surface import Surface
from pygame.font import SysFont
from pygame.font import get_default_font

import Colors
from DataTypes import Pos
from Diments import Diments
from Tokens import VerticesTokens


class Vertex:
    _color = Colors.VerticesColors.vertexDefaultColor
    _status = VerticesTokens.isDefault
    _isMoved = True

    wTextHalf, hTextHalf = None, None
    lastIntersection = None

    def __init__(self, idKey: int, pos: Pos):
        self.idKey: int = idKey
        self.pos: Pos = pos
        self.textImage = self.getTextImage()

    def getTextImage(self) -> Surface:
        font = SysFont(get_default_font(), Diments.fontSizeOnVertex)
        keyImage = font.render(str(self.idKey), True, Colors.VerticesColors.OnVertexDefaultColor)
        wText, hText = font.size(str(self.idKey))
        self.wTextHalf, self.hTextHalf = wText // 2, hText // 2
        return keyImage

    @property
    def textPos(self):
        return self.pos.x - self.wTextHalf, self.pos.y - self.hTextHalf

    @property
    def color(self):
        return self._color

    @property
    def isMoved(self):
        return self._isMoved

    @isMoved.setter
    def isMoved(self, b: bool):
        self.updateColor()
        self._isMoved = b

    @property
    def status(self):
        if self.isMoved:
            return VerticesTokens.isMoving
        else:
            return self._status

    @status.setter
    def status(self, newStatus):
        self._status = newStatus
        self.updateColor()

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
            if k == "textImage":
                setattr(result, k, v)
            else:
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

    def updateColor(self):
        color = Colors.MainColors.onSurfaceColor
        if self.status == VerticesTokens.isDefault:
            color = Colors.VerticesColors.vertexDefaultColor
        elif self.status == VerticesTokens.isSelected:
            color = Colors.VerticesColors.vertexSelectedColor
        elif self.status == VerticesTokens.isMoving:
            color = Colors.VerticesColors.isMoving
        self._color = color
