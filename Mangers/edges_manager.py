from typing import Dict, List, Iterator, Final

from DataTypes.edge_holder import EdgeHolder
from DataTypes.graph_holder import GraphHolder
from DataTypes.vertex_holder import VertexHolder
from LinearMath import getDistanceBetween2Vertices
from Mangers.vertices_manager import VerticesManager
from Views.edge import Edge


class EdgesManager:
    def __init__(self, globalVerticesManager: VerticesManager):
        self.edges: Final[List[Edge]] = []
        self.edgesPositionsMap: Final[Dict[int, int]] = {}
        self.edgesMap: Final[Dict[str, Edge]] = {}
        self._verticesManager: VerticesManager = VerticesManager()
        self.globalVerticesManager: VerticesManager = globalVerticesManager
        self._updateMaps()

    def addEdgesHolders(self, edgeHolders: List[EdgeHolder]) -> List[Edge]:
        finalEdges = []
        newEdges: List[Edge] = []
        for edgeHolder in edgeHolders:
            if self.isExist(edgeHolder):
                oldEdge = self.byId(edgeHolder.id)
                finalEdges.append(oldEdge)
                newEdges.append(oldEdge)
            else:
                newEdge = self._createEdge(edgeHolder)
                newEdges.append(newEdge)
                finalEdges.append(newEdge)
        self._addNewEdges(newEdges)
        return finalEdges

    def _addNewEdges(self, edges: List[Edge]):
        self.edges.extend(edges)
        self._updateMaps()
        self._updateVerticesManager(edges)

    def length(self, edge: Edge):
        start = self.globalVerticesManager.byName(edge.start.name)
        end = self.globalVerticesManager.byName(edge.end.name)
        return getDistanceBetween2Vertices(start, end)

    def _createEdge(self, edgeHolder: EdgeHolder) -> Edge:
        start, end = self.globalVerticesManager.addVerticesHolders([VertexHolder(edgeHolder.start),
                                                                    VertexHolder(edgeHolder.end)])
        return Edge(start, end)

    def importFromGraphHolder(self, graphHolder: GraphHolder):
        self.edges.extend(graphHolder.edges)
        self._updateMaps()

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

    def isExist(self, edgeHolder: EdgeHolder) -> bool:
        if edgeHolder.id in self.edgesMap:
            return True
        return False

    def byId(self, edgeId: str) -> Edge:
        return self.edgesMap[edgeId]

    def _updateEdgesMap(self):
        self.edgesMap.update({e.id: e for e in self.edges})

    def _updateMaps(self):
        self._updateEdgesPositionsMap()
        self._updateEdgesMap()
