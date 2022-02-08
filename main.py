from pygame import *
from level1 import *
from player import *
from blocks import *
from pyganim import *
from enemies import *
from random import randint
import pygame
import sys

WIN_WIDTH = 1920
WIN_HEIGHT = 1080
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BG_IMG = pygame.image.load('images/bg.png')
RUNNING = True
screen = pygame.display.set_mode(DISPLAY)


def main():
    pygame.init()
    pygame.display.set_caption('KOTEK')
    FPS = pygame.time.Clock()

    total_level_width = len(level[0]) * PLAT_WIDTH  # calcuting level width
    total_level_height = len(level) * PLAT_HEIGHT  # same but with height

    camera = Camera(camera_configure, total_level_width, total_level_height)
    attacking = False
    running = False  # not running by default
    hero = Player(55, 55)  # creating character by these coords
    left = right = False  # not walking by default
    up = False  # not jumping by default
    enm = Enemy(randint(300, 1920), randint(300, 1080), 2, 3, 150, 15)
    health = hero.health

    while RUNNING:
        entities = pygame.sprite.Group()  # all objects sprite group
        platforms = []  # hard objects
        villains = pygame.sprite.Group()  # all animated moving deadly creatures

        entities.add(hero)
        entities.add(enm)

        playergroup = pygame.sprite.Group()
        playergroup.add(hero)

        platforms.append(enm)

        villains.add(enm)

        x = y = 0

        screen.blit(BG_IMG, (0, 0))
        for e in pygame.event.get():  # e is for event
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYDOWN and e.key == K_w:
                up = True

            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

            if e.type == KEYDOWN and e.key == K_SPACE:
                attacking = True
            if e.type == KEYUP and e.key == K_SPACE:
                attacking = False

        for row in level:
            for column in row:
                if column == '-':
                    platform = Platform(x, y)  # creates Platform class example
                    entities.add(platform)  # adds it to the entities sprite group
                    platforms.append(platform)  # adds it to the platforms list

                if column == '*':
                    db = DeadlyBlock(x, y)
                    entities.add(db)
                    platforms.append(db)

                if column == '=':
                    platform4 = LongPlatform(x, y)
                    entities.add(platform4)
                    platforms.append(platform4)

                if column == '_':
                    platform8 = VeryLongPlatform(x, y)
                    entities.add(platform8)
                    platforms.append(platform8)

                x += PLAT_WIDTH
            y += PLAT_HEIGHT
            x = 0

        hero.update(left, right, up, running, platforms, attacking, health)
        villains.update(platforms, playergroup, attacking)
        FPS.tick(60)
        camera.update(hero)

        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if hero.health == 5:
            screen.blit(pygame.image.load('images/fullhp.png'), (50, 950))
        elif hero.health == 4:
            screen.blit(pygame.image.load('images/4hp.png'), (50, 950))
        elif hero.health == 3:
            screen.blit(pygame.image.load('images/3hp.png'), (50, 950))
        elif hero.health == 2:
            screen.blit(pygame.image.load('images/2hp.png'), (50, 950))
        else:
            screen.blit(pygame.image.load('images/1hp.png'), (50, 950))
        pygame.display.update()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = - l + WIN_WIDTH / 2, - t + WIN_HEIGHT / 2

    l = min(0, l)  # don't cross left border
    l = max(-(camera.width - WIN_WIDTH), l)  # same w/ right border
    t = min(0, t)  # same w/ top
    t = max(-(camera.height - WIN_HEIGHT), t)  # same w/ bottom

    return Rect(l, t, w, h)


if __name__ == '__main__':
    main()
