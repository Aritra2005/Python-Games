import pygame
import sys
import random
import time

pygame.init()

game_window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Crazy Rocket")
screen_height = game_window.get_height()
screen_width = game_window.get_width()
number_of_stones = 15
fps = 60
rock_x = [random.randrange(20, screen_width - 50) for i in range(number_of_stones)]
rock_y = [random.randrange(20, screen_height - 200) for j in range(number_of_stones)]
rock_coordinates = []
for j in range(number_of_stones):
    k = [rock_x[j], rock_y[j]]
    rock_coordinates.append(k)
font = pygame.font.SysFont("Arial", 60)
clock = pygame.time.Clock()

space = pygame.image.load("Gallery/Sprites/space.jpg")
space = pygame.transform.scale(space, [screen_width, screen_height]).convert_alpha()
rock = pygame.image.load("Gallery/Sprites/rock.png")
rock = pygame.transform.scale(rock, (80, 80))
spaceship = pygame.image.load("Gallery/Sprites/spaceship.png")
spaceship = pygame.transform.scale(spaceship, (100, 150)).convert_alpha()
game_over_screen = pygame.image.load("Gallery/Sprites/game over.jpg")
game_over_screen = pygame.transform.scale(game_over_screen, (screen_width, screen_height)).convert_alpha()
life = pygame.image.load("Gallery/Sprites/life.png")
welcome_screen = pygame.image.load("Gallery/Sprites/WelcomePage.jpg")
welcome_screen = pygame.transform.scale(welcome_screen, [screen_width, screen_height]).convert_alpha()
play_button = pygame.image.load("Gallery/Sprites/play button.png")
play_button = pygame.transform.scale(play_button, (200, 180)).convert_alpha()

GAME_SPRITES = {
    'space': space,
    'rock': rock,
    'spaceship': spaceship,
    'game_over': game_over_screen,
    'life': life,
    'welcome_screen': welcome_screen,
    'play_button': play_button
}

GAME_AUDIO = {
    'hit': pygame.mixer.Sound("Gallery/Audio/hit.wav"),
    'point': pygame.mixer.Sound("Gallery/Audio/point.wav")
}


def show_text(text, x, y, color):
    to_display = font.render(text, True, color)
    game_window.blit(to_display, [x, y])


def display_stones(coordinates):
    for x, y in coordinates:
        game_window.blit(GAME_SPRITES['rock'], (x, y))


def display_life(coordinates):
    for x, y in coordinates:
        game_window.blit(GAME_SPRITES['life'], (x, y))


def check_positions(coordinates):
    for x, y in coordinates:
        if (x >= screen_width or x <= 0) or (
                y >= screen_height - GAME_SPRITES['spaceship'].get_height() - 80 or y <= 0):
            del coordinates[coordinates.index([x, y])]
            coordinates.append([random.randint(50, screen_width - 100), random.randint(100, screen_height - 100)])


def detect_collision(rocks, player_x, player_y):
    collided = False
    for x, y in rocks:
        if abs(player_x - x) < 55 and abs(player_y - y) < 55:
            collided = True
    return collided


def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
        game_window.blit(GAME_SPRITES['game_over'], (0, 0))
        show_text("PRESS SPACE BAR TO RESTART THE GAME", 50, 50, "red")
        pygame.display.update()
        clock.tick(60)


def welcome():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (screen_width / 2 - 90 <= x <= screen_width / 2 - 130 + GAME_SPRITES['play_button'].get_width()
                        and screen_height / 2 + 50 <= y <= screen_height / 2 +
                        GAME_SPRITES['play_button'].get_height() - 50):
                    main_game()
        game_window.blit(GAME_SPRITES['welcome_screen'], (0, 0))
        game_window.blit(GAME_SPRITES['play_button'], (screen_width / 2 - 110, screen_height / 2))
        pygame.display.update()
        clock.tick(60)


def main_game():
    global screen_height
    global screen_width
    x = time.time()
    y = time.time()
    will_velocity_change = True
    timer = True
    vel_x = [random.randrange(-5, 5) for _ in range(number_of_stones)]
    vel_y = [random.randrange(-3, 6) for _ in range(number_of_stones)]
    delay = 4
    player_y = screen_height - 150
    player_x = random.randint(0, screen_width - 50)
    vel_player_x = 0
    vel_player_y = 0
    life_coordinates = [[60, 60], [100, 60], [140, 60]]
    life_deduction_delay = 0.5
    life_deducted = True
    score = 0
    while True:
        if will_velocity_change:
            vel_x = [random.randrange(-5, 5) for _ in range(number_of_stones)]
            vel_y = [random.randrange(-3, 6) for _ in range(number_of_stones)]
            will_velocity_change = False
            x = time.time()
        num = random.randint(1, 3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_height = game_window.get_height()
                screen_width = game_window.get_width()
                GAME_SPRITES['space'] = pygame.transform.scale(space, [screen_width, screen_height]).convert_alpha()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    vel_player_y -= 5
                    vel_player_x = 0
                elif event.key == pygame.K_DOWN:
                    vel_player_y += 5
                    vel_player_x = 0
                elif event.key == pygame.K_RIGHT:
                    vel_player_x += 5
                    vel_player_y = 0
                elif event.key == pygame.K_LEFT:
                    vel_player_x -= 5
                    vel_player_y = 0
            elif event.type == pygame.KEYUP:
                vel_player_x = 0
                vel_player_y = 0
        player_y += vel_player_y
        player_x += vel_player_x
        for i in range(number_of_stones):
            if num == 1:
                rock_coordinates[i][0] += vel_x[i]
            elif num == 2:
                rock_coordinates[i][1] += vel_y[i]
        game_window.blit(GAME_SPRITES['space'], (0, 0))
        game_window.blit(GAME_SPRITES['spaceship'], (player_x, player_y))
        display_stones(rock_coordinates)
        display_life(life_coordinates)
        if timer:
            if time.time() - x >= delay:
                will_velocity_change = True
        check_positions(rock_coordinates)
        if detect_collision(rock_coordinates, player_x, player_y):
            if life_deducted:
                GAME_AUDIO['hit'].play()
                del life_coordinates[len(life_coordinates) - 1]
                player_y = screen_height - 150
                player_x = random.randint(0, screen_width - 50)
                life_deducted = False
                y = time.time()
        if player_x <= 0 or player_x >= screen_width:
            if life_deducted:
                del life_coordinates[len(life_coordinates) - 1]
                player_y = screen_height - 150
                player_x = random.randint(0, screen_width - 50)
                life_deducted = False
                y = time.time()
        if timer:
            if time.time() - y >= life_deduction_delay:
                life_deducted = True
        if len(life_coordinates) == 0:
            game_over()
        if player_y <= 0:
            player_y = screen_height - 150
            player_x = random.randint(0, screen_width - 50)
            GAME_AUDIO['point'].play()
            score += 1
        show_text(f'{score}', 1220, 36, 'red')
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    welcome()
