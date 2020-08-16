import sys

import pygame as sdl

import Colors
from DataTypes.Pos import Pos
from Mangers.GraphGenerator import GraphGenerator
from main import Visualizer
from Views .VertexClass import Vertex, EdgeClass

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=3)
graphGenerator = GraphGenerator(w, h)
graphGenerator.vertices.extend([VertexClass(44, Pos(w // 2, (h // 2)))])
graphGenerator.vertices.extend([VertexClass(33, Pos(w // 2, (h // 2)))])
graphGenerator.vertices.extend([VertexClass(22, Pos(w // 2, (h // 2)))])
graphGenerator.edges.extend([EdgeClass(22, 33)])
# graphHolder = graphGenerator.generateTriangle()
graphHolder = graphGenerator.generateTriangle()

v.graphManger.setupFromGraphHolder(graphGenerator.exportGraphHolder())
v.startMouseThread()
font = sdl.font.SysFont(sdl.font.get_default_font(), 30)


def showIntersectionMemory(verticesName):
    posY = 0
    for name in map(str, verticesName):
        vertex = v.graphManger.verticesManger.byName(name)
        text = vertex._lastIntersectionMemory
        keyImage = font.render(f"{name:5} memo:{text}", True, Colors.MainColors.onSurfaceColor)
        v.screen.blit(keyImage, [0, posY])
        posY += font.size(name)[1]


firstTime = False
while True:
    v.events()

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()

    showIntersectionMemory(map(lambda x: x.vertexName, v.graphManger.vertices))

    v.updateDisplay()
    if firstTime:
        v.toggleVerticesSetupMode()
        firstTime = False
