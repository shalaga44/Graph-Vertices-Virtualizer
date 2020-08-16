from typing import List, Tuple, Dict, Optional

from DataTypes.Pos import Pos
from DataTypes.GraphHolder import GraphHolder
from LinearMath import getVerticesIntersection, isVerticesIntersecting, isPointInCircle, getDistanceBetween2Vertices
from Mangers.DimensionsManger import DimensionsManger
from Mangers.GraphGenerator import GraphGenerator
from Mangers.VerticesManager import VerticesManger
from SingletonMetaClass import Singleton
from Views.VertexClass import Vertex
from Views.EdgeClass import Edge


class GraphManager():
    def __init__(self, width, height):

        self.edges: List[Edge] = []
        self.verticesManger: VerticesManger = VerticesManger()
        self.edgesPositionsMap: Dict[int, int] = {}
        self.verticesPositionsMap: Dict[int, int] = {}

        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.displaySizeHalf: Tuple[int, ...] = (width // 2, height // 2)

        self.isVerticesSetupModeDisabled = False
        self.isEdgesSetupModeDisabled = False
        self._isCrazySpanningModeDisabled = False

        self._isCrazySpanningMode = True
        self.isSelectingVertexMode = False
        self.noVerticesIntersecting = False

        self.dimentsManger = DimensionsManger()

        self.graphGenerator = GraphGenerator(*self.displaySize)
        self.graphGenerator.generate2ComponentsGraph()

    @property
    def isCrazySpanningMode(self) -> Optional[bool]:
        return None if self._isCrazySpanningModeDisabled \
            else self._isCrazySpanningMode

    @isCrazySpanningMode.setter
    def isCrazySpanningMode(self, b: bool):
        self._isCrazySpanningMode = b

    @property
    def vertices(self):
        return self.verticesManger.vertices

    def setupFromGraphHolder(self, graphHolder: GraphHolder):
        self.verticesManger.takeFromGraphHolder(graphHolder)
        self.edges = graphHolder.edges
        self.edgesPositionsMap = graphHolder.edgesPositionsMap

    def setupVertices(self):
        if self.isVerticesSetupModeDisabled: return
        allStopped = True
        for vertex in self.verticesManger:
            if vertex.isMoved or 1:
                self._moveVerticesAwayFrom(vertex)
                self._alignVertexOnScreen(vertex)
            if self.isVertexNotIntersected(vertex):
                vertex.isMoved = False
            else:
                allStopped = False
        if allStopped:
            self.noVerticesIntersecting = True
            self.isCrazySpanningMode = False

    def setupEdges(self):
        if self.isEdgesSetupModeDisabled: return
        allStopped = True
        for edge in self.edges:
            self._limitVerticesOfEdge(edge)
            if not self.isVertexNotIntersected(self.verticesManger.byName(edge.start)):
                if not self.isVertexNotIntersected(self.verticesManger.byName(edge.end)):
                    allStopped = False
        if allStopped:
            self.noVerticesIntersecting = True
            self.isCrazySpanningMode = False

    def _limitVerticesOfEdge(self, edge: Edge):
        if self.isEdgesSetupModeDisabled: return
        start: Vertex = self.verticesManger.byName(edge.start)
        end: Vertex = self.verticesManger.byName(edge.end)
        distance = round(getDistanceBetween2Vertices(start, end), 2)
        if distance > self.dimentsManger.EdgesDiments.length:
            amountOfMovement = round((distance / self.dimentsManger.EdgesDiments.length) / 10, 1)

            if self.isSelectingVertexMode:
                if self.isSelectedVertex(start):
                    end.moveCloserTo(start.pos, amountOfMovement)
                    self._alignVertexOnScreen(end)
                else:
                    start.moveCloserTo(end.pos, amountOfMovement)
                    self._alignVertexOnScreen(start)

            else:
                end.moveCloserTo(start.pos, amountOfMovement)
                start.moveCloserTo(end.pos, amountOfMovement)
                self._alignVertexOnScreen(start)
                self._alignVertexOnScreen(end)

            self.verticesManger.markAsIntersected(start, end)
        else:
            self.verticesManger.markAsNotIntersected(start, end)

    def _alignVertexOnScreen(self, vertex):
        r = self.dimentsManger.VerticesDiments.radius
        if vertex.pos.x - r < 0: vertex.pos.x = 0 + r
        if vertex.pos.x + r > self.width: vertex.pos.x = self.width - r
        if vertex.pos.y - r < 0: vertex.pos.y = 0 + r
        if vertex.pos.y + r > self.height: vertex.pos.y = self.height - r

    def _moveVerticesAwayFrom(self, fixedVertex: Vertex):
        if self.isVerticesSetupModeDisabled: return
        radius = self.dimentsManger.VerticesDiments.intersectionRadius
        for vertex in self.verticesManger:
            if fixedVertex == vertex: continue
            if not self.isSelectedVertex(vertex):
                intersection = isVerticesIntersecting(fixedVertex, vertex, radius)
                if intersection:
                    self.doCrazySpanningIfPossible(vertex, intersection)
                    vertex.moveAwayFrom(fixedVertex.pos, self.normalizedDistanceOf(intersection))
                    self._alignVertexOnScreen(vertex)
                    self.verticesManger.markAsIntersected(vertex, fixedVertex)

                else:
                    self.verticesManger.markAsNotIntersected(vertex, fixedVertex)

    def isSelectedVertex(self, v: Vertex) -> bool:
        if self.isSelectingVertexMode:
            return self.verticesManger.isSelectedVertex(v)
        return False

    def moveSelectedVertexTo(self, x: int, y: int):
        try:
            selectedVertex = self.verticesManger.selectedVertex
        except KeyError:
            return
        selectedVertex.pos.x = x
        selectedVertex.pos.y = y
        self._moveVerticesAwayFrom(selectedVertex)

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

    def isVertexNotIntersected(self, v: Vertex):
        return self.verticesManger.isVertexNotIntersected(v)

    def toggleCrazySpanning(self):
        self.isCrazySpanningMode = True if not self.isCrazySpanningMode \
            else False

    def startCrazySpanning(self):
        self.isCrazySpanningMode = True

    def scaleVertices(self):
        self.verticesManger.scaleVertices()
        self.startCrazySpanning()

    def doCrazySpanningIfPossible(self, v: Vertex, intersection: float):
        if self.isCrazySpanningMode:
            v.doCrazySpan(intersection, self.dimentsManger.EdgesDiments.length)

    def toggleVerticesSetupMode(self):
        self.isVerticesSetupModeDisabled = False if self.isVerticesSetupModeDisabled \
            else True

    def toggleEdgesSetupMode(self):
        self.isEdgesSetupModeDisabled = False if self.isEdgesSetupModeDisabled \
            else True

    def normalizedDistanceOf(self, intersection) -> float:
        return round(intersection /
                     ((self.dimentsManger.scaleFactor * self.dimentsManger.scaleFactor) * 10000),
                     2)
