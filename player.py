import blocks
import enemies
from main import *
from pygame import *
import pyganim
from bullet import *

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


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.vel_x = 0  # velocity, 0 = idle
        self.vel_y = 0  # same but vertical
        self.start_x = x  # default position after restart
        self.start_y = y  # same but vertical
        self.onGround = False  # is char stands on a solid ground?
        self.image = char_idle_static
        self.rect = Rect(x, y, CHAR_WIDTH, CHAR_HEIGHT)
        self.image.set_colorkey(Color(CHAR_COLOR))  # makes bg transparent

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

    def update(self, left, right, up, running, platforms, shooting):
        if up:
            if self.onGround:
                self.vel_y = -CHAR_JUMP_POWER  # character can jump only while on ground
                if running and (left or right):  # if acc and moving
                    self.vel_y -= CHAR_JUMP_ACC  # then jump power acc
                self.image.fill(Color(CHAR_COLOR))
                self.AnimJump.blit(self.image, (0, 0))

        if left:
            self.vel_x = -CHAR_SPEED
            self.image.fill(Color(CHAR_COLOR))
            if running:
                self.vel_x -= CHAR_MOVE_ACC  # acceleration
                if not up:  # and not jumping
                    self.AnimLeftTurbo.blit(self.image, (0, 0))  # anim acc
            if up:  # if jumping
                self.AnimJumpLeft.blit(self.image, (0, 0))
            else:  # if not running
                self.AnimLeft.blit(self.image, (0, 0))
                if not up:  # and not jumping
                    self.AnimLeft.blit(self.image, (0, 0))

        if right:
            self.vel_x = CHAR_SPEED
            self.image.fill(Color(CHAR_COLOR))
            if shooting:
                self.shoot()
            if running:
                self.vel_x += CHAR_MOVE_ACC
                if not up:
                    self.AnimRightTurbo.blit(self.image, (0, 0))
            if up:
                self.AnimJumpRight.blit(self.image, (0, 0))
            else:
                self.AnimRight.blit(self.image, (0, 0))
                if not up:
                    self.AnimRight.blit(self.image, (0, 0))

        if not (left or right):
            self.vel_x = 0
            if not up:
                self.image.fill(Color(CHAR_COLOR))
                self.AnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.vel_y += GRAVITY

        self.onGround = False  # dunno if the char is on the ground

        self.rect.y += self.vel_y
        self.collide(0, self.vel_y, platforms)

        self.rect.x += self.vel_x  # moving char using vel
        self.collide(self.vel_x, 0, platforms)

    def collide(self, vel_x, vel_y, platforms):
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
                    self.die()

    def die(self):
        time.wait(500)
        self.teleport(self.start_x, self.start_y)  # teleports to default coords

    def teleport(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        entities.add(bullet)
        platforms.append(bullet)


