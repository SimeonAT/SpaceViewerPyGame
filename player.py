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

# The furthest distance that sprites can be from the edge of the screen;
# prevents them from being drawn right at the end of the scren
OFFSET = 10

class Heart:
    """
    A class describing the behaviors and attributes for each heart
    icon displayed on the Player HUD.
    """
    def __init__(self):
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()
        _, _,  self.width, self.height = self.heart_image.get_rect()
        self.width *= SIZE_MULTIPLE
        self.height *= SIZE_MULTIPLE
        self.image = pygame.transform.scale(self.heart_image,
                           (self.width, self.height))
        return

    def draw(self, screen, position = (OFFSET, OFFSET)):
        """
        Draws the heart icon onto the screen.

        Parameters:
            The screen to draw on
            The (x, y) position as a tuple or list
        """
        screen.blit(self.image, position)
        return


class Player:

    def __init__(self):
        self.lives = 3
        self.heart_icons = []
        for i in range(0, self.lives):
            self.heart_icons.append(Heart())

        self.HUD_frames_since_shown = 0
        self.hover_direction = 1
        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """

        # Display the heart icons at the top left corner of screen
        for i in range(0, self.lives):
            # The distance that top left coord of current heart needs to be in order
            # to be right next to the previous heart icon
            # 
            dist_from_prev_heart = self.heart_icons[i].width * i

            # For the ith heart, we need to offset * i in order for the hearts to be
            # offset distance apart; not * i will make the hearts cluttered together
            # 
            x_offset = OFFSET * (i + 1)

            self.heart_icons[i].draw(screen, (dist_from_prev_heart + x_offset,
                                              OFFSET))
        return

    def increment_frames(self):
        """
        Increment the number of frames that the player HUD has been displayed on screen.
        """
        self.HUD_frames_since_shown += 1
        return

