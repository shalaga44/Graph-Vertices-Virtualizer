from Views.vertex import Vertex


class Edge:
    def __init__(self, fromVertex: Vertex, toVertex: Vertex):
        self.start: Vertex = fromVertex
        self.end: Vertex = toVertex
        self._str = f"{fromVertex}->{toVertex}"

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str
