# Import required modules
import os
import sys
import pygame
from random import randint
from draw import *
from controls import *
from class_player import Player
from class_car import Car
from class_bus import Bus
from class_bullet import Bullet


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


# Initialize pygame
pygame.init()
pygame.mixer.init()


# Fonts
END_GAME_FONT = pygame.font.SysFont("Calibri", 30, True, True)


def display_welcome_message(message):
    screen.fill(BLACK)
    lines = [line.strip() for line in message.split("\n")]
    line_height = END_GAME_FONT.get_height()
    y_position = (HEIGHT - line_height * len(lines)) // 2

    for line in lines:
        line_text = END_GAME_FONT.render(line, 1, YELLOW)
        x_position = (WIDTH - line_text.get_width()) // 2
        screen.blit(line_text, (x_position, y_position))
        y_position += line_height

    pygame.display.update()

    # Shorter time delay for the welcome message
    pygame.time.delay(100)


def display_end_message(message):
    pygame.time.delay(2500)
    screen.fill(BLACK)
    lines = [line.strip() for line in message.split("\n")]
    line_height = END_GAME_FONT.get_height()
    y_position = (HEIGHT - line_height * len(lines)) // 2

    for line in lines:
        line_text = END_GAME_FONT.render(line, 1, YELLOW)
        x_position = (WIDTH - line_text.get_width()) // 2
        screen.blit(line_text, (x_position, y_position))
        y_position += line_height

    pygame.display.update()


def add_enemy(event, enemies, all_sprites):
    # Add a new enemy?
    if event.type == ADDENEMY:
        # Create the new enemy and add it to the sprite groups
        if not paused:  # Add enemies only if the game is not paused
            if randint(1, 10) >= 5:
                new_enemy = Car()
                new_enemy.generate_new_car()
            else:
                new_enemy = Bus()
                new_enemy.generate_new_car()  # Generate new bus instead of car
            # Check overlap
            while pygame.sprite.spritecollideany(new_enemy, enemies):
                # Generate new position until no overlap
                if isinstance(new_enemy, Car):
                    new_enemy.generate_new_car()
                else:
                    new_enemy.generate_new_car()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


def handle_collisions(player, enemies, bullets):
    collided_enemies = pygame.sprite.spritecollide(player, enemies, True)
    for enemy in collided_enemies:
        pygame.time.delay(1000)
        return False

    for bullet in bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            enemy.health -= 1
            bullets.remove(bullet)
            bullet.kill()
            break

    return True


# Load music and sound files
crash_sound = pygame.mixer.Sound(resource_path("Sounds/Crash.ogg"))
bullet_sound = pygame.mixer.Sound(resource_path("Sounds/bullet.ogg"))
hit_sound = pygame.mixer.Sound(resource_path("Sounds/hit.ogg"))
music = pygame.mixer.music.load(resource_path("Sounds/Druze_Tito_reggae.ogg"))

# Ensure that the song keeps looping
pygame.mixer.music.play(-1)

# Set the base volume for all sounds
crash_sound.set_volume(0.5)

# Creating a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Instantiate player.
player = Player()

# List of each bullet
bullets = []

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


def reset_game():
    global score, player, enemies, lost, waiting
    score = 0  # Reset the score
    player = Player()
    all_sprites.empty()
    all_sprites.add(player)
    enemies.empty()
    lost = False
    waiting = False


def game():
    global game_over, paused, lost, waiting, bullets
    FPS = 30
    clock = pygame.time.Clock()
    game_over = False
    paused = False

    # Reset the game flag when starting a new game
    lost = False
    
    while not game_over:
        clock.tick(FPS)
        
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user click the close button? If so, quit the game
            if event.type == QUIT:
                game_over = True
            
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the ESCAPE key? If so, quit the game
                if event.key == K_ESCAPE:
                    game_over = True

                if event.key == K_TAB:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                        player.speed = 0  # Stop the player
                        for enemy in enemies:
                            enemy.speed = 0  # Stop enemies
                    else:
                        pygame.mixer.music.unpause()
                        player.speed = 5  # Move player again
                        for enemy in enemies:
                            enemy.speed = 5  # Move enemies again

                if not paused:
                    if event.key == K_SPACE:
                        # Did the user fire a bullet?
                        bullet = Bullet(player.rect)
                        all_sprites.add(bullet)
                        bullets.append(bullet)
                        bullet_sound.play()  # Play bullet sound here

            add_enemy(event, enemies, all_sprites)

        if not paused:
            # Get the set of keys pressed and check for user input
            keys = pygame.key.get_pressed()
            player.update(keys)

        # Calculate mechanics for each bullet
        for bullet in bullets:
            bullet.update(player)

        # Remove bullets that have moved off the screen
        bullets = [bullet for bullet in bullets if bullet.rect.bottom > 0]

        # Move and update all sprites
        for entity in all_sprites:
            if entity != player:
                entity.update(player)

        # Check if any enemies have collided with the player
        if not paused:  # Check collisions only if the game is not paused
            if pygame.sprite.spritecollideany(player, enemies):
                player.kill()
                crash_sound.play()

                message = f"""You have LOST!
                                Press ENTER if you want to play again,
                                or press \"ESCAPE\" if you want to quit."""

                display_end_message(message)

                # Wait for player to click or press ESCAPE
                waiting = True
                lost = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN and lost:
                                reset_game()
                                waiting = False
                                game_over = False
                            elif event.key == K_ESCAPE:
                                game_over = True
                                waiting = False
            else:
                handle_collisions(player, enemies, bullets)

        # Fill the scene with gray color
        screen.fill(GRAY)

        # Fill the screen with yellow lanes
        draw_lanes(screen, lane_distance, num_lanes)

        # Draw all sprites except player
        for entity in all_sprites:
            if entity != player:
                screen.blit(entity.surf, entity.rect)

        # Draw the player sprite on top
        screen.blit(player.surf, player.rect)

        # Display the score
        display_score(screen, player)

        # Update everything to the display
        pygame.display.update()


    # Quit pygame and mixer
    pygame.mixer.quit()
    pygame.quit()


def main():
    global game_over, message
    game_over = False

    # Display the welcome message
    message = """Welcome to the MarkanTank game!
                Try to shoot incoming enemies
                with your little tank.
                You receive 1 score for car,
                and 2 for bus destroyed.
                Move your car with arrow keys,
                pause with "TAB" and
                shoot with "SPACE" key.
                Press "ENTER" to start the game."""
    display_welcome_message(message)

    while not game_over:
        # Wait for the player to press ENTER
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    waiting = False
                    game_over = False
                elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_over = True
                    waiting = False

        if not game_over:
            game()

    pygame.quit()
    pygame.mixer.quit()


if __name__ == "__main__":
    main()