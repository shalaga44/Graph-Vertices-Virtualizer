from math import trunc
from typing import List

import pygame as sdl

import Colors
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from Mangers.graph_generator import GraphGenerator
from Views.button import Button
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


v.toggleVerticesSetupMode()
v.toggleEdgesSetupMode()


def RUN_BUTTON_ACTION():
    print("Boooooo")


bW, bH = 100, 60
RUN_BUTTON = Button("run", Pos(((w // 2) - (bW // 2)), (h // 4) * 3), _width=bW, _height=bH)
# RUN_BUTTON.setOnClick(RUN_BUTTON_ACTION)
v.buttons.append(RUN_BUTTON)
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

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()
    v.drawButtons()
    # showDistanceBetweenVertices(v.graphManger.vertices)
    showPosOfVertices(v.graphManger.vertices)
    showDistanceBetweenEdges(v.graphManger.edges)

    v.updateDisplay()
