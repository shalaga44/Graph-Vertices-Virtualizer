from typing import Callable, Tuple

import pygame
from pygame import display, Surface
from pygame.rect import RectType

import Colors
from DataTypes.pos import Pos
from Mangers.font_manager import FontManager


class Button:
    def __init__(self, _text: str, _pos: Pos, _width: int = None, _height: int = None):
        self._width: int = _width
        self._height: int = _height
        self._text = str(_text)
        self._pos: Pos = _pos
        textSize = self._getTextSize()
        self._setupWidthAndHeight(textSize)
        self.colorText = Colors.ButtonColors.defaultText
        # self.colorTextOnClick = Colors.ButtonColors.defaultTextOnClick
        self.colorBackground = Colors.ButtonColors.defaultBackground
        self.colorBackgroundOnClick = Colors.ButtonColors.defaultBackgroundOnClick
        self._textImage: Surface = self._creatText(_text)
        self._rect: RectType = self._createRect()
        self.action: Callable = lambda: print(f"Button {self._text}::onClick()")
        self.isClicked = False
        self.clickDurationAnim = 0
        self.clickDurationAnimLimit = 5

    def _createRect(self) -> RectType:
        rect = pygame.rect.Rect(self._pos.x, self._pos.y, self._width,
                                self._height)
        return rect

    def _drawRect(self, screen: display):
        if self.clickDurationAnim > 0:
            pygame.draw.rect(screen, self.colorBackgroundOnClick, self._rect)
            self.clickDurationAnim -= 1
        else:
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
        wTextHalf, hTextHalf = wText // 2, hText // 2
        self.textPos = (self._pos.x + (self._width // 2)) - wTextHalf, (
                self._pos.y + (self._height // 2)) - hTextHalf
        self._textImage = textImage
        return textImage

    def onClick(self):
        self.action.__call__()
        self.clickDurationAnim = self.clickDurationAnimLimit

    def setOnClick(self, func: Callable):
        self.action = func

    def _setupWidthAndHeight(self, textSize: Tuple[int, int]):
        textWidth, textHeight = textSize
        if self._width is None:
            self._width = textWidth + 20
        if self._height is None:
            self._height = textHeight + 3

    def _getTextSize(self) -> Tuple[int, int]:
        font = FontManager().font
        textWidth, textHeight = font.size(self._text)
        return textWidth, textWidth
