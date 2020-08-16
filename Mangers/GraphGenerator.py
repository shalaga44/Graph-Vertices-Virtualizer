from typing import Tuple, List, Dict, Final

from DataTypes.Pos import Pos
from DataTypes.GraphHolder import GraphHolder
from Views.VertexClass import Vertex
from Views.EdgeClass import Edge


class GraphGenerator:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.vertices: Final[List[Vertex]] = []
        self.verticesPositionsMap: Final[Dict[str, int]] = {}
        self.edges: Final[List[Edge]] = []
        self.edgesPositionsMap: Final[Dict[int, int]] = {}

    def clearAll(self):
        self.clearEdges()
        self.clearVertices()

    def clearVertices(self):
        self.vertices.clear()

    def clearEdges(self):
        self.edges.clear()

    def generateTriangle(self) -> GraphHolder:
        self.vertices.extend([Vertex(3, Pos(20, 20)), Vertex(4, Pos(50, 50)), Vertex(5, Pos(80, 80))])
        self.edges.extend([Edge(3, 4), Edge(4, 5), Edge(5, 3)])
        return self.exportGraphHolder()

    def exportGraphHolder(self) -> GraphHolder:
        self._updateVerticesPositionsMap()
        self._updateEdgesPositionsMap()
        graphHolder = GraphHolder(self.edges, self.vertices, self.edgesPositionsMap)
        return graphHolder

    def generate2ComponentsGraph(self) -> GraphHolder:
        self.vertices.extend([Vertex(44, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(0, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-1, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(999, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-2, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-3, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-5, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-4, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-7, Pos(*map(lambda x: x // 2, self.displaySize))),
                              Vertex(-8, Pos(*map(lambda x: x // 2, self.displaySize)))])
        self.edges.extend([Edge(44, 999), Edge(0, 999), Edge(44, 0), Edge(-7, 0), Edge(-8, 44),
                           Edge(-2, -3), Edge(-3, -4), Edge(-4, -5), Edge(-5, -2)])
        return self.exportGraphHolder()

    def generateVerticesCanFitIn(self, width, height, dimentsManger) -> GraphHolder:
        c, r = ((width // (dimentsManger.VerticesDiments.radius * 2)) // 2), (
                (height // (dimentsManger.VerticesDiments.radius * 2)) // 2)
        self.vertices.extend([Vertex(i, Pos(((i % c) * (width // c)),
                                            ((i // c) * (height // r))))
                              for i in range(c * r)])
        self._updateVerticesPositionsMap()
        return self.exportGraphHolder()

    def _updateVerticesPositionsMap(self):
        self.verticesPositionsMap.update({self.vertices[i].vertexName: i for i in range(len(self.vertices))})

    def _updateEdgesPositionsMap(self):
        self.edgesPositionsMap.update({self.edges[i]: i for i in range(len(self.edges))})
