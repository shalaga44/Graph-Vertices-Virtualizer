import pygame as sdl

from Mangers.graph_generator import GraphGenerator
from main import Visualizer
from testing.utils import showIntersectionCircle, showDistanceBetweenVertices, showPosOfVertices, \
    showDistanceBetweenEdges

w, h = 1000, 1000
v = Visualizer(displaySize=(w, h), scale=1)
graphGenerator = GraphGenerator(w, h)
# graphGenerator.vertices.extend([Vertex(44, Pos(w // 2, (h // 2)))])
# graphGenerator.vertices.extend([Vertex(33, Pos(w // 2, (h // 2)))])
# graphGenerator.vertices.extend([Vertex(22, Pos(w // 2, (h // 2)))])
# graphGenerator.edges.extend([Edge
#                              (22, 33)])
# graphHolder = graphGenerator.generateTriangle()
graphGenerator.generateTriangle()
graphGenerator.generate2ComponentsGraph()

v.graphManger.setupFromGraphHolder(graphGenerator.generateRandomShape())
v.startMouseThread()
font = sdl.font.SysFont(sdl.font.get_default_font(), 30)

v.toggleVerticesSetupMode()
v.toggleEdgesSetupMode()
firstTime = True
secondTime = False
thirdTime = False
fourthTime = False
fifthTime = False
while True:
    v.events()
    showIntersectionCircle(v.graphManger.verticesManger.vertices, v)

    v.graphManger.setupVertices()
    v.graphManger.setupEdges()
    v.drawEdges()
    v.drawVertices()

    showDistanceBetweenVertices(v.graphManger.vertices, v.screen)
    showPosOfVertices(v.graphManger.vertices, v)
    showDistanceBetweenEdges(v.graphManger.edges, v)

    v.updateDisplay()
    if firstTime:
        v.toggleVerticesSetupMode()
        firstTime = False
        secondTime = True

    elif secondTime and v.graphManger.isVerticesIntersecting:
        v.toggleEdgesSetupMode()
        v.startCrazySpanningMode()
        secondTime = False
        thirdTime = True

    elif thirdTime and v.graphManger.isVerticesIntersecting:
        v.startCrazySpanningMode()
        thirdTime = False
        fourthTime = True

    elif fourthTime and not v.graphManger.isVerticesIntersecting:
        v.toggleVerticesSetupMode()
        fourthTime = False
        fifthTime = True

    elif fifthTime and v.graphManger.isVerticesIntersecting:
        v.toggleVerticesSetupMode()
        firstTime = False
