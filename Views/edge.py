from typing import Iterator

from Views.vertex import Vertex


class Edge:
    def __init__(self, startEdge: Vertex, endEdge: Vertex):
        self.start: Vertex = startEdge
        self.end: Vertex = endEdge
        self._str = f"{startEdge}->{endEdge}"

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str

    def __iter__(self) -> Iterator[Vertex]:
        return iter((self.start, self.end))
