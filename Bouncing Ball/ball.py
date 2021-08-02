import pygame.font

pygame.init()


class Ball:
    def __init__(self, x, y, screen, vx, vy, radius, color):
        self.screen = screen
        self.vx, self.vy = vx, vy
        self.radius = radius
        self.rect = pygame.Rect(0, 0, 2 * self.radius, 2 * self.radius)
        self.rect.center = x, y
        self.color = color

    def draw_ball(self):
        """ Draws the ball to the screen. """
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)

    def move(self):
        """ Moves the ball. """
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
