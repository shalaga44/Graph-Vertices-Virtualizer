from typing import Dict, List, Iterator, Final

from DataTypes.GraphHolder import GraphHolder
from SingletonMetaClass import Singleton
from Views.EdgeClass import Edge


class EdgesManger(metaclass=Singleton):
    def __init__(self):
        self.edges: Final[List[Edge]] = []
        self.edgesPositionsMap: Final[Dict[int, int]] = {}

    def importFromGraphHolder(self, graphHolder: GraphHolder):
        self.edges.extend(graphHolder.edges)
        self._updateEdgesPositionsMap()

    def _updateEdgesPositionsMap(self):
        self.edgesPositionsMap.update({self.edges[i]: i for i in range(len(self.edges))})

    def __getitem__(self, key) -> Edge:
        return self.edges[key]

    def __iter__(self) -> Iterator[Edge]:
        return iter(self.edges)
