""" This module holds the Planet class and everything related to it.

    USEFUL RESOURCES:
    - https://gamedev.stackexchange.com/questions/140609/games-developed-in-python-with-pygame
      -lags-too-much-how-can-i-improve-the-frame
        - The link recommended to use convert() or convert_alpha()
          after loading an inmate to improve performance
"""

import pygame
import os
from random import randint
from text_box import TextBox, Extension_TextBox, Choice_TextBox
from setup import resource_path
from spritesheet import get_frames

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]

CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)

class Planet(pygame.sprite.Sprite):

    def __init__(self, size = None):
        """ Parameters:
                size: The size of the planet sprite, representing both its length and width
        """
        super().__init__()
        self.size = size if size != None else randint(75, 500)
        self.shown = False
        self.frames_since_shown = 0
        self.description = []

        # These class attributes are only relevant with animated sprites
        self.frames_list = []
        self.total_frames = 0
        self.frame_num = 0
        self.animated = False

        self.img_file_location = os.path.join("Graphics", "Space Objects") + "/"

        rng = randint(1, 12)
        if rng == 1:
            self.img_file_location += "Baren.png"
            self.description = ["A rocky moon that doesn't orbit around any planet.",
                                "It sits silently within the deep reaches of space..."]

        elif rng == 2:
            rng_desert = randint(1, 2)
            if rng_desert == 1:
                self.img_file_location += "Desert.png"
            elif rng_desert == 2:
                self.img_file_location += "Brown Planet Animated.png"
                self.animated = True
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames = 4)

            self.description = ["A planet where it's summer everyday.",
                      "Mostly heat, sand, and dead plants, but the few oases within this planet",
                                "are teeming with life."]
        elif rng == 3:
            rng_forest = randint(1, 2)
            if rng_forest == 1:
                self.img_file_location += "Forest.png"
            else:
                self.img_file_location +="Forest Animated.png"
                self.animated = True
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames = 4)

            self.description = ["A planet that is itself a huge jungle.",
                                "Many insects and furry little creatures coincide peacefully in",
                                "the dark ecosystem covered by the leaves of various tall trees."]

        elif rng == 4:
            rng_ice = randint(1, 2)
            if rng_ice == 1:
                self.img_file_location += "Ice.png"
            elif rng_ice == 2:
                self.img_file_location += "Blue Planet.png"
            elif rng_ice == 3:
                self.img_file_location += "Blue Planet Animated.png"
                self.animated = True
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames=4)

            self.description = ["Cold and barren, life within the planet lives",
                                "in the warm caves found underground."]

        elif rng == 5:
            self.img_file_location += "Lava.png"
            self.description = ["Due to its heat, no life exists on this planet.",
                                "But, if you're willing to brace the heat, you can",
                                "find various types of rare metals next to the lava."]

        elif rng == 6:
            self.img_file_location += "Ocean.png"
            self.description = ["A planet where there exists no land.",
                            "Sea creatures thrive here, and advanced civilizations can be found",
                            "deep underwater."]

        elif rng == 7:
            self.img_file_location += "Terran.png"
            self.description = ["A planet ideal for sustainable life.",
                     "Creatures both primitive and civilized coexist together throughout the",
                     "various desert, taiga, forest, jungle, and ocean biomes within this planet."]

        elif rng == 8:
            rng_gas_giants = randint(1, 4)
            if rng_gas_giants == 1:
                self.img_file_location += "Green Gas Giant.png"
            elif rng_gas_giants == 2:
                self.img_file_location += "Grey Gas Giant.png"
            elif rng_gas_giants == 3:
                self.img_file_location += "Pink Gas Giant.png"
            elif rng_gas_giants == 4:
                self.img_file_location += "Purple Planet.png"
                self.animated = True
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames=4)

            self.description = ["A planet made solely out of air.",
                                "Birds, bats, and similar creatures of all kinds",
                                "take flight on its cloudy skies."]

        elif rng == 9:
            rng_robot = randint(1, 3)
            if rng_robot == 1:
                self.img_file_location += "Robot.png"
            elif rng_robot == 2:
                self.img_file_location += "Robot 2.png"
            elif rng_robot == 3:
                self.img_file_location += "Robot 3.png"
            elif rng_robot == 4:
                self.img_file_location += "Robot 4.png"

            self.description = ["A planet that once had civilized life...",
                                "until the robots that its inhabitants created took over!",
                     "Now all is left are robots who wander aimlessly, exploiting the planet..."]

        # The following are not 'planets' but are things you would typically see in space 
        # (i.e. sun-like stars and other planetary objects).
        # Although they are not planets, as game sprites they have the exact same behavior as 
        # planets for the purpose of this game. 
        elif rng == 10:
            rng_star = randint(1, 4)
            if rng_star == 1:
                self.img_file_location += "Blue Star.png"
            elif rng_star == 2:
                self.img_file_location += "Red Star.png"
            elif rng_star == 3:
                self.img_file_location += "Yellow Star.png"
            elif rng_star == 4:
                self.img_file_location += "Pink Star.png"

            self.description = ["A powerful star that radiates with intense cosmic energy.",
                                "Advanced beings from nearby planets harness this energy",
                                "using their advanced technologies."]

        # rng can equal either of two possible numbers to increase 
        # probability of a mooning spawning
        elif rng == 11 or rng == 12:
            rng_moon = randint(1, 5)
            if rng_moon == 1:
                self.img_file_location += "Moon.png"
            elif rng_moon == 2:
                self.img_file_location += "Moon 2.png"
            elif rng_moon == 3:
                self.img_file_location += "Red Moon.png"
            elif rng_moon == 4:
                self.img_file_location += "Blue Moon.png"
            elif rng_moon == 5:
                self.img_file_location += "Pink Moon.png"

            self.description = ["A beautiful looking moon ",
                                "that shines quietly in this ",
                                "peaceful, yet dark, corner of space. "]

        # Set up file location to work with PyInstaller
        self.img_file_location = resource_path(self.img_file_location)

        self.image = pygame.image.load(self.img_file_location).convert_alpha()

        # If not animated, all we need to do is just scale the image
        if self.animated == False:
            self.image = pygame.transform.scale(self.image,
                                                (self.size, self.size))

        self.text_boxes = [TextBox((1350, 400), lines = self.description)]
        self.text_boxes.append(Choice_TextBox((1350, 400),
                                              lines=["Do you want to enter this planet?",
                                                     " "]))
        self.textbox_result = Extension_TextBox((1350, 400), lines = ["Entering Planet..."])

        # A list containing how many frames has each textbox been shown on the screen
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)


    def draw(self, screen):
        if len(self.frames_list) != 0:
            # if 1/15 of a second has passed (assuming 60 FPS), update the frame
            if self.frames_since_shown % 4 == 0:
                self.frame_num += 1

            # if frame_number has reached the end of the spritesheet array
            if self.frame_num > len(self.frames_list) - 1:
                self.frame_num = 0

            # Create a new surface that contains the frame and resize 
            # it so it has dimensions self.size x self.size
            frame_image = self.image.subsurface(self.frames_list[self.frame_num])
            frame_image = pygame.transform.scale(frame_image, (self.size, self.size))

            screen.blit(frame_image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))
        else:
            # This code runs only when there's only 1 frame to deal with
            screen.blit(self.image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))

    def draw_textbox(self, screen, index, key_pressed = None):
        """ Parameters:
                screen: the PyGame screen in which to render the text box
                index: what textbox to draw in the text_boxes list
                key_pressed: the key that was pressed by the user

            Returns:
                True -> There are still textboxes left to render
                False -> No textboxes left to render
         """

        if key_pressed == "enter":
            # main.py increments index by 1 when player pressed ENTER.
            # Thus, in order to display the choice textbox, we need to use index - 1
            self.choice_result = self.text_boxes[index - 1] \
                    .draw(screen, self.textbox_frames_since_shown[index - 1], key_pressed)

            # Player entered "YES"
            if self.choice_result == 0:
                # Append "YES" result textbox to list so it can render
                if self.textbox_result not in self.text_boxes:
                    # make sure textbox result not in text boxes list
                    # as we don't want to include more than 1 copy of it in the list
                    self.text_boxes.append(self.textbox_result)

                    # add an element to textbox frames list to account for new textbox
                    self.textbox_frames_since_shown.append(0)

            # Player entered "NO"
            elif self.choice_result == 1:
                # make sure textbox result is in text box list
                # so that we're not removing something that doesn't exist in list
                if self.textbox_result in self.text_boxes:
                    self.text_boxes.remove(self.textbox_result)

                    # remove element from textbox frames list to remove frames from result textbox
                    self.textbox_frames_since_shown.pop()

        if index > len(self.text_boxes) - 1:
            # Remove textbox result to reset the result of the choices that the player made
            if self.textbox_result in self.text_boxes:
                self.text_boxes.remove(self.textbox_result)
                self.textbox_frames_since_shown.pop()
            return False

        # Render the textbox
        # NOTE: self.choice_result and key_pressed are solely choice textbox variables
        self.choice_result = self.text_boxes[index] \
                .draw(screen, self.textbox_frames_since_shown[index], key_pressed)

        return True
