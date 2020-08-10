import itertools
import random
from typing import List, Tuple, Dict, Optional

from DataTypes import Pos
# from Dimensions import VerticesDiments, EdgesDiments, MainDiments
from Dimensions import MainDiments
from LinearMath import getVerticesIntersection, isVerticesIntersecting, isPointInCircle
from SingletonMetaClass import Singleton
from Tokens import VerticesTokens
from views import Vertex, Edge


class GraphManager(metaclass=Singleton):
    def __init__(self, width, height):
        self.edges: List[Edge] = []
        self.vertices: List[Vertex] = []

        self.edgesPositionsMap: Dict[int:int] = {}
        self.verticesPositionsMap: Dict[int:int] = {}

        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.displaySizeHalf: Tuple[int, ...] = (width // 2, height // 2)

        self.selectedVertexId = 0
        self.isCrazySpanningMode = True
        self.isSelectingVertexMode = False
        self.test_intersectionMap: Dict[int:List[bool]] = {}
        self.dimentsManger = DimensionsManger()

    def generate2ComponentsGraph(self):
        self.vertices = [Vertex(44, Pos(*self.displaySizeHalf)), Vertex(0, Pos(*self.displaySizeHalf)),
                         Vertex(-1, Pos(*self.displaySizeHalf)), Vertex(999, Pos(*self.displaySizeHalf)),
                         Vertex(-2, Pos(*self.displaySizeHalf)), Vertex(-3, Pos(*self.displaySizeHalf)),
                         Vertex(-5, Pos(*self.displaySizeHalf)), Vertex(-4, Pos(*self.displaySizeHalf)),
                         Vertex(-7, Pos(*self.displaySizeHalf)), Vertex(-8, Pos(*self.displaySizeHalf))]
        self.edges = [Edge(44, 999), Edge(0, 999), Edge(44, 0), Edge(-7, 0), Edge(-8, 44),
                      Edge(-2, -3), Edge(-3, -4), Edge(-4, -5), Edge(-5, -2)]
        self._updateVerticesPositionsMap()
        self._updateEdgesPositionsMap()

    def generateVerticesCanFitIn(self, width, height):
        c, r = ((width // (self.dimentsManger.VerticesDiments.radius * 2)) // 2) + 1, (
                (height // (self.dimentsManger.VerticesDiments.radius * 2)) // 2)
        self.vertices = [Vertex(i, Pos(((i % c) * (width // c)),
                                       ((i // c) * (height // r))))
                         for i in range(c * r)]
        self._updateVerticesPositionsMap()

    def _updateVerticesPositionsMap(self):
        self.verticesPositionsMap: dict[int:int] = {self.vertices[i].idKey: i for i in range(len(self.vertices))}
        self.test_intersectionMap = {k: [True] * len(self.vertices) for k in self.verticesPositionsMap.keys()}
        for k in self.test_intersectionMap:
            p = self.verticesPositionsMap[k]
            self.test_intersectionMap[k][p] = False

    def _updateEdgesPositionsMap(self):
        self.edgesPositionsMap: dict[int:int] = {self.edges[i]: i for i in range(len(self.edges))}

    def setupEdges(self):
        for edge in self.edges:
            self._limitVerticesOfEdge(edge)

    def _limitVerticesOfEdge(self, edge):
        start: Vertex = self.vertices[self.verticesPositionsMap[edge.start]]
        end: Vertex = self.vertices[self.verticesPositionsMap[edge.end]]
        intersection = getVerticesIntersection(start, end, self.dimentsManger.EdgesDiments.length)
        if intersection > 0:
            end.moveCloserTo(start, intersection)
            start.moveCloserTo(end, intersection)
            self._alignVertexOnScreen(end)
            self._alignVertexOnScreen(start)
            self.markAsIntersected(start, end)

        else:
            # pass
            self.markAsNotIntersected(start, end)
            # start.isMoved = False
            # end.isMoved = False

    def _alignVertexOnScreen(self, vertex):
        r = self.dimentsManger.VerticesDiments.radius
        if vertex.pos.x - r < 0: vertex.pos.x = 0 + r
        if vertex.pos.x + r > self.width: vertex.pos.x = self.width - r
        if vertex.pos.y - r < 0: vertex.pos.y = 0 + r
        if vertex.pos.y + r > self.height: vertex.pos.y = self.height - r

    def setupVertices(self):
        allStopped = True
        for vertex in self.vertices:
            if vertex.isMoved:
                self._separateFromOtherVertices(vertex)
                self._alignVertexOnScreen(vertex)
            if self.isVertexNotIntersected(vertex):
                vertex.isMoved = False
            else:
                allStopped = False
        if allStopped:
            self.isCrazySpanningMode = False

    def _separateFromOtherVertices(self, vertex):
        # isIntersected = False
        for u in self.vertices:
            if vertex == u: continue
            if not self.isSelectedVertex(u):
                intersection = isVerticesIntersecting(vertex, u, self.dimentsManger.VerticesDiments.intersectionRadius)
                if intersection:
                    self.moveVertexAwayVertex(u, vertex, intersection)
                    self.markAsIntersected(u, vertex)
                else:
                    self.markAsNotIntersected(u, vertex)
                    # isIntersected = True
        # if not isIntersected:
        # vertex.isMoved = False

    def isSelectedVertex(self, v: Vertex) -> bool:
        if self.isSelectingVertexMode:
            return self.verticesPositionsMap[v.idKey] == self.selectedVertexId
        return False

    def moveSelectedVertexTo(self, x: int, y: int):
        selectedVertex = self.vertices[self.selectedVertexId]
        selectedVertex.pos.x = x
        selectedVertex.pos.y = y
        for u in self.vertices:
            if selectedVertex == u: continue
            intersection = isVerticesIntersecting(selectedVertex, u,
                                                  self.dimentsManger.VerticesDiments.intersectionRadius)
            if intersection:
                self.moveVertexAwayVertex(u, selectedVertex, intersection)
                self.markAsIntersected(u, selectedVertex)
            else:
                self.markAsNotIntersected(u, selectedVertex)

    def updateSelectedVertex(self, vertex: Vertex):
        self.selectedVertexId = self.verticesPositionsMap[vertex.idKey]
        vertex.status = VerticesTokens.isSelected
        self.isSelectingVertexMode = True

    def getClickedVertexAt(self, p: Pos) -> Optional[Vertex]:
        r = self.dimentsManger.VerticesDiments.radius
        for c in self.vertices:
            if isPointInCircle(p.x, p.y, c.pos.x, c.pos.y, r):
                return c
        return None

    def startVertexSelectingMode(self, mousePos: Pos):
        if self.isSelectingVertexMode:
            self.stopVertexSelectingMode()
            return

        vertex = self.getClickedVertexAt(mousePos)
        if vertex is None: return

        self.updateSelectedVertex(vertex)

    def stopVertexSelectingMode(self):
        vertex = self.vertices[self.selectedVertexId]
        vertex.status = VerticesTokens.isDefault
        self.isSelectingVertexMode = False

    def moveVertexAwayVertex(self, v: Vertex, u: Vertex, intersection):
        if self.isCrazySpanningMode:
            self.fixVertexSameIntersection(v, intersection)

        diffX = u.pos.x - v.pos.x
        diffY = u.pos.y - v.pos.y
        v.pos.x += diffX * intersection / 10000
        v.pos.y += diffY * intersection / 10000
        v.isMoved = True

    def fixVertexSameIntersection(self, v: Vertex, intersection):
        if intersection == v.lastIntersection:
            diffX, diffY = random.choice(
                list(itertools.permutations(
                    [-self.dimentsManger.EdgesDiments.length, 0, self.dimentsManger.EdgesDiments.length], 2)))
            v.pos.x += diffX
            v.pos.y += diffY
        v.lastIntersection = intersection

    def isVertexNotIntersected(self, v: Vertex):
        return not any(self.test_intersectionMap[v.idKey])

    def markAsIntersected(self, v: Vertex, u: Vertex):
        self.test_intersectionMap[v.idKey][self.verticesPositionsMap[u.idKey]] = True
        self.test_intersectionMap[u.idKey][self.verticesPositionsMap[v.idKey]] = True

    def markAsNotIntersected(self, v: Vertex, u: Vertex):
        self.test_intersectionMap[v.idKey][self.verticesPositionsMap[u.idKey]] = False
        self.test_intersectionMap[u.idKey][self.verticesPositionsMap[v.idKey]] = False

    def startCrazySpanning(self):
        if self.isCrazySpanningMode:
            self.isCrazySpanningMode = False
        else:
            self.isCrazySpanningMode = True


class DimensionsManger(metaclass=Singleton):
    def __init__(self):
        self.isChanged = False
        self._scaleFactor = MainDiments.scaleFactor = .9
        self.updateScales()

    @property
    def scaleFactor(self):
        return self._scaleFactor

    @scaleFactor.setter
    def scaleFactor(self, a):
        self._scaleFactor = a
        self.updateScales()

    class VerticesDiments:
        radius: int
        fontSize: int
        intersectionRadius: int

    class EdgesDiments:
        width: int
        length: int

    def updateScales(self):
        self.VerticesDiments.radius = int(25 * self.scaleFactor)
        self.VerticesDiments.fontSize = int(30 * self.scaleFactor)
        self.VerticesDiments.intersectionRadius = self.VerticesDiments.radius * 2
        self.EdgesDiments.width = int(5 * self.scaleFactor)
        self.EdgesDiments.length = self.VerticesDiments.radius * 3
