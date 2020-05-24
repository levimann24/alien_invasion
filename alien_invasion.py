import sys
import pygame
import settings
import ship
import bullet


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """initialize the game and create game resources."""
        pygame.init()  # initializes the background settings the pygame needs
        self.settings = settings.Settings()
        # create a display window where we will draw all the game's graphical elements
        # object assined to self.screen is called a surface
        # ___________ For full screen ____________________ uncomment to use
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        # __________________________________________________________

        # _______________for limited screen window__________________ uncomment to use
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # __________________________________________________________
        pygame.display.set_caption("Alien Invasion")
        # storing bullets in a group
        self.bullets = pygame.sprite.Group()
        # initializing ship
        self.ship = ship.Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # watch for keyboard and mouse events.
            # event is action that user performs
            self._check_events()
            # update the ship drawing
            self.ship.update()
            # update the position of the bullets
            # calls update for each bullet since they are in a group.
            self.bullets.update()
            # redraw the screen during each pass through the loop.
            self._update_screen()

            # get rid of bullets they have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            # print(len(self.bullets)) #checks to make sure the bullets are being deleted

    def _check_events(self):
        """ respond to keypresses and mouse events"""
        for event in pygame.event.get():  # accesses the events pygame detects
            if event.type == pygame.QUIT:
                sys.exit()  # Exits the game
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # move ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # exit game if q is pressed
            sys.exit()
        elif event.key == pygame.K_SPACE:  # checks if space is pressed and fire bullet if true
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = bullet.Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        # redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # loop through bullet group and update them for new location
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # make the most recently drawn screen visible.
        pygame.display.flip()  # draws empty screen each pass through the loop


if __name__ == '__main__':
    # make an instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
