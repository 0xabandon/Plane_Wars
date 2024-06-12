import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,enemy_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./image/enemy0.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("./image/enemy0_down1.png").convert_alpha(), \
            pygame.image.load("./image/enemy0_down2.png").convert_alpha(), \
            pygame.image.load("./image/enemy0_down3.png").convert_alpha(), \
            pygame.image.load("./image/enemy0_down4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = enemy_size[0], enemy_size[1]
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), \
            randint(-5 * self.height,0)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)

class MidEnemy(pygame.sprite.Sprite):
    def __init__(self,enemy_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./image/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("./image/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("./image/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("./image/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("./image/enemy1_down4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = enemy_size[0], enemy_size[1]
        self.speed = 1
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), \
            randint(-10 * self.height,-self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self,enemy_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("./image/enemy2.png").convert_alpha()
        self.image2 = pygame.image.load("./image/enemy2_n2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("./image/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("./image/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("./image/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("./image/enemy2_down4.png").convert_alpha(), \
            pygame.image.load("./image/enemy2_down5.png").convert_alpha(), \
            pygame.image.load("./image/enemy2_down6.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = enemy_size[0], enemy_size[1]
        self.speed = 1
        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.mask = pygame.mask.from_surface(self.image2)
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), \
            randint(-15 * self.height,-5 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)