class Settings:
    """A class to stor all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's Settings."""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)  # bacground color

        # adding extra settings so rocket can move up right left and down
        self.rocket = True

        # ship settings
        self.ship_speed = 6
