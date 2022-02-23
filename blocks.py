from pygame import *


PLAT_WIDTH = 50
PLAT_HEIGHT = 50
PLAT_COLOR = '#00ff00'
PLAT_IMG = image.load('images/SHROOM_BLOCK.png')
BIG_HOUSE = image.load('images/big_house_painted.png')
KIOSK = image.load('images/kiosk.png')
MID_HOUSE = image.load('images/house_painted.png')
HUGE_HOUSE = image.load('images/huge_house.png')
CAR_IMAGE = image.load('images/pink_car.png')
CLUB_IMAGE = image.load('images/club.png')

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = PLAT_IMG
        self.rect = Rect(x, y, 40, 40)


class DeadlyBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load('images/glowing_shrooms_1.png')


class BigHouse(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = BIG_HOUSE
        self.rect = Rect(x, y, PLAT_WIDTH + 250, PLAT_HEIGHT)


class Kiosk(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = KIOSK
        self.rect = Rect(x, y, PLAT_WIDTH + 250, PLAT_HEIGHT)


class MidHouse(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = MID_HOUSE
        self.rect = Rect(x, y, PLAT_WIDTH + 250, PLAT_HEIGHT)


class HugeHouse(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = HUGE_HOUSE
        self.rect = Rect(x, y, PLAT_WIDTH + 800, PLAT_HEIGHT)


class Car(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = CAR_IMAGE
        self.rect = Rect(x, y, PLAT_WIDTH + 150, PLAT_HEIGHT)

class Club(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = CLUB_IMAGE
        self.rect = Rect(x, y, PLAT_WIDTH + 150, PLAT_HEIGHT)



