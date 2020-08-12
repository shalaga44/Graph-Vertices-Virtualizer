from typing import Dict, List

from SingletonMetaClass import Singleton
from views import Vertex


class VerticesManger(metaclass=Singleton):
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.verticesPositionsMap: Dict[int:int] = {}
