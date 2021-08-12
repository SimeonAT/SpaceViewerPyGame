from os import environ
import pygame
import sound
from random import randint
from game_objects import Star, Spaceship, Intestellar_Object, Asteroid_Belt
from planet import Planet

# TURNS OFF 'WELCOME TO PYGAME MESSAGE'
# Got some help here: https://stackoverflow.com/questions/54246668/how-do-i-delete-the-hello
#                     -from-the-pygame-community-console-alert-while-using/54246669
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()
sound.initialize_music()

DIMENSIONS = [1280, 720]
GRID_SIZE = [10, 10]

screen = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("A Randomly Generated Space Game")
clock = pygame.time.Clock()  # FPS of game

list_of_spaceships = []

# current location of player
current_pos = [0, 0]

"""
Create the 'game board': a 20 x 20 grid where each space in the grid contains an object
(planet,space station, enemy spaceship, black hole, etc).
Got some help here: https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
"""
grid = [[None for i in range(GRID_SIZE[0])] for j in range(GRID_SIZE[1])]

for row in range(0, GRID_SIZE[0]):
    for column in range(0, GRID_SIZE[1]):
        """
        Decide what to place in the grid:
            0 -> nothing
            1 -> a planet
            2 -> a spaceship
            3 -> interstellar object
            4 -> asteroid belt
        """
        rng = randint(0, 4)

        """
        grid[row][column] will contain a LIST of game objects,
        so that we can have more than one game object in one grid space.
        """
        if rng == 0:
            grid[row][column] = []
        if rng == 1:
            grid[row][column] = [Planet()]
        if rng == 2:
            new_spaceship = Spaceship([row, column])
            grid[row][column] = [new_spaceship]
            list_of_spaceships.append(new_spaceship)
        if rng == 3:
            grid[row][column] = [Intestellar_Object()]
        if rng == 4:
            grid[row][column] = [Asteroid_Belt()]

"""
Generate a list of 100 Star objects. These same stars will change color and position each time user
moves to a different pos so we don't have to keep creating new stars for each space player goes to.
This will save runtime and memory.
"""
star_list = pygame.sprite.Group()
for i in range(0, 100):
    a_star = Star()
    star_list.add(a_star)

# did player press quit yet?
quit = False

# should the text boxes of the current obj be shown this frame?
show_textbox = True

# what text box to render in text_boxes list
textbox_index = 0

# IF WASD was pressed (if any) by the user; Used for textbox purposes
key_pressed = None

while not quit:
    # clear the screen so that the previous frame is not 'saved'
    screen.fill((0, 0, 0))

    # Do not use pygame.event.wait(). Use pygame.event.get().
    # RESOURCE:
    #   https://stackoverflow.com/questions/56962469/display-fps-is-0-when-nothing-is-happening
    for event in pygame.event.get():
        # Did the player click the window close button?
        if event.type == pygame.QUIT:
            quit = True
            break

        # If player pressed arrow keys, then move player to corresponding tile.
        # Help from these links:
        # - https://opensource.com/article/17/12/game-python-moving-player
        # - https://stackoverflow.com/questions/7053971/python-trouble-using-escape-key-to-exit
        if event.type == pygame.KEYDOWN:
            # keep track of previous position of player
            previous_current_pos = current_pos[:]

            if (event.key == pygame.K_LEFT):
                current_pos[0] -= 1
            elif (event.key == pygame.K_RIGHT):
                current_pos[0] += 1
            elif (event.key == pygame.K_UP):
                current_pos[1] += 1
            elif (event.key == pygame.K_DOWN):
                current_pos[1] -= 1
            elif (event.key == pygame.K_RETURN):
                # if ENTER key (aka "Carriage Return") is pressed, show the next textbox
                textbox_index += 1
                key_pressed = "enter"
            elif (event.key == pygame.K_a):
                # to 'move left' when a textbox is shown
                key_pressed = "a"
            elif (event.key == pygame.K_d):
                # to 'move right' when textbox is shown
                key_pressed = "d"

            # Need if statement so stars ONLY CHANGE when player pos changes
            if previous_current_pos != current_pos:
                star_list.update(screen)
                show_textbox = True

                # If there is an object in the previous position
                if grid[previous_current_pos[0] % 10][previous_current_pos[1] % 10]:
                    # the objects from last frame are not being shown anymore
                    for object in grid[previous_current_pos[0] % 10][previous_current_pos[1] % 10]:
                        object.shown = False
                        object.frames_since_shown = 0  # reset frames since shown

                        for i in range(0, len(object.textbox_frames_since_shown)):
                            # reset frames since shown for each textbox
                            object.textbox_frames_since_shown[i] = 0

                        textbox_index = 0

                for spaceship in list_of_spaceships:
                    """
                    1. Remove the spaceship from its original location on the grid
                    2. Update the position of the spaceship
                    3. Check if new position overlaps with another game object;
                       if so repeat steps 1-3 until it doesn't overlap
                    4. Add the spaceship to the list of the new location on the grid
                    """
                    # does new pos overlap with another game obj
                    not_overlap = False
                    while not not_overlap:
                        # remove spaceship from old position
                        old_pos = spaceship.grid_pos
                        grid[old_pos[0]][old_pos[1]].remove(spaceship)

                        # set new position for spaceship
                        new_pos = spaceship.update()
                        grid[new_pos[0]][new_pos[1]].append(spaceship)

                        # Check if spaceship does not overlap with other game objects
                        if len(grid[new_pos[0]][new_pos[1]]) == 1:
                            not_overlap = True

    """ --- DRAW EVERYTHING IN TILE --- """
    star_list.draw(screen)
    if grid[current_pos[0] % 10][current_pos[1] % 10]:
        # draw objects that are on tile if there is object to be drawn
        for object in grid[current_pos[0] % 10][current_pos[1] % 10]:
            object.shown = True
            object.frames_since_shown += 1
            object.draw(screen, object.frames_since_shown)

        # display the text box, but 'close' (don't display)
        # textbox if player pressed 'z' (show_textbox == false)
        if show_textbox:
            # TEMPORARY SOLUTION: Draw the textbox for each object on the grid space
            for object in grid[current_pos[0] % 10][current_pos[1] % 10]:
                show_textbox = object.draw_textbox(screen, textbox_index, key_pressed=key_pressed)

                if not show_textbox:
                    # if no more textboxes to render,
                    # reset index so that we can render first textbox for next obj
                    textbox_index = 0
                else:
                    object.textbox_frames_since_shown[textbox_index] += 1

    pygame.display.flip()
    clock.tick(60)  # 60 FPS
    key_pressed = None
    sound.play_music(sound.main_loop)

pygame.quit()
