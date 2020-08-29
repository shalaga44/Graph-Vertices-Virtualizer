import math
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


def calculatePoints(t: float, controlPoints: List[Pos]) -> Pos:
    if not 0 <= t <= 1: raise Exception("t: float ∈ [0,1]")
    n: int = len(controlPoints) - 1
    y: float = sum((pow((1 - t), n - i) * pow(t, i) * math.comb(n, i) * p.y) for i, p in enumerate(controlPoints))
    x: float = sum((pow((1 - t), n - i) * pow(t, i) * math.comb(n, i) * p.x) for i, p in enumerate(controlPoints))

    return Pos(int(x), int(y))


w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
vertices = [VertexHolder(0, (706, 568)), VertexHolder(1, (667, 312)), VertexHolder(2, (329, 312)),
            VertexHolder(3, (305, 579)), VertexHolder(-1, (500, 210))]
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


animationTime = 100
animationEnd = 100


def RUN_BUTTON_ACTION():
    global animationTime
    animationTime = 0


bW, bH = 100, 60
RUN_BUTTON = Button("run", Pos(((w // 2) - (bW // 2)), (h // 4) * 3))
RUN_BUTTON.setOnClick(RUN_BUTTON_ACTION)
v.buttons.append(RUN_BUTTON)

circlePos = Pos(0, 0)
while True:
    v.events()
    # showIntersectionCircle(v.graphManger.verticesManger.vertices)
    T = 0.0
    points = []
    while T < 1.0:
        pos: Pos = calculatePoints(T,
                                   [v.graphManger.verticesManger.byName(0).pos,
                                    v.graphManger.verticesManger.byName(1).pos,
                                    v.graphManger.verticesManger.byName(-1).pos,
                                    v.graphManger.verticesManger.byName(2).pos,
                                    v.graphManger.verticesManger.byName(3).pos]
                                   )
        points.append(tuple(pos))
        T += .01
    sdl.draw.lines(v.screen, Colors.MainColors.onSurfaceColor, (), points, 5)

    if animationTime < animationEnd:
        circlePos = points[animationTime]
        sdl.draw.circle(v.screen, Colors.red, tuple(circlePos), 20)
        animationTime += 1

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()
    v.drawButtons()
    # showDistanceBetweenVertices(v.graphManger.vertices)
    showPosOfVertices(v.graphManger.vertices)
    showDistanceBetweenEdges(v.graphManger.edges)

    v.updateDisplay()
