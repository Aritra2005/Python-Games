import sys
import pygame
from settings import Settings
from ball import Ball
from bouncer import Bouncer
from random import randint
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from timer import Timer
import time


class BouncingBall:

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.caption)

        self.ball = Ball(self.screen_rect.centerx, self.screen_rect.centery, self.screen, self.settings.ball_vx,
                         self.settings.ball_vy, self.settings.radius, self.settings.ball_color)

        self.bouncer_left = Bouncer(self.screen_rect.left, self.screen_rect.centery, self.screen, self.settings)

        self.bouncer_right = Bouncer(self.screen_rect.right - self.settings.bouncer_width, self.screen_rect.centery,
                                     self.screen, self.settings)

        self.bouncers = [self.bouncer_left, self.bouncer_right]
        self.button = Button(self.screen, 'PLAY', self.settings)
        self.clock = pygame.time.Clock()
        self.game_stats = GameStats()
        self.font = pygame.font.SysFont(None, 60)
        self.score_board = Scoreboard(self.screen, self.game_stats, self.settings)
        self.timer = Timer(self.screen, self.settings)

    def update_screen(self):
        """
        Updates the images, timer and the screen
        :return: None
        """

        # Drawing the vertical line :-
        pygame.draw.line(self.screen, pygame.Color('black'), (self.screen_rect.centerx, 79),
                         (self.screen_rect.centerx, self.screen_rect.bottom), 2)

        # Draw the horizontal line:-
        pygame.draw.line(self.screen, pygame.Color('black'), (self.screen_rect.left, 79), (self.screen_rect.right, 79),
                         2)
        # Drawing the ball, bouncers to the screen :-
        self.ball.draw_ball()
        for bouncer in self.bouncers:
            bouncer.draw_bouncer()
        # Allowing Movement of the ball and bouncers if the game is active :-
        if self.game_stats.game_active:
            self.ball.move()
            for bouncer in self.bouncers:
                bouncer.update()

        # Drawing the button to the screen if game is inactive:-
        if not self.game_stats.game_active:
            self.button.draw_button()

        # Drawing the scores and players to the screen:-
        self.score_board.show_scores_players()

        # Show the timer:-
        self.timer.show_time()

        # Updating the screen :-
        pygame.display.flip()

    @staticmethod
    def change_ball_state(surface):
        """
        :param surface: String
        :return: Integer
        Returns the new velocity and direction of the ball after it collides.
        """
        # Checks if the ball has collided with the top or bottom walls.
        if surface == 'vertical':
            velocity_in_y = randint(10, 18)
            return velocity_in_y
        # Checks if the ball has collided with the right or left wall or the bouncers.
        elif surface == 'horizontal':
            velocity_in_x = randint(13, 18)
            velocity_in_y = randint(-18, 18)
            return velocity_in_x, velocity_in_y

    def check_ball_wall_collisions(self):
        """ Checks if the ball collides with the screen and changes its direction and velocity:- """
        # Checks if the ball collides with the top screen :-
        if self.ball.rect.top <= self.screen_rect.top + 79:
            velocity_in_y = self.change_ball_state('vertical')
            self.ball.vy = velocity_in_y

        # Checks if the ball collides with the bottom screen :-
        elif self.ball.rect.bottom >= self.screen_rect.bottom:
            velocity_in_y = self.change_ball_state('vertical')
            self.ball.vy = -velocity_in_y

        # Checks if the ball collides with the left wall and reducing the score:-
        elif self.ball.rect.left <= self.screen_rect.left:
            velocity_in_x, velocity_in_y = self.change_ball_state('horizontal')
            self.ball.vx = velocity_in_x
            self.ball.vy = velocity_in_y
            if self.game_stats.left_score > 0:
                self.game_stats.left_score -= self.settings.points_deduction
                self.score_board.left_score = self.game_stats.left_score
                self.score_board.prep_scores()

        # Checks if the ball collides with the right wall and reducing the score:-
        elif self.ball.rect.right >= self.screen_rect.right:
            velocity_in_x, velocity_in_y = self.change_ball_state('horizontal')
            self.ball.vx = -velocity_in_x
            self.ball.vy = velocity_in_y
            if self.game_stats.right_score > 0:
                self.game_stats.right_score -= self.settings.points_deduction
                self.score_board.right_score = self.game_stats.right_score
                self.score_board.prep_scores()

    def check_ball_bouncer_collisions(self):
        """ Checks if the ball collides with bouncers and changes its direction and velocity"""
        # Checks if the ball collides with the left bouncer :-
        if self.ball.rect.colliderect(self.bouncers[0]):
            velocity_in_x, velocity_in_y = self.change_ball_state('horizontal')
            self.ball.vx = velocity_in_x
            self.ball.vy = velocity_in_y
            # Adding the score to the left player:-
            self.game_stats.left_score += self.settings.points_add
            self.score_board.left_score = self.game_stats.left_score
            self.score_board.prep_scores()

        # Checks if the ball collides with the right bouncer :-
        elif self.ball.rect.colliderect(self.bouncers[1]):
            velocity_in_x, velocity_in_y = self.change_ball_state('horizontal')
            self.ball.vx = -velocity_in_x
            self.ball.vy = velocity_in_y
            # Adding the score to the right player:-
            self.game_stats.right_score += self.settings.points_add
            self.score_board.right_score = self.game_stats.right_score
            self.score_board.prep_scores()

    def check_ball_collisions(self):
        """ Checks if the ball collides and changes its direction and velocity. """
        self.check_ball_bouncer_collisions()
        self.check_ball_wall_collisions()

    def check_key_down_events(self, event):
        """ Responds to key down events """
        if event.key == pygame.K_DOWN:
            self.bouncer_right.moving_down = True
        elif event.key == pygame.K_UP:
            self.bouncer_right.moving_up = True
        elif event.key == pygame.K_w:
            self.bouncer_left.moving_up = True
        elif event.key == pygame.K_s:
            self.bouncer_left.moving_down = True

    def check_key_up_events(self, event):
        """ Responds to key up events """
        if event.key == pygame.K_DOWN:
            self.bouncer_right.moving_down = False
        elif event.key == pygame.K_UP:
            self.bouncer_right.moving_up = False
        elif event.key == pygame.K_w:
            self.bouncer_left.moving_up = False
        elif event.key == pygame.K_s:
            self.bouncer_left.moving_down = False

    def reset_game(self):
        """
        Resets the game.
        :return: None
        """
        self.game_stats.left_score, self.game_stats.right_score = 0, 0
        self.timer.countdown = self.settings.time_in_seconds
        self.score_board = Scoreboard(self.screen, self.game_stats, self.settings)
        self.ball.rect.center = self.screen_rect.centerx, self.screen_rect.centery

    def check_mouse_clicks(self, pos):
        """ Checks the mouse clicks. """
        mouse_x, mouse_y = pos
        if self.button.rect.collidepoint(mouse_x, mouse_y):
            self.reset_game()
            self.game_stats.game_active = True

    def check_events(self):
        """ Responds to key presses and mouse clicks """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.check_key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_mouse_clicks(mouse_pos)

    def show_winner(self, text):
        """
        Shows text on the screen.
        :param text: String
        :return: None
        """
        text_image = self.font.render(text, True, pygame.Color('purple'), self.settings.screen_color)
        rect = text_image.get_rect()
        rect.centerx, rect.top = self.screen_rect.centerx, 90
        self.screen.blit(text_image, rect)

    def check_timer(self):
        """
        Checks if timer has reached 0
        :return: None
        """

        if self.timer.countdown == 0:
            if self.game_stats.left_score > self.game_stats.right_score:
                self.show_winner('Player1 has won the game')
            elif self.game_stats.right_score > self.game_stats.left_score:
                self.show_winner('Player2 has won the game')
            else:
                self.show_winner("Draw")
            self.game_stats.game_active = False

    def run(self):
        """ Runs the game and manages other functionalities . """
        # Initialize pygame modules :-
        start_time = time.time()
        pygame.init()
        self.timer = Timer(self.screen, self.settings)

        while True:
            # Checking for the events :-
            self.check_events()
            # Updating the timer :-
            time2 = time.time()
            if time2 - start_time >= 1 and self.game_stats.game_active:
                self.timer.update()
                start_time = time2
            # Filling the screen with green color:-
            self.screen.fill(pygame.Color(self.settings.screen_color))
            # Checking the ball collisions :-
            if self.game_stats.game_active:
                self.check_ball_collisions()
            # Checking the timer:-
            self.check_timer()
            # Updating the screen :-
            self.update_screen()
            # Controlling the number of times the loop runs :-
            self.clock.tick(self.settings.fps)
