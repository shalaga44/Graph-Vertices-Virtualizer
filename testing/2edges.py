import math
from typing import List

import pygame as sdl

import Colors
from DataTypes.edge_holder import EdgeHolder
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from LinearMath import calculateBezierPoints, getMidPointInLine
from Mangers.font_manager import FontManager
from Mangers.graph_generator import GraphGenerator
from Views.edge import Edge
from Views.vertex import Vertex
from main import Visualizer
from testing.utils import showPosOfVertices

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
verticesC0 = [VertexHolder('V0', (300, 600)), VertexHolder('V1', (700, 600)), VertexHolder('C0', (500, 400)),
              VertexHolder('C1', (500, 700))]
edges = [EdgeHolder('V0', 'V1')]
graphGenerator = GraphGenerator(w, h)
graphGenerator.addVerticesHolders(verticesC0)
graphGenerator.addEdgesHolders(edges)
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

verticesC0 = [v.graphManger.verticesManger.byName('V0'),
              v.graphManger.verticesManger.byName('C0'),
              v.graphManger.verticesManger.byName('V1'), ]
verticesC1 = [v.graphManger.verticesManger.byName('V0'),
              v.graphManger.verticesManger.byName('C1'),
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

    return math.atan(angle)


def showEdgeAngle(edges: List[Edge]):
    posY = 0
    for edge in edges:
        start = v.graphManger.verticesManger.byName(edge.start)
        end = v.graphManger.verticesManger.byName(edge.end)
        angle = getAngeBetweenVertices(start, end)
        text = f"{edge.start.name:^3}  {angle* (180 / math.pi)}  {edge.end.name:^3}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        posX = v.height - font.size(text)[0]
        v.screen.blit(keyImage, [posX - 20, posY])
        posY += font.size(text)[1]


circlePos = Pos(0, 0)
v.graphManger.edgesManger.byId("(V0, V1)").isCarve = True
while True:
    v.events()
    # showIntersectionCircle(v.graphManger.verticesManger.vertices)
    T = 0.0
    pointsC0 = []
    pointsC1 = []
    while T <= 1.0:
        posC0: Pos = calculateBezierPoints(T, list(map(lambda x: x.pos, verticesC0)))
        posC1: Pos = calculateBezierPoints(T, list(map(lambda x: x.pos, verticesC1)))
        pointsC0.append(tuple(posC0))
        pointsC1.append(tuple(posC1))
        T += .01
    sdl.draw.lines(v.screen, Colors.red, (), pointsC1, 5)
    sdl.draw.lines(v.screen, Colors.red, (), pointsC0, 5)

    # if animationTime < animationEnd:
    #     circlePos = points[animationTime]
    #     sdl.draw.circle(v.screen, Colors.red, tuple(circlePos), 20)
    #     animationTime += 1
    midPos = Pos(*getMidPointInLine(verticesC0[0].pos, verticesC0[-1].pos))
    sdl.draw.circle(v.screen, Colors.red, tuple(midPos), 5)
    r = 200
    angle = getAngeBetweenVertices(verticesC0[0], verticesC0[-1])
    c0x = (r * math.sin(math.pi)) + midPos.x
    c0y = (r * math.cos(math.pi)) + midPos.y  
    c0 = v.graphManger.verticesManger.byName('C0')
    c0.pos.x = c0x
    c0.pos.y = c0y

    c1x = (r * -math.sin(math.pi)) + midPos.x
    c1y = (r * -math.cos(((math.pi) + 1))) + midPos.y
    c1 = v.graphManger.verticesManger.byName('C1')
    c1.pos.x = c1x
    c1.pos.y = c1y

    # sdl.draw.circle(v.screen, Colors.blueDark, tuple(map(int, (c1x, c1y))), 50)

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()

    v.drawVertices()
    v.drawButtons()
    showPosOfVertices(v.graphManger.vertices, v)
    # showDistanceBetweenEdges(v.graphManger.edges, v)
    showEdgeAngle(v.graphManger.edges)

    v.updateDisplay()
