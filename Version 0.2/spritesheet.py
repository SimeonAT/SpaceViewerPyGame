""" Contains a function that converts a spritesheet into a list of
    individual sprite frames.
    - https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
    - https://stackoverflow.com/questions/36653519/how-do-i-get-the-size-width-x-height-of-my-pygame-window """
import pygame

def create_sprite_from_spritesheet(file_loc, rows, frames_per_row):
    """@params: file_loc -> the file location of the spritesheet
                rows -> how many rows in the spritesheet
                frames_per_row -> how many frames in each row  """
    frames = []  # the list of frames from sprite to return
    spritesheet = pygame.image.load(file_loc)  # get spritesheet surface from file location
    spritesheet_rect = spritesheet.get_rect()  # so we can find the width and height of spritesheet

    # Get the dimensions of an individual frame
    width = spritesheet_rect.width / frames_per_row
    height = spritesheet_rect.height / rows

    # The coordinates of the top left corner of each frame; starts with top left corner of first frame
    x = 0
    y = 0

    # Use a for loop to create a new surface for each individual sprite
    # and store each sprite in the sprites list
    for i in range(0, rows):
        for j in range(0, frames_per_row):
            frames.append([x, y, width, height])

            x += width  # Get ready for next sprite

        # Get ready for next row
        x = 0
        y += height

    return frames
