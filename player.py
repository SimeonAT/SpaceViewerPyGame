"""
This Python file houses the code for the Player class
and the tutorial NPC that guides the player on how to play the game.
"""
import pygame
from setup import resource_path
from random import randint
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

        self.HUD_frames_since_shown = 0
        self.hover_direction = 1

        # Load up the heart sprite and resize it by a factor of SIZE_MULTIPLE
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()
        _, _, self.heart_width, self.heart_height = self.heart_image.get_rect()
        self.heart_width *= SIZE_MULTIPLE
        self.heart_height *= SIZE_MULTIPLE
        self.heart_image = pygame.transform.scale(self.heart_image,
                           (self.heart_width, self.heart_height))
        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """
        # Offset so that there is a small amount of space between each sprite
        # and the edge of the screen
        offset = 10

        # Display the heart icons at the top left corner of screen
        for i in range(1, 4):
            # The distance that top left coord of current heart needs to be in order
            # to be right next to the previous heart icon
            # 
            dist_from_prev_heart = self.heart_width * (i - 1)

            # For the ith heart, we need to offset * i in order for the hearts to be
            # offset distance apart; not * i will make the hearts cluttered together
            # 
            x_offset = offset * i

            # Every 16 frames, slightly adjust y pos of the heart icons by a small
            # random number in order to give them a hover effect similar to the asteroids
            # 
            if self.HUD_frames_since_shown % 32 == 0:
                self.hover_direction *= -1
                self.heart_height = self.heart_height + self.hover_direction * 30

            screen.blit(self.heart_image, (dist_from_prev_heart + x_offset,
                                          self.heart_height))

        return

    def increment_frames(self):
        """
        Increment the number of frames that the player HUD has been displayed on screen.
        """
        self.HUD_frames_since_shown += 1
        return

