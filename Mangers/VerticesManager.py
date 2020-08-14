from typing import Dict, List, Iterator, Final

from DataTypes.GraphHolder import GraphHolder
from SingletonMetaClass import Singleton
from Tokens import VerticesTokens
from views import Vertex


class VerticesManger(metaclass=Singleton):
    def __init__(self):
        self.selectedVertexName = None
        self.vertices: Final[List[Vertex]] = []
        self.verticesPositionsMap: Final[Dict[str, int]] = {}
        self.intersectionMap: Final[Dict[int, List[bool]]] = {}

    def takeFromGraphHolder(self, graphHolder: GraphHolder):
        self.vertices.extend(graphHolder.vertices)
        self._updateVerticesPositionsMap()

    def byName(self, vertexName: str) -> Vertex:
        return self.vertices[self.verticesPositionsMap[str(vertexName)]]

    def isSelectedVertex(self, v: Vertex) -> bool:
        if self.selectedVertexName is None: return False
        return v.vertexName == self.selectedVertexName

    def updateSelectedVertex(self, selectedVertex: Vertex):
        self.selectedVertexName = selectedVertex.vertexName
        selectedVertex.status = VerticesTokens.isSelected

    def clearSelectedVertex(self):
        lastSelectedVertex = self.byName(self.selectedVertexName)
        lastSelectedVertex.status = VerticesTokens.isDefault
        self.selectedVertexName = None

    def getIdOf(self, v: Vertex) -> int:
        return self.verticesPositionsMap[v.vertexName]

    def getIdByName(self, vertexName: str) -> int:
        return self.verticesPositionsMap[vertexName]

    def isVertexNotIntersected(self, v: Vertex):
        return not any(self.intersectionMap[self.getIdOf(v)])

    def markAsIntersected(self, v: Vertex, u: Vertex):
        self._markIntersection(v, u, True)
        v.isMoved = True
        u.isMoved = True

    def markAsNotIntersected(self, v: Vertex, u: Vertex):
        self._markIntersection(v, u, False)

    def _markIntersection(self, v: Vertex, u: Vertex, status: bool):
        self.intersectionMap[self.getIdOf(v)][self.getIdOf(u)] = status
        self.intersectionMap[self.getIdOf(u)][self.getIdOf(v)] = status

    def _updateVerticesPositionsMap(self):
        self.verticesPositionsMap.update({v.vertexName: idx
                                          for idx, v in enumerate(self.vertices)})
        self._initIntersectionMap()

    @property
    def selectedVertex(self):
        return self.byName(self.selectedVertexName)

    def __getitem__(self, key) -> Vertex:
        return self.vertices[key]

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self.vertices)

    def _initIntersectionMap(self):
        self.intersectionMap.update({self.getIdByName(k): [True] * len(self.vertices)
                                     for k in self.verticesPositionsMap.keys()})

        # vertex can't intersect with herself
        for key in self.verticesPositionsMap:
            self.markAsNotIntersected(self.byName(key), self.byName(key))

    def scaleVertices(self):
        for vertex in self:
            vertex.generateNewTextImage()
