import sys
from copy import deepcopy
from threading import Thread
from typing import Final, Tuple

import pygame as pg

from Colors import MainColors, EdgesColors
from DataTypes.Pos import Pos
from Mangers.GraphGenerator import GraphGenerator
from Mangers.GraphManager import GraphManager, DimensionsManger
from views import Vertex


class Visualizer:
    def __init__(self, displaySize: Tuple[int, int] = (1000, 1000), fps: int = 24, scale: int = .9):

        self.isScalding = False
        self.mainThreadIsRunning = True
        self.mouseThread = Thread(target=self.mouse)
        self.mainThread = Thread(target=self.main)
        pg.init()
        # self.width, self.height = 562, 1000
        self.width, self.height = displaySize[0], displaySize[1]
        self.displaySize = displaySize
        self.displaySizeHalf = (self.width // 2, self.height // 2)
        self.clock = pg.time.Clock()
        self.fps = fps
        self.scale = scale
        self.screen = pg.display.set_mode(self.displaySize)
        self.selectedVertex = 0
        self.graphManger: Final = GraphManager(*self.displaySize)
        self.dimentsManger: Final = DimensionsManger(scale,*self.displaySize)
        self.dimentsManger.scaleFactor = scale

    def main(self):
        try:
            while self.mainThreadIsRunning:
                self.events()

                self.setupEdges()
                self.setupVertices()
                self.drawEdges()
                self.drawVertices()

                self.updateDisplay()
        except Exception as E:
            self.mainThreadIsRunning = False
            raise E

    def mouse(self):
        try:
            # self.scaleVerticesDownUpToScale()
            while self.mainThreadIsRunning:
                if self.graphManger.isSelectingVertexMode:
                    self.moveSelectedVertexToMouse()
                if self.isScalding:
                    self.graphManger.scaleVertices()
                    self.isScalding = False
        except Exception as E:
            self.mainThreadIsRunning = False
            raise E

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
                elif event.key == pg.K_v:
                    self.toggleVerticesSetupMode()
                elif event.key == pg.K_e:
                    self.toggleEdgesSetupMode()

    def updateDisplay(self):
        self.clock.tick(self.fps)
        pg.display.update()
        self.screen.fill(MainColors.surfaceColor)
        moving = not self.graphManger.noVerticesIntersecting
        scaleTag = f"scale:{self.dimentsManger.scaleFactor}" if not self.isScalding else "scaling ..."
        movingTag = f"moving:{moving}"
        verticesSetupTag = f"VerticesSetup:{not self.graphManger.isVerticesSetupModeDisabled}"
        edgesSetupTag = f"Edges Setup:{not self.graphManger.isEdgesSetupModeDisabled}"
        pg.display.set_caption(f"{scaleTag},\t"
                               f"{verticesSetupTag},\t"
                               f"{edgesSetupTag},\t"
                               f"{movingTag},\t"
                               f"Selection:{self.graphManger.isSelectingVertexMode},\t"
                               f"Crazy Spanning:{self.graphManger.isCrazySpanningMode} ")

    def setupEdges(self):
        self.graphManger.setupEdges()

    def setupVertices(self):
        self.graphManger.setupVertices()

    def scaleVerticesDownUpToScale(self):
        scale = 0.1
        while scale <= self.scale:
            if not self.graphManger.noVerticesIntersecting:
                self.isScalding = True
                self.dimentsManger.scaleFactor = scale
                self.graphManger.scaleVertices()
                self.isScalding = False
                scale += .1
        self.startCrazySpanningMode()

    def startVertexSelectingMode(self, mousePos: Pos):
        self.graphManger.startVertexSelectingMode(mousePos)

    def stopVertexSelectingMode(self):
        self.graphManger.stopVertexSelectingMode()

    def startMainThread(self):
        self.mainThread.daemon = False
        self.mainThread.start()

    def startMouseThread(self):
        self.mouseThread.daemon = False
        self.mouseThread.start()

    def moveSelectedVertexToMouse(self):
        mx, my = pg.mouse.get_pos()
        self.graphManger.moveSelectedVertexTo(mx, my)

    def startCrazySpanningMode(self):
        self.graphManger.toggleCrazySpanning()

    def scaleFactorUp(self):
        self.dimentsManger.scaleFactor += .1
        self.isScalding = True

    def scaleFactorDown(self):
        if self.dimentsManger.scaleFactor > .1:
            self.dimentsManger.scaleFactor -= .1
            self.isScalding = True

    def drawEdges(self):
        for edge in self.graphManger.edges:
            self._drawEdge(edge)

    def drawVertices(self):
        for vertex in self.graphManger.vertices:
            self._drawVertex(vertex)
            # vertex.isMoved = False

    def _drawEdge(self, edge):
        pg.draw.line(self.screen, EdgesColors.default,
                     tuple(self.graphManger.verticesManger.byName(edge.start).pos),
                     tuple(self.graphManger.verticesManger.byName(edge.end).pos),
                     self.dimentsManger.EdgesDiments.width)

    def _drawVertex(self, vertex: Vertex):
        CopiedVertex = deepcopy(vertex)
        self._drawVertexCircle(CopiedVertex)
        self._drawVertexText(CopiedVertex)

    def _drawVertexText(self, vertex: Vertex):
        self.screen.blit(vertex.textImage, vertex.textPos)

    def _drawVertexCircle(self, vertex: Vertex):
        pg.draw.circle(self.screen, vertex.color, vertex.pos.location(), self.dimentsManger.VerticesDiments.radius)

    def halt(self):
        self.mainThreadIsRunning = False
        sys.exit(0)

    def addTestingGraph(self):
        graphGenerator = GraphGenerator(*self.displaySize)
        # graphHolder = self.graphGenerator.generateVerticesCanFitIn(*self.displaySize, self.dimentsManger)
        graphHolder = graphGenerator.generate2ComponentsGraph()
        self.graphManger.setupFromGraphHolder(graphHolder)

    def toggleVerticesSetupMode(self):
        self.graphManger.toggleVerticesSetupMode()

    def toggleEdgesSetupMode(self):
        self.graphManger.toggleEdgesSetupMode()


if __name__ == '__main__':
    v = Visualizer()
    v.addTestingGraph()
    v.startMainThread()
    v.startMouseThread()
