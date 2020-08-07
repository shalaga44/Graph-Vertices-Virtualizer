import sys
from copy import deepcopy
from threading import Thread
import pygame as pg

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
        self.vertices: list[Vertex] = [Vertex(999, Pos(*self.displaySizeHalf))]

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
                self.mainThreadIsRunning = False
                sys.exit(0)

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
            self.vertices[0].pos.x = mx
            self.vertices[0].pos.y = my


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    v.startMouseThread()
