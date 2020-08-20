from typing import Tuple, List, Final

from DataTypes.edge_holder import EdgeHolder
from DataTypes.graph_holder import GraphHolder
from DataTypes.pos import Pos
from Views.vertex import Vertex


class GraphGenerator:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.vertices: Final[List[Vertex]] = []
        self.edges: Final[List[EdgeHolder]] = []

    def clearAll(self):
        self.clearEdges()
        self.clearVertices()

    def clearVertices(self):
        self.vertices.clear()

    def clearEdges(self):
        self.edges.clear()

    def generateTriangle(self) -> GraphHolder:
        self.vertices.extend([Vertex(3, Pos(20, 20)), Vertex(4, Pos(50, 50)), Vertex(5, Pos(80, 80))])
        self.edges.extend([EdgeHolder(3, 4), EdgeHolder(4, 5), EdgeHolder(5, 3)])
        return self.exportGraphHolder()

    def exportGraphHolder(self) -> GraphHolder:
        graphHolder = GraphHolder(self.edges, self.vertices)
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
        self.edges.extend(
            [EdgeHolder(44, 999), EdgeHolder(0, 999), EdgeHolder(44, 0), EdgeHolder(-7, 0), EdgeHolder(-8, 44),
             EdgeHolder(-2, -3), EdgeHolder(-3, -4), EdgeHolder(-4, -5), EdgeHolder(-5, -2)])
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
        self.verticesPositionsMap.update({self.vertices[i].name: i for i in range(len(self.vertices))})
