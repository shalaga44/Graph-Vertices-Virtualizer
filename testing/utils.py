from math import trunc
from typing import List

import pygame

import Colors
from Mangers.font_manager import FontManager
from Views.edge import Edge
from Views.vertex import Vertex
from main import Visualizer

font = FontManager().font


def showDistanceBetweenVertices(vertices: List[Vertex], screen: pygame.display):
    posY = 0
    for vertex in vertices:
        name = vertex.name
        text = f"{name:^3} dist:{vertex._lastIntersectionMemory}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        screen.blit(keyImage, [0, posY])
        posY += font.size(name)[1]


def showIntersectionCircle(vertices: List[Vertex], v: Visualizer):
    for vertex in vertices:
        pygame.draw.circle(v.screen, (255, 20, 200), tuple(vertex.pos),
                           v.dimentsManger.VerticesDiments.intersectionRadius)


def showDistanceBetweenEdges(edges: List[Edge], v: Visualizer):
    posY = 0
    for edge in edges:
        length = v.graphManger.edgesManger.length(edge)
        text = f"{edge.start.name:^3}-{trunc(length)}->{edge.end.name:^3}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        posX = v.height - font.size(text)[0]
        v.screen.blit(keyImage, [posX - 20, posY])
        posY += font.size(text)[1]


def showPosOfVertices(vertices: List[Vertex], v: Visualizer):
    for vertex in vertices:
        text = f"{vertex.pos}"
        keyImage = font.render(text, True, Colors.MainColors.onSurfaceColor)
        r = v.dimentsManger.VerticesDiments.radius
        v.screen.blit(keyImage, [vertex.pos.x - font.size(text)[0] - r, vertex.pos.y - r])
