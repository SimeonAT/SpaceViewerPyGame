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
from spritesheet import get_frames
from textbox_tree import *

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
        self.size = size if size != None else randint(200, 700)
        self.shown = False
        self.frames_since_shown = 0
        self.description = []

        # These class attributes are only relevant with animated sprites
        self.frames_list = []
        self.total_frames = 0
        self.frame_num = 0
        self.animated = True

        self.img_file_location = os.path.join("Graphics", "Space Objects") + "/"

        rng = randint(1, 10)
        if rng == 1:
            self.img_file_location += "barren_spritesheet.png"
            self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)
            self.description = ["A rocky moon that doesn't orbit around any planet.",
                                "It sits silently within the deep reaches of space..."]

        elif rng == 2:
            rng_desert = randint(1, 2)
            if rng_desert == 1:
                self.img_file_location += "terran_dry.png"
                self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)
            elif rng_desert == 2:
                self.img_file_location += "Brown Planet Animated.png"
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames = 4)

            self.description = ["A planet where it's summer everyday.",
                      "Although the surace is mostly made up of sand dunes and dust storms,",
                                "the few oases within this planet are teeming with life."]
        elif rng == 3:
            self.img_file_location += "Forest Animated.png"
            self.frames_list, self.total_frames = get_frames(5, 15, 34, 34,
                                                                 hanging_frames = 4)

            self.description = ["A planet that is essentially a huge jungle.",
                                "Many insects and furry little creatures coincide peacefully",
                                "together among the various tall trees within the planet."]

        elif rng == 4:
            rng_ice = randint(1, 2)
            if rng_ice == 1:
                self.img_file_location += "Blue Planet Animated.png"
                self.frames_list, self.total_frames = get_frames(5, 15, 34, 34, hanging_frames=4)
            else:
                self.img_file_location += "ice_spritesheet.png"
                self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)

            self.description = ["A cold and barren rogue planet. In spite of the",
                                "lifelessness on its cold surface, various underwater",
                                "creatures live behind the darkness of the ice sheets."]

        elif rng == 5:
            self.img_file_location += "lava_spritesheet.png"
            self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)
            self.description = ["The hottest planet that is not a star. No life exists",
                                "on this planet, but if you are willing to brace the heat,",
                                "you may find some very valuable metals."]

        elif rng == 6:
            self.img_file_location += "ocean_spritesheet.png"
            self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)
            self.description = ["A planet with very few land surfaces, if any.",
                                "Sea creatures thrive here, and advanced",
                                "civilizations can be found deep underwater."]

        elif rng == 7:
            self.img_file_location += "terran_spritesheet.png"
            self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)
            self.description = ["This planet contains all the qualities ideal for sustaining",
                     "various kinds of life. Both land and sea creatures coexist together",
                     "in the various biomes within this planet."]

        elif rng == 8:
            rng_gas_giants = randint(1, 2)
            if rng_gas_giants == 1:
                self.img_file_location += "gas_giant_spritesheet1.png"
                self.frames_list, self.total_frames = get_frames(15, 15, 100, 100)

            elif rng_gas_giants == 2:
                self.img_file_location += "gas_giant_spritesheet2.png"
                self.frames_list, self.total_frames = get_frames(15, 15, 300, 300)

            self.description = ["A planet made solely out of air.",
                                "Birds, bats, and various other flying beasts dominate",
                                "the skies of this hollow planet."]

        elif rng == 9:
            rng_robot = randint(1, 3)
            self.animated = False
            if rng_robot == 1:
                self.img_file_location += "Robot.png"
            elif rng_robot == 2:
                self.img_file_location += "Robot 2.png"
            elif rng_robot == 3:
                self.img_file_location += "Robot 3.png"
            elif rng_robot == 4:
                self.img_file_location += "Robot 4.png"

            self.description = ["A planet once teeming with civilized life...",
                                "until the robots that its inhabitants created took over!",
                     "Now all is left are robots who wander aimlessly, exploiting the planet..."]

        # The following are not 'planets' but are things you would typically see in space 
        # (i.e. sun-like stars and other planetary objects).
        # Although they are not planets, as game sprites they have the exact same behavior as 
        # planets for the purpose of this game. 
        elif rng == 10:
            rng_star = randint(1, 3)
            if rng_star == 1:
                self.img_file_location += "star1.png"
            elif rng_star == 2:
                self.img_file_location += "star2.png"
            elif rng_star == 3:
                self.img_file_location += "star3.png"

            self.frames_list, self.total_frames = get_frames(15, 15, 200, 200)
            self.description = ["A powerful planetary object that radiates with immese heat."]

        # Set up file location to work with PyInstaller
        self.img_file_location = self.img_file_location
        self.image = pygame.image.load(self.img_file_location).convert_alpha()

        # If not animated, we have to scale the image
        if self.animated == False:
            self.image = pygame.transform.scale(self.image,
                                                (self.size, self.size))

        # --- The Textbox Tree ---
        self.description_node = Textbox_Tree_Node(TextBox(lines = self.description))
        self.prompt_node = Textbox_Tree_Node(Choice_TextBox(lines =
                                                    ["Do you want to enter this planet?"]))
        self.yes_node = Textbox_Tree_Node(TextBox(lines = ["Entering Planet..."]))

        self.description_node.next_child = self.prompt_node
        self.prompt_node.yes_child = self.yes_node
        self.tree = Textbox_Tree(self.description_node)

    def draw(self, screen, frames_since_shown):
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

    def increment_textbox_frames(self):
        self.tree.current.increment_frames()
        return

    def reset_textbox_tree(self):
        self.tree.reset_tree()
        return

    def draw_textbox(self, screen, index, player, key_pressed = None):
        """ Parameters:
                screen: the PyGame screen in which to render the text box
                index: what textbox to draw in the text_boxes list
                key_pressed: the key that was pressed by the user
                player: the object that holds data about player,
                        as certain textbox results can positively/negative affect
                        the player

            Returns:
                True -> There are still textboxes left to render
                False -> No textboxes left to render """
        if key_pressed == "enter":
            if not self.tree.current.is_choice_textbox():
                self.tree.next_textbox()
            else:
                if self.choice_result == 0:
                    self.tree.make_choice(True)
                elif self.choice_result == 1:
                    self.tree.make_choice(False)

        if self.tree.current == None:
            # No more textboxes left to render
            return False

        # Render the textbox
        # NOTE: self.choice_result and key_pressed are solely choice textbox variables
        self.choice_result = self.tree.current.textbox_object \
                .draw(screen, self.tree.current.frames_since_shown, key_pressed)
        return True
