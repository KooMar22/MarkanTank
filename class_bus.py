# Import required modules
import sys
import os
import pygame
from draw import *
from controls import *
from class_car import Car


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



# Define the bus class
class Bus(Car):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(resource_path("Images/bus.jpg")).convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        # The starting position is randomly generated, while the speed is 5
        self.rect = self.surf.get_rect()
        # Define health
        self.health = 2

    def update(self, player):
        # Move down
        self.rect.move_ip(0, self.speed)
        # Kill if it goes below the screen
        if self.rect.top > HEIGHT:
            self.kill()
        # Update the x-coordinate based on lane
        self.rect.centerx = self.lane * lane_distance + lane_distance // 2
        # Kill if health reaches zero and add to the score
        if self.health <= 0:
            self.kill()
            player.score += 2