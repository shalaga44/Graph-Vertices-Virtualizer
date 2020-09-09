from typing import Iterator, List

import Colors
from DataTypes.pos import Pos
from LinearMath import getMidPointInLine
from Views.bezier_pin import BezierPin
from Views.vertex import Vertex


class Edge:
    def __init__(self, startEdge: Vertex, endEdge: Vertex):
        self.start: Vertex = startEdge
        self.end: Vertex = endEdge
        self._str = f"({startEdge}, {endEdge})"
        self.color = Colors.EdgesColors.default
        self.bezierPins: List[BezierPin] = []
        self.id: str = f"({startEdge.name}, {endEdge.name})"
        self._isCarve = False

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str

    def __iter__(self) -> Iterator[Vertex]:
        return iter((self.start, self.end))

    @property
    def midPoint(self) -> Pos:
        return Pos(*getMidPointInLine(self.start.pos, self.end.pos))

    @property
    def isCarve(self) -> bool:
        return self._isCarve

    @isCarve.setter
    def isCarve(self, value: bool):
        if value:
            self.color = Colors.EdgesColors.isCarve
        else:
            self.color = Colors.EdgesColors.default
        self._isCarve = value
