import sys
from copy import deepcopy
from threading import Thread
from typing import Final

import pygame as pg

from Colors import MainColors, EdgesColors
from DataTypes.Pos import Pos
from Mangers.GraphGenerator import GraphGenerator
from Mangers.GraphManager import GraphManager, DimensionsManger
from views import Vertex


class Visualizer:
    def __init__(self):

        self.mainThreadIsRunning = True
        self.mouseThread = Thread(target=self.mouse)
        self.mainThread = Thread(target=self.main)
        pg.init()
        # self.width, self.height = 562, 1000
        self.width, self.height = 720, 720
        self.displaySize = (self.width, self.height)
        self.displaySizeHalf = (self.width // 2, self.height // 2)
        self.clock = pg.time.Clock()
        self.fps = 25
        self.scale = 1
        self.screen = pg.display.set_mode(self.displaySize)
        self.selectedVertex = 0
        self.graphManger: Final = GraphManager(*self.displaySize)
        self.graphGenerator = GraphGenerator(*self.displaySize)
        # graphHolder = self.graphGenerator.generate2ComponentsGraph()
        self.dimentsManger: Final = DimensionsManger(*self.displaySize)
        graphHolder = self.graphGenerator.generateVerticesCanFitIn(*self.displaySizeHalf,self.dimentsManger)
        self.graphManger.setupFromGraphHolder(graphHolder)
        # self.graphManger.generateVerticesCanFitIn(*self.displaySize)
        # self.graphManger.generate2ComponentsGraph()

    def main(self):
        while True:
            self.events()

            self.graphManger.setupEdges()
            self.graphManger.setupVertices()
            self.drawEdges()
            self.drawVertices()

            self.updateDisplay()

    def drawVertices(self):
        for vertex in self.graphManger.vertices:
            self._drawVertex(vertex)
            # vertex.isMoved = False

    def mouse(self):
        while self.mainThreadIsRunning:
            if self.graphManger.isSelectingVertexMode:
                self.moveSelectedVertexToMouse()

    def startVertexSelectingMode(self, mousePos: Pos):
        self.graphManger.startVertexSelectingMode(mousePos)

    def stopVertexSelectingMode(self):
        self.graphManger.stopVertexSelectingMode()

    def _drawEdge(self, edge):
        pg.draw.line(self.screen, EdgesColors.default,
                     tuple(self.graphManger.verticesManger.byName(edge.start).pos),
                     tuple(self.graphManger.verticesManger.byName(edge.end).pos),
                     self.dimentsManger.EdgesDiments.width)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.halt()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                self.startVertexSelectingMode(Pos(mx, my))
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.halt()
                elif (event.key == pg.K_LCTRL) or \
                        (event.type == pg.MOUSEBUTTONUP):
                    self.stopVertexSelectingMode()
                elif event.key == pg.K_SPACE:
                    self.startCrazySpanningMode()
                elif event.key == pg.K_EQUALS:
                    self.scaleFactorUp()
                elif event.key == pg.K_MINUS:
                    self.scaleFactorDown()

    def updateDisplay(self):
        self.clock.tick(self.fps)
        pg.display.update()
        self.screen.fill(MainColors.surfaceColor)
        pg.display.set_caption(f"scale:{self.dimentsManger.scaleFactor},\t\t"
                               f"Selection:{self.graphManger.isSelectingVertexMode},\t\t"
                               f"Crazy Spanning:{self.graphManger.isCrazySpanningMode} ")

    def startMainThread(self):
        self.mainThread.daemon = False
        self.mainThread.start()

    def _drawVertex(self, vertex: Vertex):
        CopiedVertex = deepcopy(vertex)
        self._drawVertexCircle(CopiedVertex)
        self._drawVertexText(CopiedVertex)

    def _drawVertexText(self, vertex: Vertex):
        self.screen.blit(vertex.textImage, vertex.textPos)

    def _drawVertexCircle(self, vertex: Vertex):
        pg.draw.circle(self.screen, vertex.color, vertex.pos.location(), self.dimentsManger.VerticesDiments.radius)

    def drawEdges(self):
        for edge in self.graphManger.edges:
            self._drawEdge(edge)

    def startMouseThread(self):
        self.mouseThread.daemon = False
        self.mouseThread.start()

    def halt(self):
        self.mainThreadIsRunning = False
        sys.exit(0)

    def moveSelectedVertexToMouse(self):
        mx, my = pg.mouse.get_pos()
        self.graphManger.moveSelectedVertexTo(mx, my)

    def startCrazySpanningMode(self):
        self.graphManger.startCrazySpanning()

    def scaleFactorUp(self):
        self.dimentsManger.scaleFactor += .5
        for v in self.graphManger.vertices:
            v.generateNewTextImage()

    def scaleFactorDown(self):
        if self.dimentsManger.scaleFactor > .1:
            self.dimentsManger.scaleFactor -= .1
            for v in self.graphManger.vertices:
                v.generateNewTextImage()


if __name__ == '__main__':
    v = Visualizer()
    v.startMainThread()
    v.startMouseThread()
