from math import sqrt

from views import Vertex
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
