import pygame


class Settings:

    def __init__(self):
        """ Initialize the settings for the game. """
        # Display settings :-
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_color = pygame.Color('green')
        self.caption = 'Bouncing Ball'
        self.fps = 30

        # Ball Settings :-

        self.ball_vx = 5
        self.ball_vy = -3
        self.radius = 36
        self.ball_color = pygame.Color('red')

        # Bouncer Settings :-
        self.bouncer_width = 50
        self.bouncer_height = 200
        self.speed_factor = 5
        self.bouncer_color = pygame.Color('red')

        # Button settings :-

        self.button_width = 200
        self.button_height = 50
        self.button_color = pygame.Color('purple')

        # Scoreboard:-
        self.score_color = pygame.Color('black')

        # Score :-
        self.points_add = 50
        self.points_deduction = self.points_add

        # Timer:-
        self.time_in_seconds = 120
        self.time_text_color = pygame.Color('black')
