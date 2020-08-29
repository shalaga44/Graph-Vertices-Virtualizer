import pygame as sdl

import Colors
from DataTypes.pos import Pos
from DataTypes.vertex_holder import VertexHolder
from LinearMath import calculateBezierPoints
from Mangers.graph_generator import GraphGenerator
from Views.button import Button
from main import Visualizer
from testing.utils import showDistanceBetweenEdges, showDistanceBetweenVertices, showPosOfVertices

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
vertices = [VertexHolder(0, (706, 568)), VertexHolder(1, (667, 312)), VertexHolder(2, (329, 312)),
            VertexHolder(3, (305, 579)), VertexHolder(4, (500, 210)), VertexHolder(5, (500, 210)),
            VertexHolder(6, (500, 210)), ]
graphGenerator = GraphGenerator(w, h)
graphGenerator.verticesManger.addVertices(vertices)
v.graphManger.setupFromGraphHolder(graphGenerator.exportGraphHolder())
v.startMouseThread()

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
    while T <= 1.0:
        pos: Pos = calculateBezierPoints(T,
                                         [v.graphManger.verticesManger.byName(0).pos,
                                          v.graphManger.verticesManger.byName(1).pos,
                                          v.graphManger.verticesManger.byName(2).pos,
                                          v.graphManger.verticesManger.byName(3).pos,
                                          v.graphManger.verticesManger.byName(4).pos,
                                          v.graphManger.verticesManger.byName(5).pos,
                                          ]
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
    showDistanceBetweenVertices(v.graphManger.vertices, v.screen)
    showPosOfVertices(v.graphManger.vertices, v)
    showDistanceBetweenEdges(v.graphManger.edges, v)

    v.updateDisplay()
