"""
This Python file houses the code for the Player class
and the tutorial NPC that guides the player on how to play the game.
"""
import pygame
from setup import resource_path
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]

CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)

# The factor to increase the size of each player HUD sprite by
SIZE_MULTIPLE = 5

class Player:

    def __init__(self):
        self.lives = 3

        # Load up each sprite and resize them by a factor of SIZE_MULTIPLE
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()
        _, _, self.heart_width, self.heart_height = self.heart_image.get_rect()
        self.heart_width *= SIZE_MULTIPLE
        self.heart_height *= SIZE_MULTIPLE
        self.heart_image = pygame.transform.scale(self.heart_image,
                           (self.heart_width, self.heart_height))

        self.health_bar = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "health_bar.png"))).convert_alpha()
        _, _, self.hbar_width, self.hbar_height = self.health_bar.get_rect()
        self.hbar_width *= SIZE_MULTIPLE
        self.hbar_height *= SIZE_MULTIPLE
        self.health_bar = pygame.transform.scale(self.health_bar, (self.hbar_width,
                                                 self.hbar_height))
        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """
        # Offset so that there is a small amount of space between eachsprite
        # and the edge of the screen
        offset = 10

        # Display the heart icon at the top left corner of screen
        screen.blit(self.heart_image,(offset, offset))

        # The health bar is at the immediate right of the heart icon
        screen.blit(self.health_bar, (self.heart_width + offset * 2, offset))
        return

