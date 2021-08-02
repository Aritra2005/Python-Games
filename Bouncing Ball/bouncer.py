import pygame


class Bouncer:

    def __init__(self, x, y, screen, settings):
        """ Initialize the bouncer attributes. """
        self.settings = settings
        self.speed = self.settings.speed_factor
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, self.settings.bouncer_width, self.settings.bouncer_height)
        self.rect.x = x
        self.rect.centery = y
        self.color = self.settings.bouncer_color
        self.moving_up = False
        self.moving_down = False

    def draw_bouncer(self):
        """ Draws the bouncer to the screen. """
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """ Updates the position of the bouncer. """
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.centery += self.speed
        elif self.moving_up and self.rect.top >= 81:
            self.rect.centery -= self.speed
