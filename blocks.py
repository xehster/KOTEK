from pygame import *


PLAT_WIDTH = 50
PLAT_HEIGHT = 50
PLAT_COLOR = '#00ff00'
PLAT_IMG = image.load('images/SHROOM_BLOCK.png')
PLAT_IMG_4 = image.load('images/longplatform1.png')
PLAT_IMG_8 = image.load('images/longplatform2.png')


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = PLAT_IMG
        self.rect = Rect(x, y, 40, 40)


class DeadlyBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load('images/glowing_shrooms_1.png')


class LongPlatform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = PLAT_IMG_4
        self.rect = Rect(x, y, PLAT_WIDTH + 150, PLAT_HEIGHT - 30)

class VeryLongPlatform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = PLAT_IMG_8
        self.rect = Rect(x, y, PLAT_WIDTH + 350, PLAT_HEIGHT - 30)


