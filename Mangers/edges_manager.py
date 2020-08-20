from typing import Dict, List, Iterator, Final

from DataTypes.edge_holder import EdgeHolder
from DataTypes.graph_holder import GraphHolder
from LinearMath import getDistanceBetween2Vertices
from Mangers.vertices_manager import VerticesManager
from Views.edge import Edge


class EdgesManager:
    def __init__(self, globalVerticesManager: VerticesManager):
        self.edges: Final[List[Edge]] = []
        self.edgesPositionsMap: Final[Dict[int, int]] = {}
        self._verticesManager: VerticesManager = VerticesManager()
        self.globalVerticesManager: VerticesManager = globalVerticesManager

    def addEdges(self, edgesHolders: List[EdgeHolder]):
        newEdges = self._createEdges(edgesHolders)
        self.edges.extend(newEdges)
        self._updateVerticesManager(newEdges)
        self._updateEdgesPositionsMap()

    def length(self, edge: Edge):
        start = self.globalVerticesManager.byName(edge.start.name)
        end = self.globalVerticesManager.byName(edge.end.name)
        return getDistanceBetween2Vertices(start, end)

    def _createEdge(self, edgesHolders: EdgeHolder) -> Edge:
        start = self._verticesManager.createVertex(edgesHolders.start)
        end = self._verticesManager.createVertex(edgesHolders.end)
        return Edge(start, end)

    def importFromGraphHolder(self, graphHolder: GraphHolder):
        self.edges.extend(graphHolder.edges)
        self._updateEdgesPositionsMap()

    def _updateEdgesPositionsMap(self):
        self.edgesPositionsMap.update({self.edges[i]: i for i in range(len(self.edges))})

    def __getitem__(self, key) -> Edge:
        return self.edges[key]

    def __iter__(self) -> Iterator[Edge]:
        return iter(self.edges)

    def _createEdges(self, edgesHolders: List[EdgeHolder]) -> List[Edge]:
        return [self._createEdge(edgeHolder)
                for edgeHolder in edgesHolders]

    def _updateVerticesManager(self, edges: List[Edge]):
        for start, end in edges:
            self._verticesManager.vertices.extend([start, end])
