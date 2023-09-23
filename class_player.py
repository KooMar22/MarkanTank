# Import required modules
import pygame
from draw import *
from controls import *


# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("Images/Tank.jpg").convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.centerx = WIDTH // 2  # Set center x coordinate
        self.rect.centery = HEIGHT  # Set bottom y coordinate
        self.score = 0  # Initialize the score attribute
        self.shield = False # Initialize the shield atttribute

    # Move the sprite based on user keypresses
    def update(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0, -5)
        if keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT