import pygame.font


class Timer:
    def __init__(self, screen, settings):
        """ Initialising timer attributes. """
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.countdown = self.settings.time_in_seconds
        self.text_color = self.settings.time_text_color
        self.screen_color = self.settings.screen_color
        self.font = pygame.font.SysFont(None, 48)

    def prep_time(self):
        """
        Converts the countdown time to image
        :return: None
        """
        countdown_string = str(self.countdown) + ' secs'
        self.time_image = self.font.render(countdown_string, True, self.text_color, self.screen_color)
        self.rect = self.time_image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 20

    def show_time(self):
        """
        Shows the time on the screen.
        :return: None
        """
        self.prep_time()
        self.screen.blit(self.time_image, self.rect)

    def update(self):
        """
        Updates the timer.
        :return: None
        """
        self.countdown -= 1
