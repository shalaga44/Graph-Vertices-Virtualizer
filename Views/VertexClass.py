import itertools
import random
from copy import deepcopy
from typing import Dict, Set, Final, NoReturn

from pygame.font import SysFont
from pygame.font import get_default_font
from pygame.surface import Surface

import Colors
from DataTypes.Pos import Pos
from Tokens import VerticesTokens


class Vertex:
    _color = Colors.VerticesColors.vertexDefaultColor
    _status = VerticesTokens.isDefault
    _isMoved = True

    _lastIntersectionMemorySize = 6
    _lastIntersectionMemoryIndex = 0
    _lastIntersectionMemory: Final[Set[float]] = {float(emptyCell)
                                                  for emptyCell in range(_lastIntersectionMemorySize)}
    _lastIntersectionMemoryMap: Final[Dict[int, float]] = {emptyCell: float(emptyCell) for emptyCell in
                                                           range(_lastIntersectionMemorySize)}
    wTextHalf, hTextHalf = None, None
    _lastIntersection = None

    textImage: Surface

    def __init__(self, vertexName, pos: Pos):
        self.vertexName: str = str(vertexName)
        self._pos: Pos = pos
        self.generateNewTextImage()

    def moveCloserTo(self, pos: Pos, distance):
        diffX = pos.x - self.pos.x
        diffY = pos.y - self.pos.y
        moveX = diffX * distance
        moveY = diffY * distance
        self.pos.x += moveX
        self.pos.y += moveY
        self.isMoved = True

        # TODO : REMOVE
        self.lastIntersection = distance

    def moveAwayFrom(self, pos: Pos, distance):

        if distance == -1.0:
            self.fixOverlapping()
        diffX = pos.x - self.pos.x
        diffY = pos.y - self.pos.y
        # print(f"{diffX=} {diffY=} {distance=}")
        self.pos.x += diffX * distance
        self.pos.y += diffY * distance
        self.isMoved = True
        # TODO : REMOVE
        self.lastIntersection = distance

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, newPos):
        # self.isMoved = True
        self.pos = newPos

    @property
    def lastIntersection(self):
        raise NotImplementedError("Use isLastIntersection(intersection: float)")

    @lastIntersection.setter
    def lastIntersection(self, newIntersection):
        if self.isLastIntersection(newIntersection): return
        self.addNewIntersectionToMemory(newIntersection)

    def isLastIntersection(self, intersection: float):
        return intersection in self._lastIntersectionMemory

    def generateNewTextImage(self):
        from Mangers.GraphManager import DimensionsManger
        diments = DimensionsManger()
        font = SysFont(get_default_font(), diments.VerticesDiments.fontSize)
        keyImage = font.render(str(self.vertexName), True, Colors.VerticesColors.OnVertexDefaultColor)
        wText, hText = font.size(str(self.vertexName))
        self.wTextHalf, self.hTextHalf = wText // 2, hText // 2
        self.textImage = keyImage
        self.isMoved = True

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
        if self._status == VerticesTokens.isSelected:
            return VerticesTokens.isSelected
        elif self.isMoved or 1:
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
        return self.vertexName

    def __repr__(self):
        return self.__str__()

    def updateColor(self):
        color = Colors.MainColors.onSurfaceColor
        status = self.status
        if status == VerticesTokens.isDefault:
            color = Colors.VerticesColors.vertexDefaultColor
        elif status == VerticesTokens.isSelected:
            color = Colors.VerticesColors.vertexSelectedColor
        elif status == VerticesTokens.isMoving:
            color = Colors.VerticesColors.isMoving
        self._color = color

    def _incrementLastIntersectionMemory(self):
        self._lastIntersectionMemoryIndex = (self._lastIntersectionMemoryIndex + 1) % \
                                            self._lastIntersectionMemorySize

    def _lastMemoryCellKey(self) -> float:
        return self._lastIntersectionMemoryMap[self._lastIntersectionMemoryIndex]

    def _replaceIntersectionsInMemory(self, lastMemoryCell: float, newIntersection: float):
        self._lastIntersectionMemory.remove(lastMemoryCell)
        self._lastIntersectionMemory.add(newIntersection)
        self._lastIntersectionMemoryMap[self._lastIntersectionMemoryIndex] = newIntersection

    def addNewIntersectionToMemory(self, newIntersection: float):
        lastMemoryCell = self._lastMemoryCellKey()
        self._replaceIntersectionsInMemory(lastMemoryCell, newIntersection)
        self._incrementLastIntersectionMemory()

    def doCrazySpan(self, intersection: float, amount: int):
        if self.isLastIntersection(intersection):
            diffX, diffY = random.choice(
                list(itertools.permutations(
                    [-amount, 0, amount], 2)))
            self.pos.x += diffX
            self.pos.y += diffY
        self.lastIntersection = intersection

    def fixOverlapping(self):
        self.doCrazySpan(-1.0, 1)


