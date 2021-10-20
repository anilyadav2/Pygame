class Settings:
    """Storage game "alien invasion" in all settings of the class"""

    def __init__(self):
        """Initialize the static settings of the game"""
        # screen setting
        self.screen_width = 1200  # Screen width, in pixels
        self.screen_height = 700  # Screen height, in pixels
        self.bg_color = (230, 230, 230)  # background color 

        # Spacecraft setup
        self.ship_limit = 3  # Total number of ships available

        # Bullet setting
        self.bullet_with = 4
        self.bullet_height = 20
        self.bullet_color = (100, 160, 60)
        self.bullet_allowed = 3  # Maximum bullets

        # Alien settings
        self.fleet_drop_speed = 3  # The speed of moving down the line

        self.speedup_scale = 1.1  # Speed up the game
        self.score_scale = 1.5  # The speed of alien score increase

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes settings that change as the game progresses"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0
        self.fleet_direction = 1  # 1 means to move to the right, - 1 means to move to the left
        self.alien_points = 50  # An alien scored

    def increase_speed(self):
        """Increase speed setting and alien score"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)