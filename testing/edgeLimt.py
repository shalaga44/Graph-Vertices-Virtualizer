import sys
from math import trunc
from typing import List

import pygame as sdl

import Colors
from DataTypes.Pos import Pos
from LinearMath import getDistanceBetween2Vertices
from Mangers.GraphGenerator import GraphGenerator
from main import Visualizer
from Views.VertexClass import Vertex
from Views.EdgeClass import Edge

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
graphGenerator = GraphGenerator(w, h)
# graphGenerator.vertices.extend([Vertex(44, Pos(w // 2, (h // 2)))])
# graphGenerator.vertices.extend([Vertex(33, Pos(w // 2, (h // 2)))])
# graphGenerator.vertices.extend([Vertex(22, Pos(w // 2, (h // 2)))])
# graphGenerator.edges.extend([Edge
#                              (22, 33)])
# # graphHolder = graphGenerator.generateTriangle()
# graphGenerator.generateTriangle()
graphGenerator.generate2ComponentsGraph()
v.graphManger.setupFromGraphHolder(graphGenerator.exportGraphHolder())
v.startMouseThread()
font = sdl.font.SysFont(sdl.font.get_default_font(), 30)


def showDistanceBetweenVertices(vertices: List[Vertex]):
    posY = 0
    for vertex in vertices:
        name = vertex.vertexName
        text = f"{name:^3} dist:{vertex._lastIntersectionMemory}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        v.screen.blit(keyImage, [0, posY])
        posY += font.size(name)[1]


firstTime = False


def showDistanceBetweenEdges(edges: List[Edge]):
    posY = 0
    for edge in edges:
        startV = v.graphManger.verticesManger.byName(edge.start)
        endV = v.graphManger.verticesManger.byName(edge.end)
        length = getDistanceBetween2Vertices(startV, endV)
        text = f"{edge.start:^3}-{trunc(length)}->{edge.end:^3}"
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
while True:
    v.events()
    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()

    showDistanceBetweenVertices(v.graphManger.vertices)
    showPosOfVertices(v.graphManger.vertices)
    showDistanceBetweenEdges(v.graphManger.edges)

    v.updateDisplay()
    if firstTime:
        v.toggleVerticesSetupMode()
        firstTime = False
