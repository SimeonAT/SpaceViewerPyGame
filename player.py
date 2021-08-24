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

class Player:

    def __init__(self):
        self.lives = 3

        # Load up the heart sprite image and resize it so that it appears big enough on screen
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()

        _, _, self.width, self.height = self.heart_image.get_rect()
        self.width *= 5
        self.height *= 5

        self.heart_image = pygame.transform.scale(self.heart_image,
                           (self.width, self.height))
        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """
        # The heart sprite, along with the number of lives the player has,
        # will always be shown at the top left corner of the screen
        screen.blit(self.heart_image,(0, 0))
        return

