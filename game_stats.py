class GameStats:
    """Track game statistics"""

    def __init__(self, ai_game):
        """Initialization statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False  # When the game starts, it is inactive
        self.high_score = 0  # Under no circumstances should the maximum score be reset

    def reset_stats(self):
        """Initializes statistics that may change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        