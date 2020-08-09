import sys
from copy import deepcopy
from threading import Thread
from typing import Optional

import pygame as pg
import math

from Colors import MainColors
from DataTypes import Pos
from Diments import Diments
from Tokens import VerticesTokens
from views import Vertex, Edge


class Visualizer:
    def __init__(self):

        self.mainThreadIsRunning = True
        self.mouseThread = Thread(target=self.mouse)
        self.mainThread = Thread(target=self.main)
        pg.init()
        self.width, self.height = 1280, 720
        self.displaySize = (self.width, self.height)
        self.displaySizeHalf = (self.width // 2, self.height // 2)
        self.clock = pg.time.Clock()
        self.fps = 25
        self.scale = 1
        self.screen = pg.display.set_mode(self.displaySize)
        self.selectedVertex = 0
        self.isSelectingVertexMode = False
        self.vertices = [Vertex(44, Pos(*self.displaySizeHalf)), Vertex(999, Pos(*self.displaySizeHalf))]
        # self.vertices.extend(self.generateVerticesCanFitIn(self.width, self.height))
        self.verticesPositionsMap: dict[int:int] = {self.vertices[i].idKey: i for i in range(len(self.vertices))}
        self.edges = [Edge(44, 999)]
        # self.edges.extend(self.generateVerticesCanFitIn(self.width, self.height))
        self.edgesPositionsMap = {self.edges[i]: i for i in range(len(self.edges))}

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.halt()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.halt()
                elif (event.key == pg.K_LCTRL) or \
                        (event.type == pg.MOUSEBUTTONUP):
                    self.stopVertexSelectingMode()

    def updateDisplay(self):
        self.clock.tick(self.fps)
        pg.display.update()
        self.screen.fill(MainColors.surfaceColor)

    def startMainThread(self):
        self.mainThread.daemon = False
        self.mainThread.start()

    def main(self):
        while True:
            self.events()

            for edge in self.edges:
                self.drawEdge(edge)

            self.setupAndDrawVertices()

            self.updateDisplay()

    def drawVertex(self, vertex: Vertex):
        CopiedVertex = deepcopy(vertex)
        self._drawVertexCircle(CopiedVertex)
        self._drawVertexText(CopiedVertex)
        vertex.isMoved = False

    def _drawVertexText(self, vertex: Vertex):

        self.screen.blit(vertex.textImage, vertex.textPos)

    def _drawVertexCircle(self, vertex: Vertex):
        pg.draw.circle(self.screen, vertex.color, vertex.pos.location(), Diments.vertexRadius)

    def startMouseThread(self):
        self.mouseThread.daemon = False
        self.mouseThread.start()

    def mouse(self):
        while self.mainThreadIsRunning:
            if self.isSelectingVertexMode:
                self.moveSelectedVertexToMouse()
                self.separateFromOtherVertices(self.vertices[self.selectedVertex])
            elif pg.mouse.get_pressed()[0]:
                if self.isSelectingVertexMode:
                    self.stopVertexSelectingMode()
                else:
                    self.startVertexSelectingMode()

    def getClickedVertexAt(self, p: Pos) -> Optional[Vertex]:
        r = Diments.vertexRadius
        for c in self.vertices:
            if self.isPointInCircle(p.x, p.y, c.pos.x, c.pos.y, r):
                return c
        self.stopVertexSelectingMode()
        return None

    def halt(self):
        self.mainThreadIsRunning = False
        sys.exit(0)

    def moveSelectedVertexToMouse(self):
        mx, my = pg.mouse.get_pos()
        self.vertices[self.selectedVertex].pos.x = mx
        self.vertices[self.selectedVertex].pos.y = my

    def updateSelectedVertex(self):
        mx, my = pg.mouse.get_pos()
        vertex = self.getClickedVertexAt(Pos(mx, my))
        if vertex is not None:
            self.startVertexSelectingMode(vertex)

    def separateVertices(self):
        for vertex in self.vertices:
            for u in self.vertices:
                if vertex == u: continue
                if not self.isSelectedVertex(u):
                    intersection = self.isVerticesIntersecting(vertex, u)
                    if intersection:  u.moveAwayFrom(vertex, intersection)

    def isVerticesIntersecting(self, v, u):
        r = Diments.vertexRadius * 2
        return self.isCirclesIntersecting(v.pos.x, v.pos.y, u.pos.x, u.pos.y, r, r)

    @staticmethod
    def isPointInCircle(pX, pY, cX, cY, r):
        d = math.sqrt((abs(pX - cX) ** 2) + (abs(pY - cY) ** 2))
        if d <= r: return True
        return False

    @staticmethod
    def isCirclesIntersecting(x1, y1, x2, y2, r1, r2):
        distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        radSumSq = (r1 + r2) * (r1 + r2)
        intersection = distSq - radSumSq
        if intersection < 0:
            return intersection
        return 0

    def startVertexSelectingMode(self, vertex=None):
        if vertex is None:
            self.updateSelectedVertex()

        if vertex is not None:
            self.selectedVertex = self.verticesPositionsMap[vertex.idKey]
            vertex.status = VerticesTokens.isSelected
            self.isSelectingVertexMode = True

    def stopVertexSelectingMode(self):
        vertex = self.vertices[self.selectedVertex]
        vertex.status = VerticesTokens.isDefault
        self.isSelectingVertexMode = False

    def isSelectedVertex(self, v: Vertex):
        if self.isSelectingVertexMode:
            return self.verticesPositionsMap[v.idKey] == self.selectedVertex
        return False

    def alignVertexOnScreen(self, vertex):
        r = Diments.vertexRadius
        if vertex.pos.x - r < 0: vertex.pos.x = 0 + r
        if vertex.pos.x + r > self.width: vertex.pos.x = self.width - r
        if vertex.pos.y - r < 0: vertex.pos.y = 0 + r
        if vertex.pos.y + r > self.height: vertex.pos.y = self.height - r

    def separateFromOtherVertices(self, vertex):
        for u in self.vertices:
            if vertex == u: continue
            if not self.isSelectedVertex(u):
                intersection = self.isVerticesIntersecting(vertex, u)
                if intersection:  u.moveAwayFrom(vertex, intersection)

    @staticmethod
    def generateVerticesCanFitIn(width, height):
        c, r = ((width // (Diments.vertexRadius * 2)) // 2) + 1, (
                (height // (Diments.vertexRadius * 2)) // 2)
        vertices = [Vertex(i, Pos(((i % c) * (width // c)),
                                  ((i // c) * (height // r))))
                    for i in range(c * r)]
        return vertices

    def setupAndDrawVertices(self):
        for vertex in self.vertices:
            if vertex.isMoved:
                self.separateFromOtherVertices(vertex)
                self.alignVertexOnScreen(vertex)
            self.drawVertex(vertex)

    def drawEdge(self, edge):
        pg.draw.line(self.screen, (0, 0, 0),
                     self.vertices[self.verticesPositionsMap[edge.start]].pos.location(),
                     self.vertices[self.verticesPositionsMap[edge.end]].pos.location(), 5)


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    v.startMouseThread()
