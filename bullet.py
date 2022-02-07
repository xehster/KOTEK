from main import *
import pygame


class FireBall(pygame.sprite.Sprite):
    def __init__(self, direction, x, y):
        super().__init__()
        self.direction = direction
        if self.direction == "RIGHT":
            self.image = pygame.image.load('images/bullet.png')
        else:
            self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 50

    def fire(self, screentoblit):
        if self.direction == "RIGHT":
            self.image = pygame.image.load("images/bullet.png")
            screentoblit.blit(self.image, self.rect)
        else:
            self.image = pygame.image.load("images/bullet.png")
            screentoblit.blit(self.image, self.rect)

        if self.direction == "RIGHT":
            self.rect.move_ip(12, 0)
        else:
            self.rect.move_ip(-12, 0)
