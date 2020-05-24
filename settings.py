class Settings:
    """A class to stor all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's Settings."""
        # screen settings
        self.full_screen = True
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)  # bacground color

        # ship settings
        #self.ship_speed = 6
        self.rocket = True  # allows ship to move up and down
        self.ship_limit = 3

        # bullet Settings
        #self.bullet_speed = 8
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230)
        self.bullets_allowed = 3  # limiting the number of bullets

        # Star settings
        self.star_height = 1
        self.star_width = 1
        self.star_color = (230, 230, 230)
        self.stars_allowed = 1000

        # alien settings
        #self.alien_speed = 1
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represents right: -1 represents left
        #self.fleet_direction = 1

        # asteroid settings
        self.asteroid_width = 3
        self.asteroid_height = 3
        self.asteroid_color = (230, 230, 230)
        self.asteroids_allowed = 10
        self.asteroid_speed = 1

        # how quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # initialize all of the dynamic settings
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes settings taht change througout the game"""
        self.ship_speed = 3
        self.bullet_speed = 4
        self.alien_speed = 3
        # Fleet direction of 1 represents right: -1 represents left
        self.fleet_direction = 1
        # scoring
        self.alien_points = 50

    def increase_speed(self):
        """increases speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= int(self.score_scale)
