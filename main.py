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
        self.diments = self.Diments
        self.selectedVertex = 0
        self.isSelectingVertexMode = False
        self.vertices: list[Vertex] = [
            Vertex(0, Pos(300, 300)),
            Vertex(44, Pos(*self.displaySizeHalf)),
            Vertex(999, Pos(400, 400))
        ]

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
                if event.key == pg.K_LCTRL and self.isSelectingVertexMode:
                    self.isSelectingVertexMode = False
            if event.type == pg.MOUSEBUTTONUP:
                if self.isSelectingVertexMode:
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
            for v in self.vertices:
                self.drawVertex(v)
            self.updateDisplay()

    def drawVertex(self, v: Vertex):
        vertex = deepcopy(v)
        self._drawVertexCircle(vertex)
        self._drawVertexText(vertex)

    def _drawVertexText(self, v: Vertex):
        font = pg.font.SysFont(pg.font.get_default_font(), self.Diments.fontSizeOnVertex)
        keyImage = font.render(str(v.idKey), True, self.Colors.OnVertexDefaultColor)
        wText, hText = font.size(str(v.idKey))
        self.screen.blit(keyImage, [(v.pos.x - (wText // 2)), (v.pos.y - (hText // 2))])

    def _drawVertexCircle(self, v: Vertex):
        color = self.Colors.onSurfaceColor
        if v.status == "default":
            color = self.Colors.vertexDefaultColor
        pg.draw.circle(self.screen, color, v.pos.__iter__(), self.Diments.vertexRadius)

    def startMouseThread(self):
        self.mouseThread.daemon = False
        self.mouseThread.start()

    def mouse(self):
        while self.mainThreadIsRunning:
            mx, my = pg.mouse.get_pos()
            if self.isSelectingVertexMode:
                self.vertices[self.selectedVertex].pos.x = mx
                self.vertices[self.selectedVertex].pos.y = my
            if pg.mouse.get_pressed()[0]:
                if self.isSelectingVertexMode:
                    continue
                vertex = self.getClickedVertexAt(Pos(mx, my))
                if vertex is not None:
                    self.selectedVertex = self.vertices.index(vertex)

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


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    v.startMouseThread()
