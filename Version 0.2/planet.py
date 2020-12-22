""" This module holds the Planet class and everything related to it. """
import pygame
import os
from random import randint
from text_box import TextBox, Extension_TextBox
from setup import resource_path
from spritesheet import get_frames

# Dimensions of game for module to refer to:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]   # The dimensions of the grid space

# Coordinates for the center of the screen
CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)

class Planet(pygame.sprite.Sprite):
    """ Planet object in Space Viewer video game.
        Some spaces in the grid will have a planet, while other will not.  """

    def __init__(self, size = None):
        """@param: size -> size of dot as int; default is a random size """
        super().__init__()
        self.size = size if size != None else randint(75, 500)
        self.shown = False   # is the planet being currently displayed on the screen
        self.frames_since_shown = 0  # how many frames has the planet been displayed on screen
        self.description = []  # the description of planet, which is displayed on textbox (there is no desc by default)

        """ THESE CLASS ATTRIBUTES ARE ONLY RELEVANT WHEN DEALING WITH ANIMATED SPRITES """
        self.frames_list = []  # contains information about each frame in the spritesheet
                               # if list remains empty after constructor, then the sprite isn't animated.
        self.total_frames = 0  # how many frames does sprite have (# of frames in spritesheet)
        self.frame_num = 0     # what frame to render when drawing
        self.animated = False  # Will sprite be animated (Not animated by default)

        # the file location for the image of the planet
        self.img_file_location = os.path.join("Graphics", "Space Objects") + "\\"

        # Use RNG to decide what type of Planet instance should be
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
                                                                 hanging_frames = 4)  # get the animated frames from spritesheet

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
                                                                 hanging_frames=4)  # get the animated frames from spritesheet

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
                                                                 hanging_frames=4)  # get the animated frames from spritesheet

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

        elif rng == 8:  # Gas Giants
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
                                                                 hanging_frames=4)  # get the animated frames from spritesheet

            self.description = ["A planet made solely out of air.",
                                "Birds, bats, and similar creatures of all kinds",
                                "take flight on its cloudy skies."]

        elif rng == 9:  # Robot Planets
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

        # The following are not 'planets' but are things you would typically see in space (sun-like stars and other planetary objects).
        # For the time being, they will be in the planet class, as although they are not planets, as game sprites they have the
        # exact same behavior as planets. Once the behavior begins to differ (when I further develop the game), then they will
        # have a class dedicated to them.
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


        elif rng == 11 or rng == 12:  # rng can be 2 nums to increase probabilities moon will spawn
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

        self.img_file_location = resource_path(self.img_file_location)  # set up file location to work with PyInstaller

        self.image = pygame.image.load(self.img_file_location)  # load up the planet img

        if self.animated == False:  # If not animated, all we need to do is just scale the image
            self.image = pygame.transform.scale(self.image,
                                                (self.size, self.size))  # resize planet big enough so we can see it

        """ A list that will hold the text boxes for the planets; 
                    description textbox is 3X is the size of the original text box sprite """
        self.text_boxes = [TextBox((1350, 400), lines = self.description)]  # 3X is the size of the original text box sprite
        self.text_boxes.append(Extension_TextBox((1350, 400), lines=["Do you want to enter this planet?",
                                                           " ",
                                                           "Y for YES                     N for NO"]))  # Add the 'choice/prompt' textbox to list

        """ A list containing how many frames has each textbox been shown on the screen. """
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)

    """ Draws the planet sprite """
    def draw(self, screen):
        if len(self.frames_list) != 0:   # if the sprite is animated
            # The first step is to find which frame to render
            if self.frames_since_shown % 4 == 0:  # if 1/15 of a second has passed (assuming 60 FPS), update the frame
                self.frame_num += 1
            if self.frame_num > len(self.frames_list) - 1:  # if frame_number has reached the end of the spritesheet array
                self.frame_num = 0

            # Create a new surface that contains the frame and resize it so it has dimensions self.size x self.size
            frame_image = self.image.subsurface(self.frames_list[self.frame_num])
            frame_image = pygame.transform.scale(frame_image, (self.size, self.size))

            screen.blit(frame_image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))
        else:
            # This code runs only when there's only 1 frame to deal with
            screen.blit(self.image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))  # display image at center of screen

    """ Draws the textbox """
    def draw_textbox(self, screen, index):
        """ - index will hold what textbox to draw in text_boxes list. If index is past what is in self.text_boxes,
                      don't render anything.
            - Will return a boolean value: True if there are still text boxes to render, False if there are no
                      text boxes left to render. This boolean value will be saved in show_textbox in main. """
        if index > len(self.text_boxes) - 1:
            return False

        self.text_boxes[index].draw(screen, self.textbox_frames_since_shown[index])
        return True