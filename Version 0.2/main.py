from os import environ
# TURNS OFF 'WELCOME TO PYGAME MESSAGE'
# Got some help here: https://stackoverflow.com/questions/54246668/how-do-i-delete-the-hello-from-the-pygame-community-console-alert-while-using/54246669
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sound
from random import randint
from game_objects import Star, Spaceship, Intestellar_Object, Asteroid_Belt
from planet import Planet
from setup import resource_path

pygame.init()  # initialize Pygame library
sound.initialize_music()  # initialize Pygame music via music module

# Dimensions of the screen
DIMENSIONS = [1280, 720]  # [WIDTH, HEIGHT]
GRID_SIZE = [10, 10]   # The dimensions of the grid space

""" Set up the usual basics: """
screen = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("A Randomly Generated Space Game")
clock = pygame.time.Clock()  # FPS of game

list_of_spaceships = []  # contains all spaceships in game, so we can update their locations each frame quickly and easily

""" Create the 'game board': a 20 x 20 grid where each space in the grid contains an object (a planet, a space station, 
    an enemy spaceship, a black hole, etc).
    Got some help here: https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/ """
grid = [[None for i in range(GRID_SIZE[0])] for j in range(GRID_SIZE[1])]  # None means no objects in that space -> just the beautiful view of outer space
for row in range(0, GRID_SIZE[0]):
    for column in range(0, GRID_SIZE[1]):
        """ Decide what to place in the grid:
            0 -> nothing
            1 -> a planet
            2 -> a spaceship
            3 -> interstellar object
            4 -> asteroid belt """
        rng = randint(0, 4)

        """ grid[row][column] will contain a LIST of game objects, and every game object in that grid position will be 
            drawn when the player is on it. This is so that we can have more than one game object in one grid space. """
        if rng == 0:
            grid[row][column] = []  # base case; if nothing is on grid space, then empty list
        if rng == 1:
            grid[row][column] = [Planet()]  # place planet object on space in grid
        if rng == 2:
            new_spaceship = Spaceship([row, column])
            grid[row][column] = [new_spaceship]  # spaceship object on grid
            list_of_spaceships.append(new_spaceship)  # add spaceship to list of spaceships
        if rng == 3:
            grid[row][column] = [Intestellar_Object()]  # A non-planetary object in grid space
        if rng == 4:
            grid[row][column] = [Asteroid_Belt()]   # Asteroid Belt space object


current_pos = [0, 0]  # current location of player

""" Generate a list of 100 Star objects. These same stars will change color and position each time user 
    moves to a different pos so we don't have to keep creating new stars for each space player goes to. This will 
    save runtime and memory. """
star_list = pygame.sprite.Group()
for i in range(0, 100):
    a_star = Star()
    star_list.add(a_star)


""" --- Main Game Loop --- """
quit = False  # did the player press quit yet?
show_textbox = True  # should the text boxes of the current obj be shown this frame?
textbox_index = 0    # what text box to render in text_boxes list
key_pressed = None   # IF WASD was pressed (if any) by the user; "None" means WASD was not pressed; Used for textbox purposes

while quit == False:
    screen.fill((0, 0, 0))  # clear the screen so that the previous frame is not 'saved'

    """ Do not use pygame.event.wait(). Use pygame.event.get(). Using wait is why your code is having super 
        low frame rates when nothing is happening. 
        RESOURCE: https://stackoverflow.com/questions/56962469/display-fps-is-0-when-nothing-is-happening """
    for event in pygame.event.get():
        # Did the player click the window close button?
        if event.type == pygame.QUIT:
            quit = True
            break

        """ If player pressed arrow keys, then move player to corresponding tile. 
            Help from these links: https://opensource.com/article/17/12/game-python-moving-player 
                                   https://stackoverflow.com/questions/7053971/python-trouble-using-escape-key-to-exit """
        if event.type == pygame.KEYDOWN:
            previous_current_pos = current_pos[:]  # the previous position of the player
            if (event.key == pygame.K_LEFT):  # move left
                current_pos[0] -= 1
            elif (event.key == pygame.K_RIGHT): # move right
                current_pos[0] += 1
            elif (event.key == pygame.K_UP):  # move up
                current_pos[1] += 1
            elif (event.key == pygame.K_DOWN):  # move down
                current_pos[1] -= 1
            elif (event.key == pygame.K_RETURN):
                # if ENTER key (aka "Carriage Return") is pressed, show the next textbox
                textbox_index += 1
                key_pressed = "enter"
            elif (event.key == pygame.K_a):
                key_pressed = "a"      # to 'move left' when a textbox is shown
            elif (event.key == pygame.K_d):
                key_pressed = "d"      # to 'move right' when a textbox is shown

            if previous_current_pos != current_pos:  # so that a random key press can't move the stars
                star_list.update(screen)  # reset stars and draw them at new positions
                show_textbox = True  # the textbox is shown for each new obj by default

                # If there is an object in the previous position
                if grid[previous_current_pos[0] % 10][previous_current_pos[1] % 10]:  # if grid[row][column] is not empty
                    # the objects from last frame are not being shown anymore
                    for object in grid[previous_current_pos[0] % 10][previous_current_pos[1] % 10]:
                        object.shown = False
                        object.frames_since_shown = 0  # reset frames since shown
                        for i in range(0, len(object.textbox_frames_since_shown)):
                            object.textbox_frames_since_shown[i] = 0   # reset frames since shown for each textbox
                        textbox_index = 0

                """ Update the position of each spaceship when the user moves a space """
                for spaceship in list_of_spaceships:
                    """ 1. Remove the spaceship from its original location on the grid
                        2. Update the position of the spaceship
                        3. Check if new position overlaps with another game object; if so repeat steps 1-3 until it doesn't overlap 
                        4. Add the spaceship to the list of the new location on the grid """
                    """ ------- """
                    not_overlap = False  # does new position overlap with another game obj
                    while not_overlap == False:
                        # remove spaceship from old position
                        old_pos = spaceship.grid_pos
                        grid[old_pos[0]][old_pos[1]].remove(spaceship)

                        new_pos = spaceship.update()  # set new position for spaceship
                        grid[new_pos[0]][new_pos[1]].append(spaceship)  # put spaceship in new pos

                        # Check if spaceship does not overlap with other game objects
                        if len(grid[new_pos[0]][new_pos[1]]) == 1:  # space should only have 1 obj (the spaceship)
                            not_overlap = True


    """ --- DRAW EVERYTHING IN TILE --- """
    star_list.draw(screen)
    if grid[current_pos[0] % 10][current_pos[1] % 10]:  # did everything % 10 so that pos will be in range between 0-9
        # draw objects that are on tile if there is object to be drawn
        for object in grid[current_pos[0] % 10][current_pos[1] % 10]:
            object.shown = True   # the obj is being shown on screen right now
            object.frames_since_shown += 1
            object.draw(screen)  # draw the object sprite

        # display the text box, but 'close' (don't display) textbox if player pressed 'z' (show_textbox == false)
        if show_textbox == True:
            """ TEMPORARY SOLUTION: Draw the textbox for each object on the grid space """
            for object in grid[current_pos[0] % 10][current_pos[1] % 10]:
                show_textbox = object.draw_textbox(screen, textbox_index, key_pressed = key_pressed)

                if show_textbox == False:   # if there are no more text boxes to render
                    textbox_index = 0       # reset index  so that we can render first textbox for next obj
                else:
                    # the specific textbox has been shown for += 1 frames already
                    object.textbox_frames_since_shown[textbox_index] += 1


    """ --- Update frame rate, Show what's displayed on screen, Play music """
    pygame.display.flip()  # show everything that's drawn
    clock.tick(60)  # 60 FPS
    key_pressed = None      # Reset as no key as been pressed so far
    # sound.play_music(sound.main_loop)  # play main game loop music

pygame.quit()
