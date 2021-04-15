import pygame
import sys
import time
import os

# Initializing pygame modules :-

pygame.init()

# Setting screen width and height :-

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Setting font style :-

font = pygame.font.SysFont("Arial", 60)

# Initialising clock :-

clock = pygame.time.Clock()

# Initialising game window :-

game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting caption :-

pygame.display.set_caption("Dragon Game by Aritra")

# Getting the previous high score :-

with open('high_score.txt', 'r') as z:
    high_score = z.read()

# Configuring images :-

welcome_image = pygame.image.load('gallery/sprites/welcome_dragon.jpg')
welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
back_image = pygame.image.load('gallery/sprites/background.png')
back_image = pygame.transform.scale(back_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
game_over = pygame.image.load('gallery/sprites/game_over.png')
game_over = pygame.transform.scale(game_over, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
life = pygame.image.load('gallery/sprites/life.png')
life = pygame.transform.scale(life, (20, 20))

# Game Sprites :-

GAME_SPRITES = {'dino': pygame.image.load('gallery/sprites/dino.png').convert_alpha(),
                'dragon': pygame.image.load('gallery/sprites/dragon.png').convert_alpha(),
                'background': back_image,
                'welcome': welcome_image,
                'game-over': game_over,
                'life': life
                }

# Game sounds :-

GAME_SOUNDS = {
    'die': pygame.mixer.Sound('gallery/Audio/die.wav'),
    'hit': pygame.mixer.Sound('gallery/Audio/hit.wav'),
    'point': pygame.mixer.Sound('gallery/Audio/point.wav'),
    'wing': pygame.mixer.Sound('gallery/Audio/wing.wav')
}


# Shows text on the screen :-

def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


# Displays welcome screen :-

def welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_game()
        game_window.blit(GAME_SPRITES['welcome'], (0, 0))
        pygame.display.update()
        clock.tick(60)


# Checks if there is a collision :-

def is_collide(player_x, player_y, attacker_list):
    collision = 0
    for x, y in attacker_list:
        if abs(player_x - x) < 20 and abs(player_y - y) < 90:
            collision += 1
            break
    if collision >= 1:
        return True
    else:
        return False


# Displays dragons on the screen :-

def dragons(dragon_list):
    for x, y in dragon_list:
        game_window.blit(GAME_SPRITES['dragon'], (x, y))


# Displays the game_over screen :-

def game_over(score):
    # Writing the current score in the file :-
    with open('high_score.txt', 'w') as f:
        f.write(str(score))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
        game_window.blit(GAME_SPRITES['game-over'], (0, 0))
        pygame.display.update()


# Displays the number of lives available :-

def show_life(coordinates):
    for x, y in coordinates:
        game_window.blit(GAME_SPRITES['life'], (x, y))


# Main Game :-

def main_game():
    # Game variables :-

    global high_score
    t = time.time()
    x = time.time()
    cross = True
    score = 0
    player_x = 40
    player_y = 468
    attacker_x = SCREEN_WIDTH
    attacker_y = 390
    vel_attacker_x = -5
    player_jumped = False
    jump_count = 10
    timer = False
    delay = 1
    vel_x = 0
    vel_y = 0
    limit = -800
    life_coordinates = [[40, 40], [60, 40], [80, 40]]
    life_deducted = True
    life_deduction_delay = delay

    # Creating a high_score file if not exists :-

    if not os.path.exists('high_score.txt'):
        with open('high_score.txt', 'w') as f:
            f.write('0')

    # Running the game_loop :-

    while True:

        # Checking for the events :-

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_jumped = True
                    GAME_SOUNDS['wing'].play()
                elif event.key == pygame.K_RIGHT:
                    vel_x += 5
                elif event.key == pygame.K_LEFT:
                    vel_x -= 5
            if event.type == pygame.KEYUP:
                vel_x = 0
                vel_y = 0

        # Stores the co-ordinates of the attacker :-

        attacker = [[attacker_x, attacker_y]]

        # Check for the current score and increases difficulty according to it :-
        if score > 10:
            attacker.append([attacker_x + 500, attacker_y])
        if score > 20:
            vel_attacker_x = - 6
        if score > 30:
            attacker.append([attacker_x + 1000, attacker_y])
            limit = -1000
        if score > 40:
            vel_attacker_x = -8
        if score > 50:
            attacker.append([attacker_x + 1500, attacker_y])
            limit = -1500
        if score > 70:
            vel_attacker_x = -10

        # Increases the co-ordinates of the player:-
        player_x += vel_x
        player_y += vel_y

        # Shows the background :-

        game_window.blit(GAME_SPRITES['background'], (0, 0))

        # Displays the player on the screen :-

        game_window.blit(GAME_SPRITES['dino'], (player_x, player_y))

        # Increases the x co-ordinate of the attacker :-

        attacker_x += vel_attacker_x

        # Places the dragon(attacker) in the starting position after it goes out of the screen :-
        if attacker_x <= limit:
            attacker_x = SCREEN_WIDTH + 100

        # Re positioning the player after it goes out of the screen :-
        if player_x == -200:
            player_x = SCREEN_WIDTH - 90

        # Jump the player :-

        if player_jumped:
            if jump_count >= -10:
                player_y -= (jump_count * abs(jump_count)) * 0.5
                player_x += 10
                jump_count -= 1
            else:
                jump_count = 10
                player_jumped = False

        # Increases the score :-

        if cross:
            for j, k in attacker:
                if abs(player_x - j) < 145:
                    score += 1
                    x = time.time()
                    timer = True
                    cross = False
                    GAME_SOUNDS['point'].play()

        # Updates the boolean value of cross and life_deducted after a certain time :-
        if timer:
            if time.time() - x >= delay:
                cross = True
            if time.time() - t >= life_deduction_delay:
                life_deducted = True

        # Checks if collision happened and reduces 1 life :-

        if is_collide(player_x, player_y, attacker) and life_deducted:
            t = time.time()
            del life_coordinates[len(life_coordinates) - 1]
            life_deducted = False

        # Checks the number of lives available and if it is 0 calls the game_over function.

        if len(life_coordinates) == 0:
            GAME_SOUNDS['hit'].play()
            game_over(score)
            GAME_SOUNDS['die'].play()

        # Passes the co_ordinates of the dragon(attacker) to the dragon function for displaying :-
        dragons(attacker)

        # Checking if score is greater than previous high score :-
        if score > int(high_score):
            # If yes then equalise score and high score variables :-
            high_score = score
        # Passing the score and high score to display_text for displaying on the screen :-

        display_text(str(score), (255, 0, 0), 793, 51)
        display_text(str(high_score), (255, 0, 0), 459, 53)

        # Passes the life_coordinates to show_life function for displaying on the screen:-
        show_life(life_coordinates)

        # Updating the display :-

        pygame.display.update()

        # Ticking the clock 60 times a second.
        clock.tick(60)


# Calling the welcome screen :-

welcome_screen()
