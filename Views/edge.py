class Edge:
    def __init__(self, fromVertexName, toVertexName):
        self.start: str = str(fromVertexName)
        self.end: str = str(toVertexName)
        self._str = f"{fromVertexName}->{toVertexName}"

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str
