# Import required modules
import os
import sys
import pygame
from draw import BLACK
from pygame.locals import RLEACCEL


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller.
    URL: https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2  # Adjust to MEIPASS2 if not working
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Define the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.surf = pygame.image.load(resource_path("Images/tank_bullet3.jpg")).convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(player_rect.centerx, player_rect.top))

    def update(self, player, enemies=None):  
        # Move the bullet up 5 pixels
        self.rect.move_ip(0, -5)

        # Check if bullet collides with enemies
        if enemies:
            collided_enemies = pygame.sprite.spritecollide(
                self, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 1
                self.kill()
                break