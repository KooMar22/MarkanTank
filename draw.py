# Import required modules
import sys
import os
import pygame


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


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (105, 105, 102)

# Define constants for the screen width and height
WIDTH = 500
HEIGHT = 580

lane_distance = 50  # Distance between each lane
num_lanes = WIDTH // lane_distance  # Calculate the number of lanes based on width


def draw_lanes(screen, lane_distance, num_lanes):
    lane_width = 7  # Width of each lane

    for i in range(num_lanes + 1):
        lane_x = i * lane_distance  # X-coordinate

        # Draw solid lines for left, right and middle lane
        if i == 0 or i == num_lanes or i == num_lanes // 2:
            pygame.draw.line(screen, YELLOW, (lane_x, 0),
                             (lane_x, HEIGHT), lane_width)
        else:
            # Draw dashed lines for other lanes
            dash_length = 10  # Length of each dash
            gap_length = 10  # Length of each gap between dashes

            # Calculate the number of dashes and gaps based on lane width
            num_dashes = (HEIGHT // (dash_length + gap_length)) + 1

            for j in range(num_dashes):
                dash_y = j * (dash_length + gap_length)
                pygame.draw.line(
                    screen,
                    YELLOW,
                    (lane_x, dash_y),
                    (lane_x, dash_y + dash_length),
                    lane_width,
                )


def display_score(screen, player):
    # Define the font, size, bold, non-italic
    font = pygame.font.SysFont("Calibri", 25, True, False)
    # Render the text. "True" for anti-aliasing text.
    # Red color, as a true communist and regge lover.
    text = font.render("Score: " + str(player.score), True, RED)
    # Put the image of the text on the screen at 10x10
    screen.blit(text, [10, 10])

# Create the screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Markanovi Tenkići")

# Load car icons
car_icons = [resource_path("Images/Car1.jpg"),
             resource_path("Images/Car2.jpg"),
             resource_path("Images/Car3.jpg")]