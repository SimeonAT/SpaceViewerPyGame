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
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()

    def draw(self, screen):
        # The heart sprite, along with the number of lives the player has,
        # will always be shown at the top left corner of the screen
        screen.blit(self.heart_image,(0, 0))
        return

