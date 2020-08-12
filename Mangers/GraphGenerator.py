from typing import Tuple, List, Dict

from DataTypes.Pos import Pos
from DataTypes.GraphHolder import GraphHolder
from views import Vertex, Edge


class GraphGenerator:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.vertices: List[Vertex] = []
        self.verticesPositionsMap: Dict[int, int] = {}
        self.edges: List[Edge] = []
        self.vertices: List[Vertex] = []
        self.verticesPositionsMap: Dict[int, int] = {}
        self.edgesPositionsMap: Dict[int, int] = {}
        self.test_intersectionMap: Dict[int, List[bool]] = {}

    def generate2ComponentsGraph(self) -> GraphHolder:
        self.vertices = [Vertex(44, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(0, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-1, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(999, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-2, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-3, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-5, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-4, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-7, Pos(*map(lambda x: x // 2, self.displaySize))),
                         Vertex(-8, Pos(*map(lambda x: x // 2, self.displaySize)))]
        self.edges = [Edge(44, 999), Edge(0, 999), Edge(44, 0), Edge(-7, 0), Edge(-8, 44),
                      Edge(-2, -3), Edge(-3, -4), Edge(-4, -5), Edge(-5, -2)]
        self._updateVerticesPositionsMap()
        self._updateEdgesPositionsMap()

        graphHolder = GraphHolder(self.edges, self.vertices, self.edgesPositionsMap, self.verticesPositionsMap,
                                  self.test_intersectionMap)
        return graphHolder

    def generateVerticesCanFitIn(self, width, height, dimentsManger) -> GraphHolder:
        c, r = ((width // (dimentsManger.VerticesDiments.radius * 2)) // 2) + 1, (
                (height // (dimentsManger.VerticesDiments.radius * 2)) // 2)
        self.vertices = [Vertex(i, Pos(((i % c) * (width // c)),
                                       ((i // c) * (height // r))))
                         for i in range(c * r)]
        self._updateVerticesPositionsMap()
        graphHolder = GraphHolder(self.edges, self.vertices, self.edgesPositionsMap, self.verticesPositionsMap,
                                  self.test_intersectionMap)
        return graphHolder

    def _updateVerticesPositionsMap(self):
        self.verticesPositionsMap: Dict[int, int] = {self.vertices[i].idKey: i for i in range(len(self.vertices))}
        self.test_intersectionMap = {k: [True] * len(self.vertices) for k in self.verticesPositionsMap.keys()}
        for k in self.test_intersectionMap:
            p = self.verticesPositionsMap[k]
            self.test_intersectionMap[k][p] = False

    def _updateEdgesPositionsMap(self):
        self.edgesPositionsMap: Dict[int, int] = {self.edges[i]: i for i in range(len(self.edges))}
