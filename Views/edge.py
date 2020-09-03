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
        midPinPos: tuple = getMidPointInLine(startEdge.pos, endEdge.pos)
        self.bezierPins: List[BezierPin] = [BezierPin(Pos(*midPinPos))]
        self.id = f"({startEdge.name}, {endEdge.name})"

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str

    def __iter__(self) -> Iterator[Vertex]:
        return iter((self.start, self.end))
