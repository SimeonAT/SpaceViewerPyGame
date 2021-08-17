""" Classes that will represent certain objects and attributes in the Space Viewer game.

    USEFUL RESOURCES:
    - https://www.geeksforgeeks.org/python-display-images-with-pygame/
      #:~:text=load()%20method%20of%20pygame,update()%20method%20of%20pygame.
    - http://programarcadegames.com/python_examples/en/sprite_sheets/
    - https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
    - https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
    - https://stackoverflow.com/questions/19715251/pygame-getting-the
      -size-of-a-loaded-image/19715931
    - https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame """

import pygame
import os
from random import randint, randrange
from text_box import TextBox, Extension_TextBox, Choice_TextBox
from setup import resource_path
from spritesheet import get_frames
from textbox_tree import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]

CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)


class Intestellar_Object(pygame.sprite.Sprite):
    """ This class refers to all instances that are non-planetary interstellar objects
        (i.e. black holes, nebulas, and so on). """

    def __init__(self, size_multiple = None):
        """ Parameters:
                size_multiple: The factor to increase the size of the sprite by

            Returns:
                No return value; just creates a new intestellar object
        """
        self.size_multiple = size_multiple if size_multiple != None else randint(3, 5)
        self.shown = False
        self.frames_since_shown = 0

        # rng == 1 -> black hole 
        # rng == 2 -> nebula
        #rng == 3-> small nebula
        rng = randint(1, 3)
        if rng == 1:
            self.size = [128 * self.size_multiple, 95 * self.size_multiple]
            self.img_file_location = \
                resource_path(os.path.join("Graphics", "Space Objects", "Wormhole.png"))
            self.description = ["A black hole that SWIRLS WITH RAGE!!!",
                                "Whatever comes in...",
                                "...never comes out."]
        elif rng == 2:
            self.size = [128 * self.size_multiple, 128 * self.size_multiple]
            self.img_file_location = \
                    resource_path(os.path.join("Graphics", "Space Objects", "Nebula.png"))
            self.description = ["The debris of dust, hydrogen, helium, oxygen, and space rocks",
                                "swirl together to create this beautiful mix of ",
                                "cosmic space energy. "]
        elif rng == 3:
            self.size = [128 * (self.size_multiple - 1), 33 * (self.size_multiple - 1)]
            self.img_file_location = \
                    resource_path(os.path.join("Graphics", "Space Objects", "Small Nebula.png"))
            self.description = ["A small cluster of space debris and dark energy",
                                "laying around as unfinished goods",
                                "at the edge of space."]

        self.image = pygame.image.load(self.img_file_location).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))

        # 1350 x 400 is three times the size of the original text box sprite
        self.text_boxes = [TextBox((1350, 400), lines=self.description)]
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)


    def draw(self, screen, frames_since_shown):
        screen.blit(self.image, (CENTER_X - self.size[0] / 2, CENTER_Y - self.size[1] / 2))


    def draw_textbox(self, screen, index, key_pressed=None):
        """ Parameters:
                index: the index for the text box that should be drawn in the text_boxes list
                key_pressed: the key value that has been pressed by the user

            Returns:
                True -> there are still text boxes left to render
                False -> No more text boxes left to render """
        if index > len(self.text_boxes) - 1:
            return False

        if key_pressed != None:
            self.text_boxes[index].draw(screen, self.textbox_frames_since_shown[index], key_pressed)
        else:
            self.text_boxes[index].draw(screen, self.textbox_frames_since_shown[index])

        return True


class Star(pygame.sprite.Sprite):
    """ A star is outer space. Is generated to be very small (1 - 3 pixels) in order to give the
        appearance that it is far away. Unlike Planets and other objects, Stars are going to
        be displaced randomly in all spaces in the grid. """

    def __init__(self):
        super().__init__()
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.width = self.height = randint(1, 4)

        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()
        self.rect.x = randint(0, SCREEN_WIDTH)
        self.rect.y = randint(0, SCREEN_HEIGHT)

    def update(self, screen):
        self.rect.x = randint(0, SCREEN_WIDTH)
        self.rect.y = randint(0, SCREEN_HEIGHT)
        self.width = randint(1, 10)
        self.height = randint(1, 10)


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, grid_pos, size = None):
        """ Parameters:
                grid_pos: the [row, column]/(row, column) position of the spaceship on the grid
                size: the size of the spaceship sprite

            Returns:
                No return value """
        super().__init__()
        self.grid_pos = grid_pos
        self.size = size if size != None else randint(300, 700)
        self.shown = False
        self.frames_since_shown = 0

        self.spritesheet = [pygame.image.load(resource_path(os.path.join("Graphics",
                                 "Spaceships", "spaceship-1.png"))).convert_alpha(),
                            pygame.image.load(resource_path(os.path.join("Graphics",
                                 "Spaceships", "spaceship-2.png"))).convert_alpha()]

        # Resize each image in self.spritesheet to the dimensions of self.size
        for index in range(0, len(self.spritesheet)):
            self.spritesheet[index] = \
                pygame.transform.scale(self.spritesheet[index], (self.size, self.size))

        # What frame is the sprite animation on; also the index for self.spritesheet
        self.frame = 0
        self.image = self.spritesheet[self.frame]

        self.text_boxes = []
        self.description = None

        rng = randint(1, 3)
        if rng == 1:
            self.description = ["Just another passing spaceship from a nearby planet."]
        if rng == 2:
            self.description = ["AN ENEMY SPACESHIP HAS JUST APPEARED!",
                                "The spaceship has detected you and its targeting computer",
                                "is aimed right at you!"]
        if rng == 3:
            self.description = ["The creatures inside the spaceship look at you with",
                                "curious eyes."]

        self.text_boxes.append(TextBox((1350, 400), lines = self.description))
        self.text_boxes.append(Choice_TextBox((1350, 400), lines =
                                              ["Do you want to fight this spaceship?", " "]))
        self.textbox_result = Extension_TextBox((1350, 400), lines =
                                              ["Spaceship battle will happen here.",
                                               "But it is still in development right now."])

        # A list containing how many frames has each textbox been shown on the screen
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)


    def draw(self, screen, frames_since_shown):
        if self.frames_since_shown % 4 == 0:
            # if 1/15 of a second has passed (assuming 60 FPS), update the frame
            self.frame += 1

        # if frame_number has reached the end of the spritesheet array
        if self.frame > len(self.spritesheet) - 1:
            self.frame = 0
        self.image = self.spritesheet[self.frame]

        screen.blit(self.image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))
        return


    def draw_textbox(self, screen, index, key_pressed=None):
        """ Parameters:
                screen: the PyGame screen in which to render the text box
                index: what textbox to draw in the text_boxes list
                key_pressed: the key that was pressed by the user

            Returns:
                True -> There are still textboxes left to render
                False -> No textboxes left to render
            """

        if key_pressed == "enter":
            # main.py increments index by 1 when ENTER is pressed
            # Thus, in order to display the choice textbox, we need to use index - 1
            self.choice_result = self.text_boxes[index - 1] \
                .draw(screen, self.textbox_frames_since_shown[index - 1], key_pressed)

            # Player chose "YES"
            if self.choice_result == 0:
                # Append "YES" result textbox to list so it can render the "YES" outcome.
                if self.textbox_result not in self.text_boxes:
                    # Make sure textbox result not in text boxes list,
                    # as we don't want to include more than 1 copy of it in the list
                    self.text_boxes.append(self.textbox_result)

                    # add an element to textbox frames list to account for new textbox
                    self.textbox_frames_since_shown.append(0)

            # Player Chose "NO"
            elif self.choice_result == 1:
                # make sure textbox result is in text box list
                # so that we're not removing something that doesn't exist in list
                if self.textbox_result in self.text_boxes:
                    self.text_boxes.remove(self.textbox_result)

                    # remove element from textbox frames list to remove frames from result textbox
                    self.textbox_frames_since_shown.pop()

        if index > len(self.text_boxes) - 1:
            # Remove textbox result so that we can reset the result of 
            # the choices that the player made
            if self.textbox_result in self.text_boxes:
                self.text_boxes.remove(self.textbox_result)
                self.textbox_frames_since_shown.pop()
            return False

        # Render the textbox
        # NOTE: self.choice_result and key_pressed are only choice textbox class attributes
        self.choice_result = self.text_boxes[index] \
                .draw(screen, self.textbox_frames_since_shown[index], key_pressed)

        return True


    def update(self):
        """ Updates the position of the spaceship, which allows the spaceship to move to
            a different space each time the player moves.
            This will allow us to simulate the 'movement' of a spaceship. """
        horizontal = randint(0, GRID_SIZE[0] - 1)
        vertical = randint(0, GRID_SIZE[1] - 1)
        self.grid_pos[0] = horizontal
        self.grid_pos[1] = vertical
        return self.grid_pos


class Asteroid(pygame.sprite.Sprite):
    """ The class for individual asteroid instances. These asteroids will be grouped together
        as an asteroid belt in-game. """

    def __init__(self, pos = None, size_multiple = None):
        """ Parameters:
               pos: position of the asteroid on the screen represented as either
                    [row, column] or (row, column)
               size_multiple: the factor to increase the size of the asteroid sprite

               NOTE: Parameters are set to none and are given random values in initialization """
        super().__init__()
        self.size_multiple = size_multiple if size_multiple != None else randint(1, 5)
        self.shown = False
        self.frames_since_shown = 0
        self.hover_direction = 1

        # Load up which sprite graphic to use
        self.img_file_location = os.path.join("Graphics", "Space Objects") + "/"
        rng = randint(1, 4)
        if rng == 1:
            self.img_file_location += "Asteroid 1.png"
        elif rng == 2:
            self.img_file_location += "Asteroid 2.png"
        elif rng == 3:
            self.img_file_location += "Asteroid 3.png"
        elif rng == 4:
            self.img_file_location += "Asteroid 4.png"

        # Load up the sprite img and resize it by factor of size_multiple
        self.image = pygame.image.load(self.img_file_location).convert_alpha()
        self.size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.size[0] * self.size_multiple,
                                                         self.size[1] * self.size_multiple))
        self.size = [self.size[0] * self.size_multiple, self.size[1] * self.size_multiple]

        # Determine the position of the asteroid
        LIMIT_X = SCREEN_WIDTH - self.size[0]
        LIMIT_Y = SCREEN_HEIGHT - self.size[1]
        self.pos = pos if pos != None else randint(0, LIMIT_X), randint(0, LIMIT_Y)

    def draw(self, screen, frames_since_shown):

        # Slightly change position every 16 frames to display a "hovering"
        # effect on the asteroid
        if frames_since_shown % 16  == 0:

            # Hover direction can only either be -1 and 1, which when multiplied
            # with the x of y position can make the asteroid sprite
            # move up and down, or left and right, respectively.
            if self.hover_direction == 1:
                self.hover_direction = -1
            else:
                self.hover_direction = 1

            self.pos = (self.pos[0] + randint(1, 10) * self.hover_direction,
                        self.pos[1] + randint(1, 10) * self.hover_direction)

        screen.blit(self.image, (self.pos[0], self.pos[1]))
        return


class Asteroid_Belt(pygame.sprite.Sprite):
    """ A collection of individual asteroids that will be simultaneously shown on the screen. """

    def __init__(self):
        self.quantity = randint(30, 50)
        self.asteroid_belt = []
        self.frames_since_shown = 0

        for index in range(self.quantity):
            self.asteroid_belt.append(Asteroid())

        self.description = ["A large field of stray, floating asteroids.",
                            "The asteroids themselves are made up of mineral, space rocks, and",
                            "the debris of countless dead planets."]

        # The Textbox Tree will manage the which textboxes should render next given
        # the player input. More info on this ADT can be found in textbox_tree.py.
        #
        self.head_node = Textbox_Tree_Node(TextBox((1350, 400),
                                                            lines = self.description))
        self.head_node.next_child = Textbox_Tree_Node(Choice_TextBox((1350, 400),
                               lines = ["Do you want to mine this asteroid belt?", " "]))
        self.tree = Textbox_Tree(self.head_node)

        # used to determine the choice the player made on the choice text box
        self.choice_result = None

    def draw(self, screen, frames_since_shown):
        for asteroid in self.asteroid_belt:
            asteroid.draw(screen, frames_since_shown)
        return

    def random_item(self):
        """ Generates a random item that can be found on asteroid when mining """
        rng = randint(1, 3)
        if rng == 1:
            self.textbox_result.lines[2] = "{} bars of sulfurite!".format(randint(0, 1000))
        elif rng == 2:
            self.textbox_result.lines[2] = "{} mythril ores!".format(randint(0, 500))
        elif rng == 3:
            self.textbox_result.lines[2] = "{} gold!".format(randrange(0, 100000))
        return


    def draw_textbox(self, screen, index, key_pressed):
        """ Parameters:
                screen: the PyGame screen in which to render the text box
                index: what textbox to draw in the text_boxes list
                key_pressed: the key that was pressed by the user

            Returns:
                True -> There are still textboxes left to render
                False -> No textboxes left to render
        """

        if key_pressed == "enter":
            # main.py increments index by 1 when ENTER is pressed.
            # Thus, in order to display the choice textbox, we need to use index - 1.
            self.choice_result = self.tree.current.textbox_object \
            .draw(screen, self.tree.current.frames_since_shown,
                                                 key_pressed)

            if self.choice_result == 0:
                self.tree.make_choice(True)
            elif self.choice_result == 1:
                self.tree.make_choice(False)
                return False

        # Render the textbox
        # NOTE: self.choice_result and key_pressed variables are used only for choice text boxes
        print(self.tree.current)
        self.choice_result = self.tree.current.textbox_object.draw(screen,
                                             self.tree.current.frames_since_shown, key_pressed)

        return True

    def increment_textbox_frames(self):
        self.tree.current.increment_frames()
        return

    def reset_textbox_tree(self):
        self.tree.reset_tree()
