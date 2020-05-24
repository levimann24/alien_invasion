import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """initialize the ship and sets its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # load the ship image and get its rect.
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()
        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # store a decimal value for the ships horizontal position.
        self.x = float(self.rect.x)
        # rocket package
        self.y = float(self.rect.y)
        # movement flag
        self.moving_right = False
        self.moving_left = False
        # rocket package
        self.moving_down = False
        self.moving_up = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # rocket package
        if self.settings.rocket:
            if self.moving_up and self.rect.top > 0:
                self.y -= self.settings.ship_speed
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ship_speed
        # update rect object from self.x
        self.rect.x = self.x

        # rocket package
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at it's current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on the bottom of screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
