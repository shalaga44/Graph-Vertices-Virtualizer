from Dimensions import MainDiments
from SingletonMetaClass import Singleton


class DimensionsManger(metaclass=Singleton):
    def __init__(self):
        self.isChanged = False
        self._scaleFactor = MainDiments.scaleFactor = .9
        self.updateScales()

    @property
    def scaleFactor(self):
        return self._scaleFactor

    @scaleFactor.setter
    def scaleFactor(self, a):
        self._scaleFactor = round(a, 2)
        self.updateScales()

    class VerticesDiments:
        radius: int
        fontSize: int
        intersectionRadius: int

    class EdgesDiments:
        width: int
        length: int

    def updateScales(self):
        self.VerticesDiments.radius = int(25 * self.scaleFactor)
        self.VerticesDiments.fontSize = int(30 * self.scaleFactor)
        self.VerticesDiments.intersectionRadius = self.VerticesDiments.radius * 2
        self.EdgesDiments.width = int(5 * self.scaleFactor)
        self.EdgesDiments.length = self.VerticesDiments.intersectionRadius * 3
