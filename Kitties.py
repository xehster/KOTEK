from pygame import *
from main import *


class Kitten(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = image.load('images/kitten_1.png')
        self.rect = self.image.get_rect()
        self.posx = 0
        self.posy = 0

    def render(self, screenie):
        self.rect.x = self.posx
        self.rect.y = self.posy
        screenie.blit(self.image, self.rect)

    def update(self, group, hero):
        hits = sprite.spritecollide(self, group, False)
        if hits:
            hero.score += 1
            self.kill()
