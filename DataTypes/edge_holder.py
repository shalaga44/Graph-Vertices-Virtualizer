from typing import Any


class EdgeHolder:
    def __init__(self, fromVertex: Any, toVertexName: Any):
        self.start: str = str(fromVertex)
        self.end: str = str(toVertexName)
        self.id = f"({fromVertex}, {toVertexName})"
