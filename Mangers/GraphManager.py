import itertools
import random
from typing import List, Tuple, Dict, Optional

from DataTypes.Pos import Pos
# from Dimensions import VerticesDiments, EdgesDiments, MainDiments
from DataTypes.GraphHolder import GraphHolder
from LinearMath import getVerticesIntersection, isVerticesIntersecting, isPointInCircle
from Mangers.DimensionsManger import DimensionsManger
from Mangers.GraphGenerator import GraphGenerator
from Mangers.VerticesManager import VerticesManger
from SingletonMetaClass import Singleton
from views import Vertex, Edge


class GraphManager(metaclass=Singleton):
    def __init__(self, width, height):
        self.edges: List[Edge] = []
        self.verticesManger: VerticesManger = VerticesManger()
        self.edgesPositionsMap: Dict[int, int] = {}
        self.verticesPositionsMap: Dict[int, int] = {}

        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.displaySizeHalf: Tuple[int, ...] = (width // 2, height // 2)

        self.isCrazySpanningMode = True
        self.isSelectingVertexMode = False
        self.dimentsManger = DimensionsManger()

        self.graphGenerator = GraphGenerator(*self.displaySize)
        self.graphGenerator.generate2ComponentsGraph()

    @property
    def vertices(self):
        return self.verticesManger.vertices

    def setupFromGraphHolder(self, graphHolder: GraphHolder):
        self.verticesManger.takeFromGraphHolder(graphHolder)
        self.edges = graphHolder.edges
        self.edgesPositionsMap = graphHolder.edgesPositionsMap

    def setupEdges(self):
        for edge in self.edges:
            self._limitVerticesOfEdge(edge)

    def _limitVerticesOfEdge(self, edge: Edge):
        start: Vertex = self.verticesManger.byName(edge.start)
        end: Vertex = self.verticesManger.byName(edge.end)
        intersection = getVerticesIntersection(start, end, self.dimentsManger.EdgesDiments.length)
        if intersection > 0:
            end.moveCloserTo(start, intersection)
            start.moveCloserTo(end, intersection)
            self._alignVertexOnScreen(end)
            self._alignVertexOnScreen(start)
            self.verticesManger.markAsIntersected(start, end)

        else:
            # pass
            self.verticesManger.markAsNotIntersected(start, end)
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
        for vertex in self.verticesManger:
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
        for u in self.verticesManger:
            if vertex == u: continue
            if not self.isSelectedVertex(u):
                intersection = isVerticesIntersecting(vertex, u, self.dimentsManger.VerticesDiments.intersectionRadius)
                if intersection:
                    self.moveVertexAwayVertex(u, vertex, intersection)
                    self.verticesManger.markAsIntersected(u, vertex)
                else:
                    self.verticesManger.markAsNotIntersected(u, vertex)
                    # isIntersected = True
        # if not isIntersected:
        # vertex.isMoved = False

    def isSelectedVertex(self, v: Vertex) -> bool:
        if self.isSelectingVertexMode:
            return self.verticesManger.isSelectedVertex(v)
        return False

    def moveSelectedVertexTo(self, x: int, y: int):
        selectedVertex = self.verticesManger.selectedVertex
        selectedVertex.pos.x = x
        selectedVertex.pos.y = y
        for u in self.verticesManger:
            if selectedVertex == u: continue
            intersection = isVerticesIntersecting(selectedVertex, u,
                                                  self.dimentsManger.VerticesDiments.intersectionRadius)
            if intersection:
                self.moveVertexAwayVertex(u, selectedVertex, intersection)
                self.verticesManger.markAsIntersected(u, selectedVertex)
            else:
                self.verticesManger.markAsNotIntersected(u, selectedVertex)

    def updateSelectedVertex(self, vertex: Vertex):
        self.verticesManger.updateSelectedVertex(vertex)
        self.isSelectingVertexMode = True

    def getClickedVertexAt(self, p: Pos) -> Optional[Vertex]:
        r = self.dimentsManger.VerticesDiments.radius
        for c in self.verticesManger:
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
        self.verticesManger.clearSelectedVertex()
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
        return self.verticesManger.isVertexNotIntersected(v)

    def startCrazySpanning(self):
        if self.isCrazySpanningMode:
            self.isCrazySpanningMode = False
        else:
            self.isCrazySpanningMode = True
