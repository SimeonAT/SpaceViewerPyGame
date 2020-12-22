""" Classes that will represent certain objects and attributes in the Space Viewer game.
    Got some help from these links:
    - https://www.geeksforgeeks.org/python-display-images-with-pygame/#:~:text=load()%20method%20of%20pygame,update()%20method%20of%20pygame.
    - http://programarcadegames.com/python_examples/en/sprite_sheets/
    - https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
    - https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
    - https://stackoverflow.com/questions/19715251/pygame-getting-the-size-of-a-loaded-image/19715931
    - https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame """
import pygame
import os
from random import randint
from text_box import TextBox
from setup import resource_path
from spritesheet import get_frames

# Dimensions of game for module to refer to:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]   # The dimensions of the grid space

# Coordinates for the center of the screen
CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)


class Intestellar_Object(pygame.sprite.Sprite):
    """ Any objects in space that is not a planetary object (black holes, nebulas, etc)
        Although similar to the planet objects, they differ in property, size, and
        the player will be able to interact more with them. """

    def __init__(self, size_multiple = None):
        """@params: size_multiple -> should black hole be same size, 2x, 3x, 4x, etc bigger; this is because sprite is rect in shape """
        self.size_multiple = size_multiple if size_multiple != None else randint(3, 5)
        self.shown = False  # is the black hole being currently displayed on the screen
        self.frames_since_shown = 0  # how many frames has the black hole been displayed on screen

        # Load up the sprite depending the planetary object it will be
        rng = randint(1, 5)

        if rng == 1:  # Black Hole
            self.size = [128 * self.size_multiple, 95 * self.size_multiple]  # the actual size of the sprite * the size multiple
            self.img_file_location = resource_path(os.path.join("Graphics", "Space Objects", "Wormhole.png"))
            self.description = ["A black hole that swirls with rage!",
                                "Whatever comes inside...",
                                "...never comes out..."]

        elif rng == 2 or rng == 3:  # Nebula
            self.size = [128 * self.size_multiple, 128 * self.size_multiple]
            self.img_file_location = resource_path(os.path.join("Graphics", "Space Objects", "Nebula.png"))
            self.description = ["The debris of dust, hydrogen, helium, oxygen, and space rocks",
                                "swirl together to create this beautiful mix of ",
                                "cosmic space energy. "]

        elif rng == 4 or rng == 5: # Small Nebula
            self.size = [128 * (self.size_multiple - 1), 33 * (self.size_multiple - 1)]  # subtract by 1 since nebula is small
            self.img_file_location = resource_path(os.path.join("Graphics", "Space Objects", "Small Nebula.png"))
            self.description = ["A small cluster of space debris and dark energy",
                                "laying around as unfinished goods",
                                "at the edge of space."]

        # Load up the sprite img
        self.image = pygame.image.load(self.img_file_location)  # load up the planet img
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))  # resize so it is big enough so we can see it

        """ A list that will hold the text boxes for the space objects; 
                    description textbox is 3X is the size of the original text box sprite """
        self.text_boxes = [TextBox((1350, 400), lines=self.description)]  # 3X is the size of the original text box sprite
        """ A list containing how many frames has each textbox been shown on the screen. """
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)

    """ Draws the space object sprite """
    def draw(self, screen):
        screen.blit(self.image, (CENTER_X - self.size[0] / 2, CENTER_Y - self.size[1] / 2))  # display image at center of screen

    """ Draws the textbox """

    def draw_textbox(self, screen, index):
        """ - index will hold what textbox to draw in text_boxes list. If index is past what is in self.text_boxes,
                      don't render anything.
                    - Will return a boolean value: True if there are still text boxes to render, False if there are no
                      text boxes left to render. This boolean value will be saved in show_textbox in main. """
        if index > len(self.text_boxes) - 1:
            return False

        """ A list containing how many frames has each textbox been shown on the screen. """
        self.text_boxes[index].draw(screen, self.textbox_frames_since_shown[index])
        return True


class Star(pygame.sprite.Sprite):
    """ A star is outer space. Is generated to be very small (1 - 3 pixels) in order to
        give the appearance that it is far away. Unlike Planets and other objects, Stars are going to
        be displaced randomly in all spaces in the grid. """

    def __init__(self):
        super().__init__()
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.width = self.height = randint(1, 4)   # width and height are the same so the stars look like squares (planets)

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
    """ The name says it all. Like the Planets, they have dialogue boxes with flavor text/descriptions, but I'm going to try
        to add turn based combat and trade features to them later on in development. """

    def __init__(self, grid_pos, size = None):
        """ @params: grid_pos -> position of the spaceship on the grid space
                     size -> the size of the spaceship sprite """
        super().__init__()
        self.grid_pos = grid_pos
        self.size = size if size != None else randint(300, 700)
        self.shown = False  # is the spaceship being currently displayed on the screen
        self.frames_since_shown = 0  # how many frames has the spaceship been displayed on screen

        # the images for each frame of the sprite animation
        self.spritesheet = [pygame.image.load(resource_path(os.path.join("Graphics", "Spaceships", "spaceship-1.png"))),
                            pygame.image.load(resource_path(os.path.join("Graphics", "Spaceships", "spaceship-2.png")))]

        # Resize each image in self.spritesheet to the dimensions of self.size
        for index in range(0, len(self.spritesheet)):
            self.spritesheet[index] = pygame.transform.scale(self.spritesheet[index], (self.size, self.size))

        self.frame = 0  # index of self.spritesheet; what frame is the sprite animation on
        self.image = self.spritesheet[self.frame]  # the image of sprite to show in a given frame

        # Set up the text box
        self.text_boxes = []     # a list that will contain all the text boxes for the spaceship
        self.description = None  # the text to display in textbox (set to nothing right now, so we can use rng to determine the desc)
        rng = randint(1, 3)
        if rng == 1:
            self.description = ["A spaceship from an unknown galaxy.", "It looks at your spaceship with curiosity."]
        if rng == 2:
            self.description = ["AN ENEMY SPACESHIP HAS JUST APPEARED!",
                                "Thank god your have your cloaking device on.",
                                "Otherwise, they would have seen you."]
        if rng == 3:
            self.description = ["A Metroid themed spaceship.", "That's cool.", "Didn't know those were real."]

        self.text_boxes.append(TextBox((1350, 400), lines = self.description))   # Add desc textbox to the list
                                                                                 # # 3X is the size of the original text box sprite
        self.text_boxes.append(TextBox((1350, 400), lines = ["Do you want to fight this spaceship?",
                                                             " ",
                                                             "Yes or no?"]))     # Add the 'choice/prompt' textbox to list
        """ A list containing how many frames has each textbox been shown on the screen. """
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)

    """ Update the image to be shown after each frame (so the spaceship can be animated), and draw the spaceship. """
    def draw(self, screen):
        # Update the frame that is being shown
        if self.frames_since_shown % 4 == 0:   # if 1/15 of a second has passed (assuming 60 FPS), update the frame
            self.frame += 1
        if self.frame > len(self.spritesheet) - 1:  # if frame_number has reached the end of the spritesheet array
            self.frame = 0
        self.image = self.spritesheet[self.frame]   # update the image shown based on changes to self.frame

        # Draw the sprite
        screen.blit(self.image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))  # display image at center of screen

    """ Draws the textbox """
    def draw_textbox(self, screen, index):
        """ - index will hold what textbox to draw in text_boxes list. If index is past what is in self.text_boxes,
              don't render anything.
            - Will return a boolean value: True if there are still text boxes to render, False if there are no
              text boxes left to render. This boolean value will be saved in show_textbox in main. """
        if index > len(self.text_boxes) - 1:
            return False

        """ A list containing how many frames has each textbox been shown on the screen. """
        self.text_boxes[index].draw(screen, self.textbox_frames_since_shown[index])
        return True

    """ Update the position of the spaceship, which moves to a different space each time the player moves. 
        This will allow us to simulate the 'movement' of spaceships. """
    def update(self):
        # The new coordinates of the Spaceship
        horizontal = randint(0, GRID_SIZE[0] - 1)
        vertical = randint(0, GRID_SIZE[1] - 1)

        # Update positions
        self.grid_pos[0] = horizontal
        self.grid_pos[1] = vertical

        return self.grid_pos   # return the new grid position of the spaceship


class Asteroid(pygame.sprite.Sprite):
    """ Asteroids, space rock. These asteroids will be grouped together
    as an asteroid belt in-game. """

    def __init__(self, pos = None, size_multiple = None):
        """@params: pos -> position of the asteroid on screen
                    size_multiple -> should asteroid be 1x, 2x, 3x, 4x, etc bigger?
           NOTE: Parameters are set to none and are given random values in initialization """
        super().__init__()
        self.size_multiple = size_multiple if size_multiple != None else randint(1, 5)
        self.shown = False  # is the asteroid being currently displayed on the screen
        self.frames_since_shown = 0  # how many frames has the asteroid been displayed on screen

        """ Load up which sprite graphic to use """
        self.img_file_location = os.path.join("Graphics", "Space Objects") + "\\"
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
        self.image = pygame.image.load(self.img_file_location)  # load up the planet img
        self.size = self.image.get_rect().size  # Get the size of the sprite
        self.image = pygame.transform.scale(self.image, (self.size[0] * self.size_multiple, self.size[1] * self.size_multiple))
        self.size = [self.size[0] * self.size_multiple, self.size[1] * self.size_multiple]  # Get the new size of the sprite

        # Determine the position of the asteroid
        LIMIT_X = SCREEN_WIDTH - self.size[0]  # has to be at least a width/height away so that asteroid stays on screen
        LIMIT_Y = SCREEN_HEIGHT - self.size[1]
        self.pos = pos if pos != None else randint(0, LIMIT_X), randint(0, LIMIT_Y)

    """ Draws the asteroid """
    def draw(self, screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))  # display image at self.pos


class Asteroid_Belt(pygame.sprite.Sprite):
    """ A list of individual asteroids that will be shown on the screen at the same time. """

    def __init__(self):
        self.quantity = randint(30, 50)   # how many asteroids to display
        self.asteroid_belt = []  # the list of asteroids
        self.frames_since_shown = 0  # how many frames has the asteroid been displayed on screen

        # Put some Asteroid objects (with random features) in the Asteroid Belt
        for index in range(self.quantity):
            self.asteroid_belt.append(Asteroid())

        # Textbox objection and descriptions
        self.description = ["A large field of stray, floating asteroids.",
                            "They are composed of debris from dead planets, ",
                            "and are space rocks with tones of gems and minerals. "]

        """ A list that will hold the text boxes for the asteroid belt; 
            description textbox is 3X is the size of the original text box sprite """
        self.text_boxes = [TextBox((1350, 400), lines = self.description)]

        """ A list containing how many frames has each textbox been shown on the screen. """
        self.textbox_frames_since_shown = [0] * len(self.text_boxes)

    """ Draws the asteroid belt """
    def draw(self, screen):
        for asteroid in self.asteroid_belt:
            asteroid.draw(screen)

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
