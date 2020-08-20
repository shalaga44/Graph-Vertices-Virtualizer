from typing import List

from DataTypes.edge_holder import EdgeHolder
from Views.vertex import Vertex


class GraphHolder:
    # def __init__(self, edges: List[Edge], vertices: List[Vertex], edgesPositionsMap: Dict[int, int] ):
    def __init__(self, edges: List[EdgeHolder], vertices):
        self.edges: List[EdgeHolder] = edges
        self.vertices: List[Vertex] = vertices
