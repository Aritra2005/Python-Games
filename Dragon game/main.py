import pygame
import sys
import time

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
font = pygame.font.SysFont("Arial", 60)
clock = pygame.time.Clock()

game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dragon Game by Aritra")

welcome_image = pygame.image.load('gallery/sprites/welcome_dragon.jpg')
welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
back_image = pygame.image.load('gallery/sprites/background.jpg')
back_image = pygame.transform.scale(back_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
game_over = pygame.image.load('gallery/sprites/game_over.png')
game_over = pygame.transform.scale(game_over, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
GAME_SPRITES = {'dino': pygame.image.load('gallery/sprites/dino.png').convert_alpha(),
                'dragon': pygame.image.load('gallery/sprites/dragon.png').convert_alpha(),
                'background': back_image,
                'welcome': welcome_image,
                'game-over': game_over,
                }

GAME_SOUNDS = {
    'die': pygame.mixer.Sound('gallery/Audio/die.wav'),
    'hit': pygame.mixer.Sound('gallery/Audio/hit.wav'),
    'point': pygame.mixer.Sound('gallery/Audio/point.wav'),
    'wing': pygame.mixer.Sound('gallery/Audio/wing.wav')
}


def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


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


def dragons(dragon_list):
    for x, y in dragon_list:
        game_window.blit(GAME_SPRITES['dragon'], (x, y))


def game_over():
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


def main_game():
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

    while True:
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
        attacker = [[attacker_x, attacker_y]]
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
        player_x += vel_x
        player_y += vel_y
        game_window.blit(GAME_SPRITES['background'], (0, 0))
        game_window.blit(GAME_SPRITES['dino'], (player_x, player_y))
        attacker_x += vel_attacker_x
        if attacker_x <= limit:
            attacker_x = SCREEN_WIDTH + 100
        if player_jumped:
            if jump_count >= -10:
                player_y -= (jump_count * abs(jump_count)) * 0.5
                player_x += 10
                jump_count -= 1
            else:
                jump_count = 10
                player_jumped = False
        if cross:
            for j, k in attacker:
                if abs(player_x - j) < 145:
                    score += 1
                    x = time.time()
                    timer = True
                    cross = False
                    GAME_SOUNDS['point'].play()
        if timer:
            if time.time() - x >= delay:
                cross = True
        if is_collide(player_x, player_y, attacker):
            GAME_SOUNDS['hit'].play()
            game_over()
            GAME_SOUNDS['die'].play()
        dragons(attacker)
        display_text(str(score), (255, 0, 0), 793, 48)
        pygame.display.update()
        clock.tick(60)


welcome_screen()
