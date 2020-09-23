""" Classes that will represent certain objects and attributes in the Space Viewer game.
    Got some help from these links:
    - https://www.geeksforgeeks.org/python-display-images-with-pygame/#:~:text=load()%20method%20of%20pygame,update()%20method%20of%20pygame.
    - http://programarcadegames.com/python_examples/en/sprite_sheets/
    - https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
    - https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
    - https://stackoverflow.com/questions/19715251/pygame-getting-the-size-of-a-loaded-image/19715931 """
import pygame
import os
from random import randint
from text_box import TextBox
from setup import resource_path

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
                self.img_file_location += "Brown Planet.png"

            self.description = ["A planet where it is summer everyday.",
                                "Mostly heat, sand, and dead plants, but the few oases within this planet",
                                "are teeming with life."]
        elif rng == 3:
            self.img_file_location += "Forest.png"
            self.description = ["A planet that is itself a huge jungle.",
                                "Many insects and furry little creatures coincide peacefully in",
                                "the dark ecosystem covered by the leaves of various tall trees."]
        elif rng == 4:
            rng_ice = randint(1, 2)
            if rng_ice == 1:
                self.img_file_location += "Ice.png"
            elif rng_ice == 2:
                self.img_file_location += "Blue Planet.png"

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
            rng_gas_giants = randint(1, 3)
            if rng_gas_giants == 1:
                self.img_file_location += "Green Gas Giant.png"
            elif rng_gas_giants == 2:
                self.img_file_location += "Grey Gas Giant.png"
            elif rng_gas_giants == 3:
                self.img_file_location += "Pink Gas Giant.png"

            self.description = ["A planet made of solely of air.",
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

            print("A star has appeared...")  # so I know when stars spawn, since they're so rare

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

            print("A moon has appeared...")   # so I know when moons spawn, since they're so rare

        self.img_file_location = resource_path(self.img_file_location)  # set up file location to work with PyInstaller

        self.image = pygame.image.load(self.img_file_location)  # load up the planet img
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # resize planet big enough so we can see it

        # Create the text box for the planet
        self.text_box = TextBox((1350, 400), lines = self.description)  # 3X is the size of the original text box sprite

    """ Draws the planet sprite """
    def draw(self, screen):
       screen.blit(self.image, (CENTER_X - self.size / 2, CENTER_Y - self.size / 2))  # display image at center of screen

    """ Draws the textbox """
    def draw_textbox(self, screen):
       self.text_box.draw(screen, self.frames_since_shown)


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
            print("A black hole has appeared...")

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

        # Create the text box
        self.text_box = TextBox((1350, 400), lines=self.description)  # 3X is the size of the original text box sprite

    """ Draws the space object sprite """
    def draw(self, screen):
        screen.blit(self.image, (CENTER_X - self.size[0] / 2, CENTER_Y - self.size[1] / 2))  # display image at center of screen

    """ Draws the textbox """
    def draw_textbox(self, screen):
        self.text_box.draw(screen, self.frames_since_shown)


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

        self.text_box = TextBox((1350, 400), lines = self.description)  # 3X is the size of the original text box sprite

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
    def draw_textbox(self, screen):
        self.text_box.draw(screen, self.frames_since_shown)

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
        self.size_multiple = size_multiple if size_multiple != None else randint(5, 7)
        self.shown = False  # is the asteroid being currently displayed on the screen
        self.frames_since_shown = 0  # how many frames has the asteroid been displayed on screen
        self.description = ["Testing asteroid sprite.",
                            "These asteroid sprites won't be alone; they will be in an asteroid belt.",
                            "Description is for debugging purposes only."]

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
        self.size = list(self.image.get_rect().size)  # Get the new size of the sprite

        # Create the text box
        self.text_box = TextBox((1350, 400), lines=self.description)  # 3X is the size of the original text box sprite

    """ Draws the asteroid """
    def draw(self, screen):
        screen.blit(self.image, (CENTER_X - self.size[0] / 2, CENTER_Y - self.size[1] / 2))  # display image at center of screen

    """ Draws the textbox """
    def draw_textbox(self, screen):
        self.text_box.draw(screen, self.frames_since_shown)


