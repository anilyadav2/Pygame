import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class that manages the bullets fired by a spaceship"""

    def __init__(self, ai_game):
        """Create a bullet object in the current position of the ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a rectangle at (0,0) to represent the bullet, and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_with, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet position in decimal
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up"""
        # Update the decimal value that represents the bullet position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullets on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)