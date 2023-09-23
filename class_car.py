# Import required modules
import pygame
from random import randint, choice
from draw import *
from controls import *


# Define the enemy car class
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_icon = choice(car_icons)
        self.surf = pygame.image.load(self.car_icon).convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        # The starting position is randomly generated, while the speed is 5
        self.rect = self.surf.get_rect()
        self.speed = 5
        # Determine the lane based on x-axis
        self.lane = self.rect.centerx // lane_distance
        # Define health
        self.health = 1

    def generate_enemy_position(self):
        lane = randint(0, num_lanes - 1)  # Generate random lane
        lane_x = lane * lane_distance  # Calculate x-coordinate based on lane
        return lane_x

    def generate_new_car(self):
        # Determine the lane based on x-axis
        self.lane = self.generate_enemy_position() // lane_distance
        self.rect.center = (self.lane * lane_distance + lane_distance // 2,
                            randint(-100, -20))

    # Move the sprite based on speed and lane
    # Remove the sprite when it passes the bottom edge of the screen
    def update(self, player):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()
        # Update the x-coordinate based on lane
        self.rect.centerx = self.lane * lane_distance + lane_distance // 2
        if self.health <= 0:
            self.kill()
            player.score += 1