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

    def show_players(self):
        """
        Shows the players.
        :return: None
        """
        player1 = self.font.render('Player1', True, self.settings.score_color, self.settings.screen_color)
        player2 = self.font.render('Player2', True, self.settings.score_color, self.settings.screen_color)
        rect1 = player1.get_rect()
        rect2 = player2.get_rect()
        rect1.left, rect1.top = self.screen_rect.left, self.screen_rect.top + 5
        rect2.right, rect1.top = self.screen_rect.right, self.screen_rect.top + 5
        self.screen.blit(player1, rect1)
        self.screen.blit(player2, rect2)

    def show_scores(self):
        """ Shows the scores on the screen. """
        self.prep_scores()
        self.screen.blit(self.left_score_image, self.left_score_rect)
        self.screen.blit(self.right_score_image, self.right_score_rect)
