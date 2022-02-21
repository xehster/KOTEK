from pygame import *
from level1 import *
from player import *
from blocks import *
from pyganim import *
from enemies import *
from random import randint
import pygame
import sys
from Kitties import *


WIN_WIDTH = 1920
WIN_HEIGHT = 1080
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BG_IMG = pygame.image.load('images/bg_fire.png')
RUNNING = True
screen = pygame.display.set_mode(DISPLAY)


def main():
    pygame.init()
    pygame.display.set_caption('KOTEK')
    FPS = pygame.time.Clock()

    total_level_width = len(level[0]) * PLAT_WIDTH  # calcuting level width
    total_level_height = len(level) * PLAT_HEIGHT  # same but with height

    camera = Camera(camera_configure, total_level_width, total_level_height)
    attacking = hero.attacking
    running = False  # not running by default
    left = right = False  # not walking by default
    up = False  # not jumping by default
    enemies = pygame.sprite.Group()  # for enemies (to move them)
    enemies.add(enm)
    heroprojectiles = pygame.sprite.Group()
    kitties = pygame.sprite.Group()

    while RUNNING:
        entities = pygame.sprite.Group()  # all objects sprite group
        platforms = []  # hard objects
        herogroup = pygame.sprite.Group()  # main char group
        herogroup.add(hero)  # to configure collision and update
        entities.add(hero)  # to blitw
        #entities.add(enm)  # to blit
        platforms.append(enm)

        if enm not in enemies:
            platforms.remove(enm)

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

            if e.type == KEYDOWN and e.key == K_f:
                hero.fireball(heroprojectiles)


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

                if column == 'b':
                    bighouse = BigHouse(x, y)
                    entities.add(bighouse)
                    platforms.append(bighouse)

                if column == 'k':
                    kiosk = Kiosk(x, y)
                    entities.add(kiosk)
                    platforms.append(kiosk)

                if column == 'm':
                    midhouse = MidHouse(x, y)
                    entities.add(midhouse)
                    platforms.append(midhouse)

                x += PLAT_WIDTH
            y += PLAT_HEIGHT
            x = 0


        for projectile in heroprojectiles:
            projectile.render(screen, camera)
            projectile.update(enemies, screen)
            print(projectile.rect)
        enemies.update(herogroup, heroprojectiles, attacking, kitties)
        herogroup.update(left, right, up, running, platforms, attacking, health)


        # gamedev assistance data



        # moving all mobs


        # updating every sprite image


        for e in entities:
            screen.blit(e.image, camera.apply(e))

        for enem in enemies:
            screen.blit(enem.image, camera.apply(enem))
            enem.move()

        for kit in kitties:
            kit.render(screen)
            kit.update(herogroup, hero)
        #  hp visual update

        score = pygame.font.SysFont(None, 50)
        scoresurface = score.render(str(hero.score), False, (0, 0, 0))
        screen.blit(scoresurface, (100, 50))
        if hero.health == 5:
            screen.blit(pygame.image.load('images/fullhp.png'), (50, 980))
        elif hero.health == 4:
            screen.blit(pygame.image.load('images/4hp.png'), (50, 980))
        elif hero.health == 3:
            screen.blit(pygame.image.load('images/3hp.png'), (50, 980))
        elif hero.health == 2:
            screen.blit(pygame.image.load('images/2hp.png'), (50, 980))
        else:
            screen.blit(pygame.image.load('images/1hp.png'), (50, 980))

        if enm.hp == 3:
            screen.blit(pygame.image.load('images/3hp.png'), (50, 900))
        elif enm.hp == 2:
            screen.blit(pygame.image.load('images/2hp.png'), (50, 900))
        elif enm.hp == 1:
            screen.blit(pygame.image.load('images/1hp.png'), (50, 900))
        FPS.tick(60)
        camera.update(hero)
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
    l = max(-(camera.width - WIN_WIDTH), l)  # same wf/ right border
    t = min(0, t)  # same w/ top
    t = max(-(camera.height - WIN_HEIGHT), t)  # same w/ bottom

    return Rect(l, t, w, h)


if __name__ == '__main__':
    main()
