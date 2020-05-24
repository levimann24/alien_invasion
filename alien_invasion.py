import sys
from time import sleep  # allows you to pause the game

import pygame

import settings
from game_stats import GameStats
from ship import Ship
import bullet
from alien import Alien
from star import Star
from asteroids import Asteroid
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """initialize the game and create game resources."""
        pygame.init()  # initializes the background settings the pygame needs
        self.settings = settings.Settings()
        # create a display window where we will draw all the game's graphical elements
        # object assined to self.screen is called a surface
        # ___________ For full screen ____________________ uncomment to use
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # __________________________________________________________

        # _______________for limited screen window__________________ uncomment to use
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # __________________________________________________________

        pygame.display.set_caption("Alien Invasion")
        self.screen_rect = self.screen.get_rect()
        # create an instance to store game statistics
        self.stats = GameStats(self)
        # storing stars in a group
        self.stars = pygame.sprite.Group()
        self._create_stars()
        # storing asteroids in a group
        self.asteroids = pygame.sprite.Group()
        # create a scoreboard
        self.sb = Scoreboard(self)
        # storing bullets in a group
        self.bullets = pygame.sprite.Group()
        # storing aliens in a group
        self.aliens = pygame.sprite.Group()
        # initializing ship
        self.ship = Ship(self)
        self._create_fleet()
        # make the Play button.
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # watch for keyboard and mouse events.
            # event is action that user performs
            self._check_events()
            if self.stats.game_active:
                self.ship.update()  # update the ship drawing
                self._update_asteroid()  # update asteroids
                self._create_asteroid()
                self._update_bullets()  # update bullets
                self._update_aliens()  # update aliens
            self._update_screen()  # redraw the screen

    def _check_events(self):
        """ respond to keypresses and mouse events"""
        for event in pygame.event.get():  # accesses the events pygame detects
            if event.type == pygame.QUIT:
                sys.exit()  # Exits the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        # reset the game statistics.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        # get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        # create new fleet and center ship.
        self._create_fleet()
        self.ship.center_ship()
        # hide mouse cursor.
        pygame.mouse.set_visible(False)

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
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

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
        for star in self.stars.sprites():
            star.draw_star()
        self.ship.blitme()
        # loop through asteroids and update them for new location
        for asteroid in self.asteroids.sprites():
            asteroid.draw_asteroid()
        # loop through bullet group and update them for new location
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # draw aliens on screen
        self.aliens.draw(self.screen)
        # draw scoreboard on screen
        self.sb.show_score()
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        # make the most recently drawn screen visible.
        pygame.display.flip()  # draws empty screen each pass through the loop

    def _update_bullets(self):
        """update the position of bullets and get rid of old bullets."""
        # update bullet positions
        # update the position of the bullets
        # calls update for each bullet since they are in a group.
        self.bullets.update()
        # get rid of bullets they have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # checks to make sure the bullets are being deleted
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions."""
        # remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and creat new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # increase level.
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _create_fleet(self):
        """create the fleet of aliens."""
        # make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # determine number of columns
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # determine number of rows
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3*alien_height)-ship_height)
        number_rows = available_space_y // (2*alien_height)

        # create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
                # create an alien and place it in the row.

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """ 
        check if the fleet is at an edge, then
        update position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen_rect
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treet this the same as if the ship got hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_stars(self):
        while len(self.stars) < self.settings.stars_allowed:
            star = Star(self)
            self.stars.add(star)

    def _create_asteroid(self):
        if len(self.asteroids) < self.settings.asteroids_allowed:
            asteroid = Asteroid(self)
            self.asteroids.add(asteroid)

    def _update_asteroid(self):
        self.asteroids.update()
        for asteroid in self.asteroids.copy():
            if asteroid.rect.top >= self.screen_rect.bottom:
                self.asteroids.remove(asteroid)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # decrement the ships left.
            self.stats.ships_left -= 1
            # get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # dcreate a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # pause for half a second
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    # make an instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
