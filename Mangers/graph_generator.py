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

    def addVerticesHolders(self, verticesHolders: List[VertexHolder]) -> List[Vertex]:
        newVertices = self.verticesManger.addVerticesHolders(verticesHolders)
        return newVertices

    def addEdgesHolders(self, edgesHolders: List[EdgeHolder]) -> List[Edge]:
        newEdges = self.edgesManger.addEdgesHolders(edgesHolders)
        return newEdges

    def generateTriangle(self) -> GraphHolder:
        count = len(self.verticesManger.vertices)
        self.addVerticesHolders([VertexHolder(count), VertexHolder(count + 1), VertexHolder(count + 2)])
        self.edgesManger.addEdges(
            [EdgeHolder(count, count + 1), EdgeHolder(count + 1, count + 2), EdgeHolder(count + 2, count)])
        return self.exportGraphHolder()

    def exportGraphHolder(self) -> GraphHolder:
        graphHolder = GraphHolder(self.edgesManger.edges, self.verticesManger.vertices)
        return graphHolder

    def generateRandomShape(self) -> GraphHolder:
        self.edgesManger.addEdges(
            [EdgeHolder(1, 2),
             EdgeHolder(0, 1),
             EdgeHolder(0, 2),
             EdgeHolder(2, 0),
             EdgeHolder(3, 2),
             EdgeHolder(2, 5),
             EdgeHolder(3, 4),
             EdgeHolder(4, 3),
             EdgeHolder(6, 5),
             EdgeHolder(6, 7),
             EdgeHolder(7, 8),
             EdgeHolder(8, 7),
             EdgeHolder(5, 8)])
        return self.exportGraphHolder()

    def generate2ComponentsGraph(self) -> GraphHolder:
        count = len(self.verticesManger.vertices)

        edges = [EdgeHolder(count, count + 3),
                 EdgeHolder(count, count + 1),
                 EdgeHolder(count + 1, count + 3),
                 EdgeHolder(count + 8, count + 1),
                 EdgeHolder(count + 4, count + 5),
                 EdgeHolder(count + 5, count + 7),
                 EdgeHolder(count + 6, count + 4),
                 EdgeHolder(count + 7, count + 6),
                 EdgeHolder(count + 9, count)]
        self.edgesManger.addEdges(edges)

        vertices = [
            VertexHolder(count),
            VertexHolder(count + 1),
            VertexHolder(count + 2),
            VertexHolder(count + 3),
            VertexHolder(count + 4),
            VertexHolder(count + 5),
            VertexHolder(count + 6),
            VertexHolder(count + 7),
            VertexHolder(count + 8),
            VertexHolder(count + 9)]
        self.verticesManger.addVertices(vertices)
        return self.exportGraphHolder()

    def generateVerticesCanFitIn(self, width, height, dimentsManger) -> GraphHolder:
        c, r = ((width // (dimentsManger.VerticesDiments.radius * 2)) // 2), (
                (height // (dimentsManger.VerticesDiments.radius * 2)) // 2)
        self.vertices.extend([Vertex(-i, Pos(((i % c) * (width // c)),
                                             ((i // c) * (height // r))))
                              for i in range(c * r)])
        return self.exportGraphHolder()
