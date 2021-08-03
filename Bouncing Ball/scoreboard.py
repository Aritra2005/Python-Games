import pygame.font


class Scoreboard:
    def __init__(self, screen, stats, settings):
        """ Initialises scoreboard attributes. """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.left_score = stats.left_score
        self.right_score = stats.right_score
        self.font = pygame.font.SysFont(None, 48)
        self.settings = settings
        self.prep_scores()
        self.prep_players()

    def prep_scores(self):
        """ Converts the scores into an image . """
        left_score_string = '{:,}'.format(self.left_score)
        right_score_string = '{:,}'.format(self.right_score)
        self.left_score_image = self.font.render(left_score_string, True, self.settings.score_color,
                                                 self.settings.screen_color)
        self.left_score_rect = self.left_score_image.get_rect()
        self.right_score_image = self.font.render(right_score_string, True, self.settings.score_color,
                                                  self.settings.screen_color)
        self.right_score_rect = self.right_score_image.get_rect()
        self.left_score_rect.left = self.screen_rect.left
        self.right_score_rect.right = self.screen_rect.right
        self.left_score_rect.top = self.right_score_rect.top = self.screen_rect.top + 40

    def prep_players(self):
        """
        Turns the player strings into images.
        :return: None
        """
        self.player1 = self.font.render('Player1', True, self.settings.score_color, self.settings.screen_color)
        self.player2 = self.font.render('Player2', True, self.settings.score_color, self.settings.screen_color)
        self.rect1 = self.player1.get_rect()
        self.rect2 = self.player2.get_rect()
        self.rect1.left, self.rect1.top = self.screen_rect.left, self.screen_rect.top + 5
        self.rect2.right, self.rect1.top = self.screen_rect.right, self.screen_rect.top + 5

    def show_scores_players(self):
        """ Shows the scores, players on the screen. """
        self.screen.blit(self.left_score_image, self.left_score_rect)
        self.screen.blit(self.right_score_image, self.right_score_rect)
        self.screen.blit(self.player1, self.rect1)
        self.screen.blit(self.player2, self.rect2)
