import pygame
import pygame.sprite
from random import randint


class Star(pygame.sprite.Sprite):
    """ Places stars on the screen randomly """

    def __init__(self, ai_game):
        """initializes the stars"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.star_color
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.x = randint(0, self.screen_width)
        self.y = randint(0, self.screen_height)

        # initialize star at random location.
        self.rect = pygame.Rect(
            self.x, self.y, self.settings.star_width, self.settings.star_height)

    def draw_star(self):
        """Draw star on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
