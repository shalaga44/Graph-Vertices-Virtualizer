import math
from typing import List

import pygame as sdl

import Colors
from DataTypes.edge_holder import EdgeHolder
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from LinearMath import calculateBezierPoints
from Mangers.font_manager import FontManager
from Mangers.graph_generator import GraphGenerator
from Views.edge import Edge
from Views.vertex import Vertex
from main import Visualizer
from testing.utils import showPosOfVertices

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
vertices = [VertexHolder('V0', (300, 600)), VertexHolder('V1', (700, 600)), VertexHolder('C0', (500, 400)),
            VertexHolder('C1', (500, 700))]
edges = [EdgeHolder('V0', 'V1')]
graphGenerator = GraphGenerator(w, h)
graphGenerator.verticesManger.addVertices(vertices)
graphGenerator.edgesManger.addEdges(edges)
v.graphManger.setupFromGraphHolder(graphGenerator.exportGraphHolder())
v.startMouseThread()

animationTime = 100
animationEnd = 100

# def RUN_BUTTON_ACTION():
#     global animationTime
#     animationTime = 0
#

# bW, bH = 100, 60
# RUN_BUTTON = Button("run", Pos(((w // 2) - (bW // 2)), (h // 4) * 3))
# RUN_BUTTON.setOnClick(RUN_BUTTON_ACTION)
# v.buttons.append(RUN_BUTTON)

vertices = [v.graphManger.verticesManger.byName('V0'),
            v.graphManger.verticesManger.byName('C0'),
            v.graphManger.verticesManger.byName('V1'), ]

font = FontManager().font


def getAngeBetweenVertices(start: Vertex, end: Vertex) -> float:
    x0 = start.pos.x
    y0 = start.pos.y
    x1 = end.pos.x
    y1 = end.pos.y
    try:
        angle = ((y1 - y0) / (x1 - x0))
    except ZeroDivisionError:
        return 0

    return math.atan(angle) * (180 / math.pi)


def getMidPointInLine(start: Vertex, end: Vertex) -> Pos:
    return Pos(start.pos.x + ((end.pos.x - start.pos.x) // 2),
               start.pos.y + ((end.pos.y - start.pos.y) // 2))


def showEdgeAngle(edges: List[Edge]):
    posY = 0
    for edge in edges:
        start = v.graphManger.verticesManger.byName(edge.start)
        end = v.graphManger.verticesManger.byName(edge.end)
        angle = getAngeBetweenVertices(start, end)
        text = f"{edge.start.name:^3}  {angle}  {edge.end.name:^3}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        posX = v.height - font.size(text)[0]
        v.screen.blit(keyImage, [posX - 20, posY])
        posY += font.size(text)[1]


circlePos = Pos(0, 0)
while True:
    v.events()
    # showIntersectionCircle(v.graphManger.verticesManger.vertices)
    T = 0.0
    points = []
    while T <= 1.0:
        pos: Pos = calculateBezierPoints(T, list(map(lambda x: x.pos, vertices)))
        points.append(tuple(pos))
        T += .01
    sdl.draw.lines(v.screen, Colors.MainColors.onSurfaceColor, (), points, 5)
    if animationTime < animationEnd:
        circlePos = points[animationTime]
        sdl.draw.circle(v.screen, Colors.red, tuple(circlePos), 20)
        animationTime += 1

    sdl.draw.circle(v.screen, Colors.red, tuple(getMidPointInLine(vertices[0], vertices[-1])), 5)
    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()
    v.drawButtons()
    showPosOfVertices(v.graphManger.vertices, v)
    # showDistanceBetweenEdges(v.graphManger.edges, v)
    showEdgeAngle(v.graphManger.edges)

    v.updateDisplay()
