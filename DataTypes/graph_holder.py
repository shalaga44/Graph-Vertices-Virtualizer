from typing import List

from Views.edge import Edge
from Views.vertex import Vertex


class GraphHolder:
    # def __init__(self, edges: List[Edge], vertices: List[Vertex], edgesPositionsMap: Dict[int, int] ):
    def __init__(self, edges: List[Edge], vertices: List[Vertex]):
        self.edges: List[Edge] = edges
        self.vertices: List[Vertex] = vertices
