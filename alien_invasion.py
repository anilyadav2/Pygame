import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """Class that initializes game resources and behaviors"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()  # Initialize background settings to make Pygame work properly
        self.settings = Settings()  # Create an instance of Settings and use it to access Settings
        # Create a display window. The parameter is tuple, the unit is pixel, and the return object is surface (part of the screen, used to display game elements, here represents the whole game window)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)  # Create an instance to store game statistics
        self.scoreboard = ScoreBoard(self)  # Create scoreboard
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Create groups to store bullets
        self.aliens = pygame.sprite.Group()  # Creating groups for storing aliens
        self.play_button = Button(self, "Play")  # Create Play button
        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop of the game"""
        while True:  # The transaction management is separated from other aspects of the game (such as updating the screen) through auxiliary methods -- refactoring, which makes the loop simple
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            # Redraw the screen every time you cycle
            self._update_screen()

    def _check_events(self):
        """Response to button and mouse events"""
        for event in pygame.event.get():  # Get a list of monitoring keyboard and mouse events (all events occurred after the last call)
            if event.type == pygame.QUIT:  # When the player clicks the close button in the game window, it will detect pygame.QUIT event
                sys.exit()  # Quit the game
            elif event.type == pygame.KEYDOWN:  # Each time the player presses a key, it is registered as a key down event
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Players click the Play button
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Response button"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _create_fleet(self):
        """Creating alien groups"""
        # Create the first alien and calculate how many aliens a row can hold
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - alien_width
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        num_aliens_x = available_space_x // (2 * alien_width)
        num_aliens_rows = available_space_y // (2 * alien_height)

        # Creating alien groups
        for row_number in range(num_aliens_rows):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        """Create an alien colony"""
        alien = Alien(self)
        alien.x = alien_width + alien_number * alien_width * 2
        alien.y = alien_height + 10 + row_number * alien_height * 2
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _fire_bullet(self):
        """Create a bullet and add it to the group bullets in"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)  # Don't forget to import ai_game
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the location of the bullet and delete the missing bullet"""
        self.bullets.update()  # When you call update() on a group, the group automatically calls update() on each sprite in the group

        # Delete missing bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_bullet_alien_collisions()  # Shooting aliens

    def _check_bullet_alien_collisions(self):
        """Check for bullets and collisions for pedestrians"""
        # Check whether there are bullets hitting the aliens, if there are, delete the corresponding bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:  # Scoring
            for aliens in collisions.values():  # Every alien guaranteed to be eliminated is counted in the score
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # If the alien crowd is eliminated, delete the existing bullets and create a new group of aliens, and speed up the pace of the game to enhance the player level
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """Check if there are aliens at the edge of the screen, and update the location of all aliens in the alien crowd"""
        self._check_fleet_edge()
        self.aliens.update()

        # Detecting collisions between aliens and spaceships
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens at the bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edge(self):
        """Take corresponding measures when aliens arrive at the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move the whole group down and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """The spaceship was hit by aliens"""

        if self.stats.ships_left > 0:
            # Will ship_left - 1
            self.stats.ships_left -= 1
            # Update scoreboard
            self.scoreboard.prep_ships()

            # Empty the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new group of aliens and place the spacecraft in the center at the bottom of the screen
            self._create_fleet()
            self.ship.center_ship()

            # Pause for half a second
            sleep(0.5)
        else:
            self.stats.game_active = False  # game over
            pygame.mouse.set_visible(True)  # Show hidden cursor

    def _check_aliens_bottom(self):
        """Check to see if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()  # Deal with it like a ship is hit
                break

    def _check_play_button(self, mouse_pos):
        """Click on the Play Button to start a new game"""
        button_checked = self.play_button.rect.collidepoint(mouse_pos)
        if button_checked and not self.stats.game_active:  # Prevent the game from restarting when the user clicks the area where the button is in the process of the game
            # Hide mouse cursor
            pygame.mouse.set_visible(False)

            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()  # Scores need to change
            self.scoreboard.prep_level()  # The level needs to change
            self.scoreboard.prep_ships()  # The number of remaining ships will change

            # Empty the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new group of aliens and place the spacecraft in the center at the bottom of the screen
            self._create_fleet()
            self.ship.center_ship()

    def _check_keyup_events(self, event):
        """Response release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update the image on the screen and switch to the new screen"""
        self.screen.fill(self.settings.bg_color)  # Color, fill() method is used to deal with the surface, only accept one argument - one color
        self.ship.blitme()  # Drawing spaceships
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # If the game is inactive, draw the Play button
        if not self.stats.game_active:
            self.play_button.draw_button()

        self.scoreboard.show_score_level_ships()  # Show score, rank and number of spaceships
        pygame.display.flip()  # Make the recently drawn screen visible


