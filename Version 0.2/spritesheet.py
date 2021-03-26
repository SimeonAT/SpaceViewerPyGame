"""
Contains a function that converts a spritesheet into a list of
individual sprite frames.
- https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
- https://stackoverflow.com/questions/36653519
  /how-do-i-get-the-size-width-x-height-of-my-pygame-window
"""


def get_frames(rows, frames_per_row, frame_width, frame_height, hanging_frames=None):
    """
    Returns a list containing the position of each individual sprite frame in the spritesheet,
    and the number of frames that are in the spritesheet.

    rows -> how many rows in the spritesheet
    frames_per_row -> how many frames in each row
    frame_width, frame_height -> the dimensions of each frame in the spritesheet
    hanging_frames -> contains how many frames are in last row when last row < frames_per_row;
                      'None' means that last row has frames_per_row frames
    """
    frames = []
    num_frames = 0

    # The coordinates of top left corner of each frame; starts with top left corner of first frame
    x = 0
    y = 0

    # Use a for loop to create a new surface for each individual sprite
    # and store each sprite in the sprites list
    for i in range(1, rows + 1):
        for j in range(1, frames_per_row + 1):
            frames.append([x, y, frame_width, frame_height])
            num_frames += 1

            # Get ready for next sprite
            x += frame_width

            # We break if we're on last row and there are hanging frames to avoid 
            # creating any empty frames
            if hanging_frames is not None and i == rows:
                if j >= hanging_frames:
                    break

        # Get ready for next row
        x = 0
        y += frame_height

    return (frames, num_frames)
