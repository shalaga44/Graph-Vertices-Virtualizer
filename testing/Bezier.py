from math import trunc
from typing import List

import pygame as sdl
from pygame.rect import Rect

import Colors
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from Mangers.graph_generator import GraphGenerator
from Views.edge import Edge
from Views.vertex import Vertex
from main import Visualizer


# 𝑓𝑥(𝑡):=(1−𝑡)3𝑝1𝑥+3𝑡(1−𝑡)2𝑝2𝑥+3𝑡2(1−𝑡)𝑝3𝑥+𝑡3𝑝4𝑥
def calculatePoints(t: float, start: Pos, c1: Pos, c2: Pos, end: Pos) -> Pos:
    x: float = \
        ((1.0 - t) ** 3.0) * start.x + 3 * t * ((1.0 - t) ** 2.0) * c1.x + 3 * t * t * (
                1.0 - t) * c2.x + t * t * t * end.x
    y: float = \
        ((1.0 - t) ** 3.0) * start.y + 3 * t * ((1.0 - t) ** 2.0) * c1.y + 3 * t * t * (
                1.0 - t) * c2.y + t * t * t * end.y
    return Pos(int(x), int(y))


w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
vertices = [VertexHolder(0, (706, 568)), VertexHolder(1, (667, 302)), VertexHolder(2, (329, 312)),
            VertexHolder(3, (305, 579))]
graphGenerator = GraphGenerator(w, h)
graphGenerator.verticesManger.addVertices(vertices)
v.graphManger.setupFromGraphHolder(graphGenerator.exportGraphHolder())
v.startMouseThread()
font = sdl.font.SysFont(sdl.font.get_default_font(), 30)


def showDistanceBetweenVertices(vertices: List[Vertex]):
    posY = 0
    for vertex in vertices:
        name = vertex.name
        text = f"{name:^3} dist:{vertex._lastIntersectionMemory}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        v.screen.blit(keyImage, [0, posY])
        posY += font.size(name)[1]


def showIntersectionCircle(vertices: List[Vertex]):
    for vertex in vertices:
        sdl.draw.circle(v.screen, (255, 20, 200), tuple(vertex.pos), v.dimentsManger.VerticesDiments.intersectionRadius)


def showDistanceBetweenEdges(edges: List[Edge]):
    posY = 0
    for edge in edges:
        length = v.graphManger.edgesManger.length(edge)
        text = f"{edge.start.name:^3}-{trunc(length)}->{edge.end.name:^3}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        posX = h - font.size(text)[0]
        v.screen.blit(keyImage, [posX - 20, posY])
        posY += font.size(text)[1]


def showPosOfVertices(vertices):
    for vertex in vertices:
        text = f"{vertex.pos}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        r = v.dimentsManger.VerticesDiments.radius
        v.screen.blit(keyImage, [vertex.pos.x - font.size(text)[0] - r, vertex.pos.y - r])


class Button:
    def __init__(self, _text: str, _pos: Pos, _width: int = 100, _height: int = 100):
        self._width = _width
        self._height = _height
        self._text = str(_text)
        self._pos = _pos
        self.colorText = Colors.MainColors.surfaceColor
        self.colorBackground = Colors.MainColors.onSurfaceColor
        self._rect = self._createRect(_pos.x, _pos.y, _width, _height)
        self._textImage = self._creatText(_text)

    @staticmethod
    def _createRect(left, top, _width, height) -> Rect:
        rect = sdl.rect.Rect(left, top, _width, height)
        return rect

    def _drawRect(self, screen: sdl.display):
        sdl.draw.rect(screen, self.colorBackground, self._rect)

    def _drawText(self, screen: sdl.display):
        screen.blit(self._textImage, self.textPos)

    def draw(self, screen: sdl.display):
        self._drawRect(screen)
        self._drawText(screen)

    def _creatText(self, _text) -> sdl.Surface:
        textImage = font.render(self._text, True, self.colorText)
        wText, hText = font.size(self._text)
        self.wTextHalf, self.hTextHalf = wText // 2, hText // 2
        self.textPos = (self._pos.x + (self._width // 2)) - self.wTextHalf, (
                self._pos.y + (self._height // 2)) - self.hTextHalf
        self._textImage = textImage
        return textImage

v.toggleVerticesSetupMode()
v.toggleEdgesSetupMode()
bW, bH = 100, 60
b = Button("run", Pos(((w // 2)-(bW//2)), (h // 4) * 3), _width=bW, _height=bH)

while True:
    v.events()
    showIntersectionCircle(v.graphManger.verticesManger.vertices)
    t = 0.0
    points = []
    while t < 1.0:
        pos: Pos = calculatePoints(t,
                                   v.graphManger.verticesManger.byName(0).pos,
                                   v.graphManger.verticesManger.byName(1).pos,
                                   v.graphManger.verticesManger.byName(2).pos,
                                   v.graphManger.verticesManger.byName(3).pos,
                                   )
        points.append(tuple(pos))
        t += .01
    sdl.draw.lines(v.screen, Colors.MainColors.onSurfaceColor, (), points, 5)
    b.draw(v.screen)
    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()
    # showDistanceBetweenVertices(v.graphManger.vertices)
    showPosOfVertices(v.graphManger.vertices)
    showDistanceBetweenEdges(v.graphManger.edges)

    v.updateDisplay()
