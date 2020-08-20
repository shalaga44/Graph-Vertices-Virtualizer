from typing import List

import pygame as sdl

import Colors
from DataTypes.edge_holder import EdgeHolder
from DataTypes.vertex_holder import VertexHolder
from Mangers.graph_generator import GraphGenerator
from Views.vertex import Vertex
from main import Visualizer

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
graphGenerator = GraphGenerator(w, h)
graphGenerator.verticesManger.addVertices([VertexHolder(44)])
graphGenerator.verticesManger.addVertices([VertexHolder(33)])
graphGenerator.verticesManger.addVertices([VertexHolder(22)])
graphGenerator.edgesManger.addEdges([EdgeHolder(22, 33)])
# graphHolder = graphGenerator.generateTriangle()
graphHolder = graphGenerator.generateTriangle

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


def showIntersectionCircle(vertices: List[Vertex]):
    for vertex in vertices:
        sdl.draw.circle(v.screen, (255, 20, 200), tuple(vertex.pos), v.dimentsManger.VerticesDiments.intersectionRadius)


firstTime = False
while True:
    v.events()

    showIntersectionCircle(v.graphManger.vertices)

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()

    showIntersectionMemory(map(lambda x: x.name, v.graphManger.vertices))

    v.updateDisplay()
    if firstTime:
        v.toggleVerticesSetupMode()
        firstTime = False
