from pygame.font import SysFont, init, get_default_font, Font

from SingletonMetaClass import Singleton


class FontManager(metaclass=Singleton):
    def __init__(self):
        init()
        self.font: Font = SysFont(get_default_font(), 30)
