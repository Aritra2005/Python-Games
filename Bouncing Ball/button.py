import pygame.font


class Button:

    def __init__(self, screen, msg, settings):
        """ Initialize the button attributes. """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimension nd properties of the button :-
        self.width, self.height = settings.button_width, settings.button_height
        self.button_color = settings.button_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it :-
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message need to be prepped only once :-
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn message into rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and draw the message :-
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
