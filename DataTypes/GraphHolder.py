from typing import Dict, List

from views import Vertex, Edge


class GraphHolder:
    def __init__(self, edges: List[Edge], vertices: List[Vertex], edgesPositionsMap: Dict[int,  int],
                 verticesPositionsMap: Dict[int,  int], test_intersectionMap: Dict[int,  List[bool]]):
        self.edges: List[Edge] = edges
        self.vertices: List[Vertex] = vertices

        self.edgesPositionsMap: Dict[int,  int] = edgesPositionsMap
        self.verticesPositionsMap: Dict[int,  int] = verticesPositionsMap
        self.test_intersectionMap: Dict[int,  List[bool]] = test_intersectionMap
