from typing import Dict, List

from views import Vertex, Edge


class GraphHolder:
    def __init__(self, edges: List[Edge], vertices: List[Vertex], edgesPositionsMap: Dict[int, int], ):
        self.edges: List[Edge] = edges
        self.vertices: List[Vertex] = vertices

        self.edgesPositionsMap: Dict[int, int] = edgesPositionsMap
