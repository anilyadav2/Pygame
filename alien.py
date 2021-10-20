import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class representing a single alien"""

    def __init__(self, ai_game):
        """Initialize the alien and set its initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect property
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # Each alien is initially near the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the exact location of the aliens
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edge(self):
        """Check whether the alien is at the edge of the screen, and return if yes True"""
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            return True

    def update(self):
        """Move left or right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x