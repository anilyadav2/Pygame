import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """Initialize button properties"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the size and other properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # None lets Pygame use the default font and 48 specifies the font size

        # Create the rect object of the button and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The label for the button only needs to be created once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """take msg Render to an image and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw a button filled with color, and then draw the text"""
        self.screen.fill(self.button_color, self.rect)   
        # Or pygame.draw.rect(self.screen, self.button_color, self.rect)
        
        self.screen.blit(self.msg_image, self.msg_image_rect)