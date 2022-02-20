import pyganim
import pygame
from pygame import *
from main import*
import random


ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60
ENEMY_COLOR = '#66ffff'
ENEMY_IMG = pygame.image.load("images/CRYING_EYEBALL_1.png")

ENEMY_ANIM_DELAY = 100
ENEMY_ANIM = ["images/CRYING_EYEBALL_1.png", "images/CRYING_EYEBALL_2.png", "images/CRYING_EYEBALL_3.png", "images/CRYING_EYEBALL_4.png", 'images/CRYING_EYEBALL_5.png']

vec = Vector2



class Enemy(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = randint(2, 6) / 2  # Randomized velocity of the generated enemy
        self.hp = 3
        self.state = "ALIVE"

        if self.direction == 0:
            self.pos.x = 150
            self.pos.y = 500
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 500

        enemyAnim = []
        for enemyanim in ENEMY_ANIM:
            enemyAnim.append((enemyanim, ENEMY_ANIM_DELAY))

        self.enemyAnim = pyganim.PygAnimation(ENEMY_ANIM)
        self.enemyAnim.play()


    def move(self):
        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIN_WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect

    def update(self, herogroup, projectiles, attacking, kitties):
        self.enemyAnim.blit(self.image, (0, 0))
        hits = pygame.sprite.spritecollide(self, herogroup, False)
        # Activates upon either of the two expressions being true
        if hits and attacking:
            self.hp -= 1
            if self.hp < 1:
                self.state = "DEAD"
                self.kill()
                rand_num = randint(0, 100)
                if rand_num <= 100:
                    kittie = Kitten()
                    kitties.add(kittie)
                    kittie.posx = self.pos.x
                    kittie.posy = self.pos.y

                print("Enemy killed")

        projectilehits = pygame.sprite.spritecollide(self, projectiles, False)
        if projectilehits:
            self.hp -= 1
            if self.hp < 1:
                self.state = "DEAD"
                self.kill()
                rand_num = randint(0, 100)
                if rand_num <= 100:
                    kittie = Kitten()
                    kitties.add(kittie)
                    kittie.posx = self.pos.x
                    kittie.posy = self.pos.y
                print("Enemy killed by projectile")

enm = Enemy()



