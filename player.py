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
        self.x, self.y, self.width, self.height = self.heart_image.get_rect()
        print(f"Before scaling: (width, height): {(self.width, self.height)}")
        self.width *= SIZE_MULTIPLE
        self.height *= SIZE_MULTIPLE
        self.heart_image = pygame.transform.scale(self.heart_image,
                           (self.width, self.height))

        self.frames_since_shown = 0
        self.hover_direction = 1
        return

    def draw(self, screen, position = None):
        """
        Draws the heart icon onto the screen.

        Parameters:
            The screen to draw on
            The (x, y) position as a tuple or list
        """
        if position == None:
            position = (self.x, self.y)

        # Change the direction and position every 16 frames (assuming 60 FPS)
        # so the heart displays a "hovering effect" similar to the asteroids
        # if self.frames_since_shown % 16 == 0:
        #    self.hover_direction *= -1
        #    self.y += (self.hover_direction * randint(1, 10))

        screen.blit(self.heart_image, position)
        return

    def increment_frames(self):
        self.frames_since_shown += 1
        return


class Player:

    def __init__(self):
        self.lives = 3
        self.heart_icons = []
        for i in range(0, self.lives):
            self.heart_icons.append(Heart())

        # Determine the position that each heart icon will be in:
        # They will all appear at the top left corner of the screen with
        # OFFSET spaces apart
        for i in range(0, self.lives):
            # The distance that top left coord of current heart needs to be in order 
            # to be right next to the previous heart icon 
            dist_from_prev_heart = self.heart_icons[i].width * i

            # The distance that the ith heart is from the first heart. Each heart
            # will be be OFFSET spaces away from each other.
            x_offset = OFFSET * (i + 1)

            (self.heart_icons[i].x,
             self.heart_icons[i].y) = (dist_from_prev_heart + x_offset, OFFSET)

        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """
        for heart in self.heart_icons:
            heart.draw(screen)
        return

    def increment_frames(self):
        """
        Increment the number of frames that the player HUD has been displayed on screen.
        """
        for heart in self.heart_icons:
            heart.increment_frames()
        return

