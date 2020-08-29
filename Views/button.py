from typing import Callable

import pygame
from pygame import display, Surface
from pygame.rect import RectType

import Colors
from DataTypes.pos import Pos
from Mangers.font_manager import FontManager


class Button:
    def __init__(self, _text: str, _pos: Pos, _width: int = 100, _height: int = 100):
        self._width: int = _width
        self._height: int = _height
        self._text = str(_text)
        self._pos: Pos = _pos
        self.colorText = Colors.MainColors.surfaceColor
        self.colorBackground = Colors.MainColors.onSurfaceColor
        self._rect: RectType = self._createRect(_pos.x, _pos.y, _width, _height)
        self._textImage: Surface = self._creatText(_text)
        self.action: Callable = lambda: print(f"Button {self._text}::onClick()")

    @staticmethod
    def _createRect(left, top, _width, height) -> RectType:
        rect = pygame.rect.Rect(left, top, _width, height)
        return rect

    def _drawRect(self, screen: display):
        pygame.draw.rect(screen, self.colorBackground, self._rect)

    def _drawText(self, screen: display):
        screen.blit(self._textImage, self.textPos)

    def draw(self, screen: display):
        self._drawRect(screen)
        self._drawText(screen)

    def _creatText(self, _text: str) -> Surface:
        font = FontManager().font
        textImage = font.render(self._text, True, self.colorText)
        wText, hText = font.size(self._text)
        self.wTextHalf, self.hTextHalf = wText // 2, hText // 2
        self.textPos = (self._pos.x + (self._width // 2)) - self.wTextHalf, (
                self._pos.y + (self._height // 2)) - self.hTextHalf
        self._textImage = textImage
        return textImage

    def onClick(self):
        self.action.__call__()

    def setOnClick(self, func: Callable):
        self.action = func
