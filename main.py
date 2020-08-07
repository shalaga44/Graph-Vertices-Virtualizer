import sys
from copy import deepcopy
from threading import Thread
from typing import Optional

import pygame as pg
import math
from DataTypes import Pos
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
        self.vertices: list[Vertex] = [
            Vertex(0, Pos(300, 300)),
            Vertex(44, Pos(*self.displaySizeHalf)),
            Vertex(999, Pos(400, 400))
        ]
        self.verticesPositionsMap = {self.vertices[i].idKey: i for i in range(len(self.vertices))}

    class Colors:
        OnVertexDefaultColor = (255, 255, 255)
        surfaceColor = (255, 255, 255)
        onSurfaceColor = (0, 0, 0)
        vertexDefaultColor = (0, 76, 207)

    class Diments:
        scaleFactor = 1
        vertexRadius = 25 * scaleFactor
        fontSizeOnVertex = 30 * scaleFactor

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.halt()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.halt()
                elif (event.key == pg.K_LCTRL) or \
                        (event.type == pg.MOUSEBUTTONUP):
                    self.isSelectingVertexMode = False

    def updateDisplay(self):
        self.clock.tick(self.fps)
        pg.display.update()
        self.screen.fill(self.Colors.surfaceColor)

    def startMainThread(self):
        self.mainThread.daemon = False
        self.mainThread.start()

    def main(self):
        while True:
            self.events()

            for vertex in self.vertices: self.drawVertex(vertex)

            self.updateDisplay()

    def drawVertex(self, vertex: Vertex):
        vertex = deepcopy(vertex)
        self._drawVertexCircle(vertex)
        self._drawVertexText(vertex)

    def _drawVertexText(self, vertex: Vertex):
        font = pg.font.SysFont(pg.font.get_default_font(), self.Diments.fontSizeOnVertex)
        keyImage = font.render(str(vertex.idKey), True, self.Colors.OnVertexDefaultColor)
        wText, hText = font.size(str(vertex.idKey))
        self.screen.blit(keyImage, [(vertex.pos.x - (wText // 2)), (vertex.pos.y - (hText // 2))])

    def _drawVertexCircle(self, vertex: Vertex):
        color = self.Colors.onSurfaceColor
        if vertex.status == "default":
            color = self.Colors.vertexDefaultColor
        pg.draw.circle(self.screen, color, vertex.pos.__iter__(), self.Diments.vertexRadius)

    def startMouseThread(self):
        self.mouseThread.daemon = False
        self.mouseThread.start()

    def mouse(self):
        while self.mainThreadIsRunning:
            if self.isSelectingVertexMode:
                self.moveSelectedVertexToMouse()
            elif pg.mouse.get_pressed()[0]:
                self.updateSelectedVertex()

    def getClickedVertexAt(self, p: Pos) -> Optional[Vertex]:
        for c in self.vertices:
            d = math.sqrt((abs(p.x - c.pos.x) ** 2) +
                          (abs(p.y - c.pos.y) ** 2))
            if d <= self.Diments.vertexRadius:
                self.isSelectingVertexMode = True
                return c
        self.isSelectingVertexMode = False
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
            self.selectedVertex = self.verticesPositionsMap[vertex.idKey]


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    v.startMouseThread()
