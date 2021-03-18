import pygame

x = pygame.init()

# Creating Window :- 

gameWindow = pygame.display.set_mode((1200, 500))
pygame.display.set_caption("My First Game")

# Game specific variables in pygame :-

exit_game = False # If exit_game = True the it will close the window
game_over = False # If game_over = True then the game will be over.

#Creating a game loop :-

while not exit_game:
    pass

pygame.quit()
quit()
