from typing import Dict, List

from Views.vertex import Vertex
from Views.edge import Edge


class GraphHolder:
    # def __init__(self, edges: List[Edge], vertices: List[Vertex], edgesPositionsMap: Dict[int, int] ):
    def __init__(self, edges, vertices):
        self.edges: List[Edge] = edges
        self.vertices: List[Vertex] = vertices