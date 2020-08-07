import sys
from copy import deepcopy
from threading import Thread
from typing import Optional

import pygame as pg
import math

from Colors import MainColors, VerticesColors
from DataTypes import Pos
from Diments import Diments
from Tokens import VerticesTokens
from views import Vertex


class Visualizer:
    def __init__(self):

        self.mainThreadIsRunning = True
        self.mouseThread = Thread(target=self.mouse)
        self.mainThread = Thread(target=self.main)
        pg.init()
        self.width, self.height = 720, 720
        self.displaySize = (self.width, self.height)
        self.displaySizeHalf = (self.width // 2, self.height // 2)
        self.clock = pg.time.Clock()
        self.fps = 25
        self.scale = 1
        self.screen = pg.display.set_mode(self.displaySize)
        self.selectedVertex = 0
        self.isSelectingVertexMode = False
        self.vertices = [Vertex(i, Pos(i * 50, i * 50)) for i in range(58)]
        self.verticesPositionsMap = {self.vertices[i].idKey: i for i in range(len(self.vertices))}

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
            # self.separateVertices()
            for vertex in self.vertices:
                if vertex.isMoved:
                    self.separateFromOtherVertices(vertex)
                    self.alignVertexOnScreen(vertex)
                self.drawVertex(vertex)

            self.updateDisplay()

    def drawVertex(self, vertex: Vertex):
        CopiedVertex = deepcopy(vertex)
        self._drawVertexCircle(CopiedVertex)
        self._drawVertexText(CopiedVertex)
        vertex.isMoved = False

    def _drawVertexText(self, vertex: Vertex):
        font = pg.font.SysFont(pg.font.get_default_font(), Diments.fontSizeOnVertex)
        keyImage = font.render(str(vertex.idKey), True, VerticesColors.OnVertexDefaultColor)
        wText, hText = font.size(str(vertex.idKey))
        self.screen.blit(keyImage, [(vertex.pos.x - (wText // 2)), (vertex.pos.y - (hText // 2))])

    def _drawVertexCircle(self, vertex: Vertex):
        color = MainColors.onSurfaceColor
        if vertex.status == VerticesTokens.isDefault:
            color = VerticesColors.vertexDefaultColor
        if vertex.status == VerticesTokens.isSelected:
            color = VerticesColors.vertexSelectedColor
        if vertex.status == VerticesTokens.isMoving:
            color = VerticesColors.isMoving
        pg.draw.circle(self.screen, color, vertex.pos.location(), Diments.vertexRadius)

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
        return self.verticesPositionsMap[v.idKey] == self.selectedVertex

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


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    # v.startMouseThread()
