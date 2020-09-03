import itertools
import random
from typing import Dict, List, Iterator, Final, Any

from DataTypes.graph_holder import GraphHolder
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from Tokens import VerticesTokens
from Views.vertex import Vertex


class VerticesManager():
    def __init__(self):
        self.selectedVertexName = None
        self._vertices: Final[List[Vertex]] = []
        self.verticesPositionsMap: Final[Dict[str, int]] = {}
        self.intersectionMap: Final[Dict[int, List[bool]]] = {}

    @property
    def vertices(self):
        return self._vertices

    def importFromGraphHolder(self, graphHolder: GraphHolder):
        self._vertices.extend(graphHolder.vertices)
        self._updateVerticesPositionsMap()

    def addVertices(self, verticesHolder: List[VertexHolder]) -> List[Vertex]:
        newVertices = [self.createVertex(vertexHolder.name, vertexHolder.pos)
                       for vertexHolder in verticesHolder]
        self._vertices.extend(newVertices)
        self._updateVerticesPositionsMap()
        return newVertices

    def byName(self, vertexName: str) -> Vertex:
        return self._vertices[self.verticesPositionsMap[str(vertexName)]]

    def isExists(self, vertexName: str) -> bool:
        return str(vertexName) in self.verticesPositionsMap

    def isSelectedVertex(self, v: Vertex) -> bool:
        if self.selectedVertexName is None: return False
        return v.name == self.selectedVertexName

    def updateSelectedVertex(self, selectedVertex: Vertex):
        self.selectedVertexName = selectedVertex.name
        selectedVertex.status = VerticesTokens.isSelected

    def clearSelectedVertex(self):
        lastSelectedVertex = self.byName(self.selectedVertexName)
        lastSelectedVertex.status = VerticesTokens.isDefault
        self.selectedVertexName = None

    def getIdOf(self, v: Vertex) -> int:
        return self.verticesPositionsMap[v.name]

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
        self.verticesPositionsMap.update({v.name: idx
                                          for idx, v in enumerate(self._vertices)})
        self._initIntersectionMap()

    @property
    def selectedVertex(self):
        return self.byName(self.selectedVertexName)

    def __getitem__(self, key) -> Vertex:
        return self._vertices[key]

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._vertices)

    def _initIntersectionMap(self):
        self.intersectionMap.update({self.getIdByName(k): [True] * len(self._vertices)
                                     for k in self.verticesPositionsMap.keys()})

        # vertex can't intersect with herself
        for key in self.verticesPositionsMap:
            self.markAsNotIntersected(self.byName(key), self.byName(key))

    def scaleVertices(self):
        for vertex in self:
            vertex.generateNewTextImage()

    @staticmethod
    def createVertex(VertexName: Any, pos: Pos = None) -> Vertex:
        if pos is None: pos = Pos(*random.choice(
            list(itertools.permutations(
                [-3, 0, 3, 1], 2))))
        return Vertex(VertexName, pos)
