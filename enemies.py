from pyganim import *
from pygame import *
from main import*

ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60
ENEMY_COLOR = '#66ffff'
ENEMY_IMG = pygame.image.load("images/CRYING_EYEBALL_1.png")

ENEMY_ANIM_DELAY = 100
ENEMY_ANIM = ["images/CRYING_EYEBALL_1.png", "images/CRYING_EYEBALL_2.png", "images/CRYING_EYEBALL_3.png", "images/CRYING_EYEBALL_4.png", 'images/CRYING_EYEBALL_5.png']

class Enemy(sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y, pathlength_x, pathlenght_y):  # coords, enemy's velocity x/y, and how far enemy can go one way in x or y
        sprite.Sprite.__init__(self)
        self.image = ENEMY_IMG
        #self.image.fill(Color(ENEMY_COLOR))
        self.rect = Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image.set_colorkey(Color(ENEMY_COLOR))
        self.start_x = x
        self.start_y = y
        self.pathlenght_x = pathlength_x
        self.pathlenght_y = pathlenght_y
        self.vel_x = vel_x  # 0 = enemy stops
        self.vel_y = vel_y  # same but vertical
        Anim = []
        for anim in ENEMY_ANIM:
            Anim.append((anim, ENEMY_ANIM_DELAY))
        self.Anim = PygAnimation(Anim)
        self.Anim.play()

    def update(self, platforms, playergroup, attacking):
        #self.image.fill(Color(ENEMY_COLOR))
        self.Anim.blit(self.image, (0, 0))

        self.rect.y += self.vel_y
        self.rect.x += self.vel_x

        self.collide(platforms)
        hits = pygame.sprite.spritecollide(self, playergroup, False)

        if hits and attacking:
            self.kill()
            f = pygame.font.SysFont("arial.ttf", 100)
            g = f.render(str('ENEMYKILLED'), True, (123, 255, 0))
            screen.blit(g, (100, 100))


        if abs(self.start_x - self.rect.x) > self.pathlenght_x:  # if the enemy passed their full path then they have to go back
            self.vel_x = - self.vel_x
        if abs(self.start_y - self.rect.y) > self.pathlenght_y:
            self.vel_y = -self.vel_y

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # if collide - go back
                self.vel_x = - self.vel_x
                self.vel_y = - self.vel_y


