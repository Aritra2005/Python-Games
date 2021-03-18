import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image :-

bgimg = pygame.image.load("snake.jpeg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes")
pygame.display.update()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)

with open("highscore.txt", "r") as f:
    high_score = f.read()


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# Welcome screen :-

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 210, 229))
        text_screen("Welcome to Snakes", black, 270, 260)
        text_screen("Press Spacebar To Play !", black, 250, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.ogg')
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(60)


# Game Loop

def game_loop():
    global high_score
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_length = 1
    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60
    snake_list = []

    # Check if hiscore file exists:-

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as h:
            h.write("0")
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as g:
                g.write(str(high_score))
            gameWindow.fill(white)
            text_screen("Game Over ! Press Enter to continue", red, 100, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Adding cheat codes :-
                    if event.key == pygame.K_q:
                        score += 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, int(screen_width / 2))
                food_y = random.randint(20, int(screen_height / 2))
                snake_length += 5
                if score > int(high_score):
                    high_score = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            head = [snake_x, snake_y]
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                pygame.mixer.music.load('gameover.ogg')
                pygame.mixer.music.play()
                game_over = True
            text_screen(f"Score :- {score}   High Score :- {high_score}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
