class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # start Alien Invasion in an inactive state
        self.game_active = False
        # high score should never be reset
        self.filename = 'high_scores.txt'
        self.high_score = 0

    def reset_stats(self):
        """initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def write_high_score(self):
        with open(self.filename, 'w') as f:
            f.write(self.high_score)
