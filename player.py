import blocks
import enemies
from main import *
from pygame import *
import pyganim
import pygame
from pygame import math


CHAR_SPEED = 15
CHAR_JUMP_POWER = 30
GRAVITY = 1.5
CHAR_JUMP_ACC = 5
CHAR_MOVE_ACC = 5

CHAR_WIDTH = 100
CHAR_HEIGHT = 110
CHAR_COLOR = '#333333'


char_idle_static = pygame.image.load('images/idle_1.png')
ANIM_DELAY = 100  # animation change rate
ANIM_TURBO_DELAY = 50

ANIM_RIGHT = ['images/r_1.png', 'images/r_2.png', 'images/r_3.png', 'images/r_4.png']
ANIM_LEFT = ['images/l_1.png', 'images/l_2.png', 'images/l_3.png', 'images/l_4.png']
ANIM_JUMP = ['images/idle_1.png']
ANIM_JUMP_RIGHT = ['images/j_r.png']
ANIM_JUMP_LEFT = ['images/j_l.png']
ANIM_STAY = ['images/idle_1.png', 'images/idle_2.png', 'images/idle_3.png', 'images/idle_4.png']
SIMPLE_SHOT_IMG = pygame.image.load('images/bullet.png')
ANIM_SHOOTING_RIGHT = ['images/attackr.png']
ANIM_SHOOTING_LEFT = ['images/attackl.png']
ANIM_MELEE_LEFT = ['images/melee_l_1.png', 'images/melee_l_2.png', 'images/melee_l_3.png', 'images/melee_l_4.png']
ANIM_MELEE_RIGHT = ['images/melee_r_1.png', 'images/melee_r_2.png', 'images/melee_r_3.png', 'images/melee_r_4.png']

vec = pygame.math.Vector2

class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.vel_x = 0  # velocity, 0 = idle
        self.vel_y = 0  # same but vertical
        self.onGround = False  # is char stands on a solid ground?
        self.pos = vec((55, 1000))
        self.image = char_idle_static
        self.rect = Rect(self.pos.x, self.pos.y, CHAR_WIDTH, CHAR_HEIGHT)
        self.image.set_colorkey(Color(CHAR_COLOR))  # makes bg transparent
        self.direction = 'RIGHT'
        self.attacking = False
        self.attack_frame = 0
        self.health = 5
        # right animation

        Anim = []
        AnimTurbo = []

        for anim in ANIM_RIGHT:
            Anim.append((anim, ANIM_DELAY))
            AnimTurbo.append((anim, ANIM_TURBO_DELAY))
        self.AnimRight = pyganim.PygAnimation(Anim)
        self.AnimRight.play()
        self.AnimRightTurbo = pyganim.PygAnimation(AnimTurbo)
        self.AnimRightTurbo.play()

        # left animation

        Anim = []
        AnimTurbo = []

        for anim in ANIM_LEFT:
            Anim.append((anim, ANIM_DELAY))
            AnimTurbo.append((anim, ANIM_TURBO_DELAY))
        self.AnimLeft = pyganim.PygAnimation(Anim)
        self.AnimLeft.play()
        self.AnimLeftTurbo = pyganim.PygAnimation(AnimTurbo)
        self.AnimLeftTurbo.play()

        # idle anim

        self.AnimStay = pyganim.PygAnimation(ANIM_STAY)
        self.AnimStay.play()
        self.AnimStay.blit(self.image, (0, 0))  # staying by default

        # jump left anim

        self.AnimJumpLeft = pyganim.PygAnimation(ANIM_JUMP_LEFT)
        self.AnimJumpLeft.play()

        # jump right anim

        self.AnimJumpRight = pyganim.PygAnimation(ANIM_JUMP_RIGHT)
        self.AnimJumpRight.play()

        # jump up anim

        self.AnimJump = pyganim.PygAnimation(ANIM_JUMP)
        self.AnimJump.play()

        # shooting anim right

        self.AnimShootingRight = pyganim.PygAnimation(ANIM_SHOOTING_RIGHT)
        self.AnimShootingRight.play()

        # shooting anim left

        self.AnimShootingLeft = pyganim.PygAnimation(ANIM_SHOOTING_LEFT)
        self.AnimShootingLeft.play()

        # melee anim right
        Anim = []
        for anim in ANIM_MELEE_RIGHT:
            Anim.append((anim, ANIM_DELAY))
        self.AnimMeleeRight = pyganim.PygAnimation(ANIM_MELEE_RIGHT)
        self.AnimMeleeRight.play()

        # melee anim left
        Anim = []
        for anim in ANIM_MELEE_LEFT:
            Anim.append((anim, ANIM_DELAY))
        self.AnimMeleeLeft = pyganim.PygAnimation(ANIM_MELEE_LEFT)
        self.AnimMeleeLeft.play()

    def update(self, left, right, up, running, platforms, attacking, health):
        if up:
            if self.onGround:
                self.vel_y = -CHAR_JUMP_POWER  # character can jump only while on ground
                if running and (left or right):  # if acc and moving
                    self.vel_y -= CHAR_JUMP_ACC  # then jump power acc
                self.image.fill(Color(CHAR_COLOR))
                self.AnimJump.blit(self.image, (0, 0))
                if attacking:
                    self.AnimMeleeLeft.blit(self.image, (0, 0))
            if attacking:
                self.AnimMeleeLeft.blit(self.image, (0, 0))

        if left:
            self.direction = "LEFT"
            self.vel_x = -CHAR_SPEED
            self.image.fill(Color(CHAR_COLOR))
            if attacking and not running and not up:
                self.AnimMeleeLeft.blit(self.image, (0, 0))
            if running and not attacking:
                self.vel_x -= CHAR_MOVE_ACC  # acceleration
                if not up:  # and not jumping
                    self.AnimLeftTurbo.blit(self.image, (0, 0))  # anim acc
            if attacking and running:
                self.vel_x -= CHAR_MOVE_ACC
                self.AnimMeleeLeft.blit(self.image, (0, 0))
            if up and not attacking:  # if jumping
                self.AnimJumpLeft.blit(self.image, (0, 0))
            if attacking and up:
                self.AnimMeleeLeft.blit(self.image, (0, 0))
            if not up and not running and not attacking:  # if not running
                self.AnimLeft.blit(self.image, (0, 0))
                if not up:  # and not jumping
                    self.AnimLeft.blit(self.image, (0, 0))

        if right:
            self.direction = "RIGHT"
            self.vel_x = CHAR_SPEED
            self.image.fill(Color(CHAR_COLOR))
            if attacking and not running and not up:
                self.AnimMeleeRight.blit(self.image, (0, 0))
            if running and not attacking:
                self.vel_x += CHAR_MOVE_ACC
                if not up:
                    self.AnimRightTurbo.blit(self.image, (0, 0))
            if attacking and running:
                self.vel_x += CHAR_MOVE_ACC
                self.AnimMeleeLeft.blit(self.image, (0, 0))
            if up and not attacking:
                self.AnimJumpRight.blit(self.image, (0, 0))
            if up and attacking:
                self.AnimMeleeLeft.blit(self.image, (0, 0))
            if not up and not running and not attacking:
                self.AnimRight.blit(self.image, (0, 0))

        if not (left or right):
            self.vel_x = 0
            if attacking and up:
                if self.direction == "RIGHT":
                    self.AnimMeleeRight.blit(self.image, (0, 0))
                else:
                    self.AnimMeleeLeft.blit(self.image, (0, 0))
            if not up and not attacking:
                self.image.fill(Color(CHAR_COLOR))
                self.AnimStay.blit(self.image, (0, 0))
            if not up and attacking:
                if self.direction == "LEFT":
                    self.AnimMeleeLeft.blit(self.image, (0, 0))
                else:
                    self.AnimMeleeRight.blit(self.image, (0, 0))
        if not self.onGround:
            self.vel_y += GRAVITY

        self.onGround = False  # dunno if the char is on the ground

        self.rect.y += self.vel_y
        self.collide(0, self.vel_y, platforms, attacking)

        self.rect.x += self.vel_x  # moving char using vel
        self.collide(self.vel_x, 0, platforms, attacking)

    def collide(self, vel_x, vel_y, platforms, attacking):
        for p in platforms:

            if sprite.collide_rect(self, p):  # if character meets platform

                if vel_x > 0:  # if moves to the right
                    self.rect.right = p.rect.left  # then doesn't move to the right (meets and stops moving)

                if vel_x < 0:
                    self.rect.left = p.rect.right

                if vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vel_y = 0

                if vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

                if isinstance(p, blocks.DeadlyBlock) or isinstance(p, enemies.Enemy):  # char dies if touches deadly block
                    if not attacking:
                        self.health -= 1
                    if self.health < 1:
                        self.die()
                        self.health = 5

    def die(self):
        time.wait(500)
        self.teleport(55, 1000)  # teleports to default coords

    def teleport(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y

    def fireball(self, group):
        fireball = FireBall(self)
        group.add(fireball)



hero = Player()
health = hero.health


class FireBall(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.image = None
        self.direction = player.direction
        if self.direction == "RIGHT":
            self.image = pygame.image.load('images/fireball_r.png')
        elif self.direction == "LEFT":
            self.image = pygame.image.load('images/fireball_l.png')

        self.rect = self.image.get_rect(center = player.rect.center)

    def render(self, screenie, cam):
        screenie.blit(self.image, cam.apply(self))

    def update(self, group, screenie):

        hits = pygame.sprite.spritecollideany(self, group)
        if (self.rect.x - hero.rect.x) < -1000 or (self.rect.x - hero.rect.x) > 1000:
            self.kill()
        if hits:
            self.kill()
        if self.direction == "RIGHT":
            self.rect.move_ip(50, 0)
        elif self.direction == "LEFT":
            self.rect.move_ip(-50, 0)
