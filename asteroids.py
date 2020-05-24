import pygame
import pygame.sprite
from random import randint


class Asteroid(pygame.sprite.Sprite):
    """Defines an asteroid that falls from the top of the screen."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.asteroid_color
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.x = randint(0, self.screen_width)
        self.y = randint(0, self.screen_height/2)

        # initialize asteroid at random locations on top quarter of screen
        self.rect = pygame.Rect(
            self.x, self.y, self.settings.asteroid_width, self.settings.asteroid_height)

    def update(self):
        """moves asteroid to the bottom of the screen with speed"""
        self.y += self.settings.asteroid_speed
        self.rect.y = self.y

    def draw_asteroid(self):
        """Draw the asteroid on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
