from math import sqrt

from DataTypes.pos import Pos
from Views.edge import Edge
from Views.vertex import Vertex
from typing import Union


def isVerticesIntersecting(v: Vertex, u: Vertex, radius: int) -> Union[int, bool]:
    intersection = getCirclesIntersection(v.pos.x, v.pos.y, u.pos.x, u.pos.y, radius, radius)
    if intersection < 0:
        return intersection
    return False


def getVerticesIntersection(v: Vertex, u: Vertex, radius: int) -> int:
    intersection = getCirclesIntersection(v.pos.x, v.pos.y, u.pos.x, u.pos.y, radius, radius)
    return intersection


def isPointInCircle(pX: int, pY: int, cX: int, cY: int, r: int) -> bool:
    d = sqrt((abs(pX - cX) ** 2) + (abs(pY - cY) ** 2))
    if d <= r: return True
    return False


def getCirclesIntersection(x1: int, y1: int, x2: int, y2: int, r1: int, r2: int) -> int:
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    radSumSq = (r1 + r2) * (r1 + r2)
    intersection = distSq - radSumSq
    return intersection


def getDistanceBetween2Points(x1: int, y1: int, x2: int, y2: int) -> float:
    distance = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
    return distance


def getDistanceBetween2Pos(pos1: Pos, pos2: Pos) -> float:
    # distance = getDistanceBetween2Points(pos1.x, pos2.x, pos1.y, pos2.y)
    # Not the same @_@ . I Don't Know why
    distance = sqrt(pow((pos1.x - pos2.x), 2) + pow((pos1.y - pos2.y), 2))
    return distance


def getDistanceBetween2Vertices(vertex1: Vertex, vertex2: Vertex) -> float:
    # distance = getDistanceBetween2Pos(vertex1.pos, vertex2.pos)
    # Not the same @_@ . I Don't Know why
    distance = sqrt(pow((vertex1.pos.x - vertex2.pos.x), 2) + pow((vertex1.pos.y - vertex2.pos.y), 2))
    return distance
