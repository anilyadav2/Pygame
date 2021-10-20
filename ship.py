import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Classes for managing spaceships"""

    def __init__(self, ai_game):  # Parameters: reference self and a reference to the current AlienInvasion instance, which enables Ship to access all game resources defined in AlienInvasion
        """Initialize the ship and set its initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()  # get_rect() to access the properties of the screen rect

        # Load the spaceship image and get its external rectangle
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()

        # For each new ship, place it in the center at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # The x attribute stores small values, because the x and other attributes of rect can only store integer values

        # Mobile logo
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship in the specified position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        """Put the ship in the bottom center of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)