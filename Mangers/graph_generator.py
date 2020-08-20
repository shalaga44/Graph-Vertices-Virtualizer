from typing import Tuple, List, Final

from DataTypes.edge_holder import EdgeHolder
from DataTypes.graph_holder import GraphHolder
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from Mangers.edges_manager import EdgesManager
from Mangers.vertices_manager import VerticesManager
from Views.edge import Edge
from Views.vertex import Vertex


class GraphGenerator:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.displaySize: Tuple[int, ...] = (width, height)
        self.vertices: Final[List[Vertex]] = []
        self.edges: Final[List[Edge]] = []
        self.verticesManger: Final[VerticesManager] = VerticesManager()
        self.edgesManger: Final[EdgesManager] = EdgesManager(self.verticesManger)

    def clearAll(self):
        self.clearEdges()
        self.clearVertices()

    def clearVertices(self):
        self.vertices.clear()

    def clearEdges(self):
        self.edges.clear()

    def generateTriangle(self) -> GraphHolder:
        self.verticesManger.addVertices([VertexHolder(3), VertexHolder(4), VertexHolder(5)])
        self.edgesManger.addEdges([EdgeHolder(3, 4), EdgeHolder(4, 5), EdgeHolder(5, 3)])
        return self.exportGraphHolder()

    def exportGraphHolder(self) -> GraphHolder:
        graphHolder = GraphHolder(self.edgesManger.edges, self.verticesManger.vertices)
        return graphHolder

    def generate2ComponentsGraph(self) -> GraphHolder:
        edges = [EdgeHolder(44, 999), EdgeHolder(0, 999), EdgeHolder(44, 0), EdgeHolder(-7, 0), EdgeHolder(-8, 44),
                 EdgeHolder(-2, -3), EdgeHolder(-3, -4), EdgeHolder(-4, -5), EdgeHolder(-5, -2)]
        self.edgesManger.addEdges(edges)

        vertices = [
            VertexHolder(44),
            VertexHolder(0),
            VertexHolder(-1),
            VertexHolder(999),
            VertexHolder(-2),
            VertexHolder(-3),
            VertexHolder(-5),
            VertexHolder(-4),
            VertexHolder(-7),
            VertexHolder(-8)]
        self.verticesManger.addVertices(vertices)

        return self.exportGraphHolder()

    def generateVerticesCanFitIn(self, width, height, dimentsManger) -> GraphHolder:
        c, r = ((width // (dimentsManger.VerticesDiments.radius * 2)) // 2), (
                (height // (dimentsManger.VerticesDiments.radius * 2)) // 2)
        self.vertices.extend([Vertex(i, Pos(((i % c) * (width // c)),
                                            ((i // c) * (height // r))))
                              for i in range(c * r)])
        return self.exportGraphHolder()
