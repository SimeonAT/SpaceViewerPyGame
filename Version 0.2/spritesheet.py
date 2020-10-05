""" Contains a function that converts a spritesheet into a list of
    individual sprite frames.
    - https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame """
import pygame

def create_spritesheet(file_loc, rows, columns):
    """@params: file_loc -> the file location of the spritesheet
                rows -> sprites per row
                columns -> sprites per column """
    sprite = []  # the list of sprite surfaces to return
    spritesheet = pygame.image.load(file_loc)  # get spritesheet surface from file location
    spritesheet_rect = spritesheet.get_rect()  # so we can find the width and height of spritesheet

    # Get the dimensions of an individual sprite in the spritesheet
    width = spritesheet_rect.width / rows
    height = spritesheet_rect.height / columns

    # Use a for loop to create a new surface for each individual sprite
    # and store each sprite in the sprites list



