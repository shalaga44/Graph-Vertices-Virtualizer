import pygame as sdl

from DataTypes.edge_holder import EdgeHolder
from DataTypes.vertex_holder import VertexHolder
from Mangers.graph_generator import GraphGenerator
from main import Visualizer
from testing.utils import showIntersectionCircle, showDistanceBetweenVertices

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

firstTime = False
while True:
    v.events()

    showIntersectionCircle(v.graphManger.vertices, v)

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()

    showDistanceBetweenVertices(v.graphManger.vertices, v.screen)

    v.updateDisplay()
    if firstTime:
        v.toggleVerticesSetupMode()
        firstTime = False
