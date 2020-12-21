""" Contains a function that converts a spritesheet into a list of
    individual sprite frames.
    - https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
    - https://stackoverflow.com/questions/36653519/how-do-i-get-the-size-width-x-height-of-my-pygame-window """
import pygame

def get_frames(rows, frames_per_row, frame_width, frame_height, hanging_frames = None):
    """@params: rows -> how many rows in the spritesheet
                frames_per_row -> how many frames in each row
                frame_width, frame_height -> the dimensions of each frame in the spritesheet
                hanging_frames -> contains how many frames are in last row when last row < frames_per_row;
                                  'None' means that last row has frames_per_row frames  """
    frames = []  # the list of frames from sprite to return
    num_frames = 0  # how many frames does the spritesheet have?

    # The coordinates of the top left corner of each frame; starts with top left corner of first frame
    x = 0
    y = 0

    # Use a for loop to create a new surface for each individual sprite
    # and store each sprite in the sprites list
    for i in range(1, rows + 1):
        for j in range(1 , frames_per_row + 1):
            frames.append([x, y, frame_width, frame_height])
            num_frames += 1

            x += frame_width  # Get ready for next sprite

            # If on last row and there are hanging frames, break once we got all the hanging frames
            if hanging_frames != None and i == rows:
                if j >= hanging_frames:
                    break

        # Get ready for next row
        x = 0
        y += frame_height

    print(frames)
    return (frames, num_frames)
