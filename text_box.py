"""
Manages the functionality of dialogue and text boxes for the video game.
USEFUL RESOURCES:
- https://stackoverflow.com/questions/328061
  /how-to-make-a-surface-with-a-transparent-background-in-pygame
- https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
"""
import pygame
import os
from setup import resource_path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)


class TextBox(pygame.sprite.Sprite):
    """ Class template for text and dialogue boxes. """

    def __init__(self, size=(452, 93), lines=[]):
        """
        size -> tuple containing dimensions of the text box
        lines -> a list of strings; each element is a line to display on the textbox
        NOTE: The original size of the text box is 452 x 93.
        """
        super().__init__()

        # the "actual" dimensions of the textbox
        self.final_size = size

        # the dimensions of the textbox as it is shown on the screen;
        # the dimensions become bigger each frame to give a "transition effect"
        self.current_size = [0, 0]
        self.lines = lines

        # These variables are needed to give the RPG dialogue text "pop up" effect
        self.total_lines = len(self.lines)

        # the line and letter to render in a given frame; always starts at first line/letter
        self.current_line = 1
        self.current_letter = 1

        # set up the text box sprite/image
        self.file_loc = resource_path(os.path.join("Graphics", "text_box.png"))
        self.image = pygame.image.load(self.file_loc).convert()

        # make img transparent to black
        self.image.set_colorkey((0, 0, 0))

        self.top_left = ((CENTER_X - self.final_size[0] / 2),
                         (CENTER_Y - self.final_size[1] / 2) + 250)
        return

    def draw(self, screen, frames_since_shown, key_pressed=None):
        """
        Displays the textbox onto the screen.

        screen: the screen to draw text box on
        frames_since_shown: how many frames has it appeared on screen so far
        key_pressed: holds the key player pressed in current frame
        """

        """ --- THE TEXT BOX APPEARANCE TRANSITION --- """
        if frames_since_shown <= 30:
            # If textbox just popped up:
            # - reset current line and current letter to give RPG dialogue transition effect
            # - exit function early to avoid displaying textbox in its initial frames
            self.current_line = self.current_letter = 1
            return

        # The actual transition:
        elif frames_since_shown == 31:
            self.current_size = [int(self.final_size[0] / 3), int(self.final_size[1] / 3)]
        elif frames_since_shown == 32:
            self.current_size = [int(self.final_size[0] / 2.5), int(self.final_size[1] / 2.5)]
        elif frames_since_shown == 33:
            self.current_size = [int(self.final_size[0] / 2), int(self.final_size[1] / 2)]
        elif frames_since_shown == 34:
            self.current_size = [int(self.final_size[0] / 1.5), int(self.final_size[1] / 1.5)]
        elif frames_since_shown == 35:
            self.current_size = [self.final_size[0], self.final_size[1]]

        # self.image is the original img to transform;
        # self.current_image is the transformed img to be displayed on screen
        self.current_image = pygame.transform.scale(self.image,
                                                    (self.current_size[0], self.current_size[1]))

        # Display current image to the bottom center half of the screen
        screen.blit(self.current_image, ((CENTER_X - self.current_size[0] / 2),
                                         (CENTER_Y - self.current_size[1] / 2) + 250))

        # Display text on the textbox; we render one new line each frame so that each line
        # "pops up" like how they do in a typical RPG.
        if frames_since_shown > 35:
            font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)

            # coordinates of the top left corner of the first line of text
            top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                        CENTER_Y - (self.final_size[1] / 2) + 375]

            for i in range(0, self.current_line):
                if i >= len(self.lines):
                    # Double check if we just rendered the last line;
                    # if we did, leave loop, because there isn't a "next line" to get ready for
                    break

                if i == self.current_line - 1:
                    # slice string up to where current_letter is "referring to"
                    line_to_render = self.lines[i][0:self.current_letter - 1]
                else:
                    # render whole line
                    line_to_render = self.lines[i]

                text = font.render(line_to_render, True, (255, 255, 255, 255))
                screen.blit(text, dest=top_left)
                top_left[1] += 40

                # a new letter appears every 0.25 frames
                if frames_since_shown % 0.25 == 0:
                    # need >= to account for when self.current_letter is > than amount of lines
                    if self.current_letter >= len(self.lines[i]):
                        # If all letters have been printed for given line, get ready for next line
                        self.current_line += 1

                        # reset self.current_letter so that we can print first letter of next line
                        self.current_letter = 1
                    else:
                        # if not finished printing out whole line,
                        # get ready to print next letter in next frame
                        self.current_letter += 1

            close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))
            screen.blit(close_text, dest=(CENTER_X + 250, CENTER_Y + 290))


class Extension_TextBox(TextBox):
    """
    A special type of textbox that is never the first textbox to be shown. It is the
    textbook that is always drawn after the first textbox. Unlike the first textbox, which
    will always draw the textbox graph, this textbox will only render its text.
    """

    def draw(self, screen, frames_since_shown, key_pressed=None):
        """
        screen: the screen to draw text box on
        frames_since_shown: how many frames has it appeared on screen so far
        key_pressed: doesn't do anything in this function,
                     but needed as other text box classes use it
        """
        if frames_since_shown <= 10:
            # Reset current line and letter to give RPG dialogue transition effect
            self.current_line = self.current_letter = 1
            return

        # self.image -> original img to transform
        # self.current_image -> transformed image to be displayed
        self.current_image = pygame.transform.scale(self.image,
                                                    (self.final_size[0], self.final_size[1]))

        # display image at given coordinates
        screen.blit(self.current_image,
                    ((CENTER_X - self.final_size[0] / 2),
                     (CENTER_Y - self.final_size[1] / 2) + 250))

        # 'm5x7' font by Daniel Linssen
        font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)

        # Display what is intended to be displayed:
        # Render one new line each frame so that each
        # line "pops up" like how they do in a typical RPG.
        # Coordinates refer to top left corner of text box.
        top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                    CENTER_Y - (self.final_size[1] / 2) + 375]

        for i in range(0, self.current_line):
            if i >= len(self.lines):
                # We just rendered the last line
                break

            if i == self.current_line - 1:
                # slice string up to the current letter to be rendered
                line_to_render = self.lines[i][0:self.current_letter - 1]
            else:
                # render whole line
                line_to_render = self.lines[i]

            text = font.render(line_to_render, True, (255, 255, 255, 255))
            screen.blit(text, dest=top_left)

            # the next line of text will be under previous line of text
            top_left[1] += 40

            # A new letter appears every 1/4 frame
            if frames_since_shown % 0.25 == 0:
                if self.current_letter >= len(self.lines[i]):
                    # We already print out all letters in current line;
                    # Move to the next line
                    self.current_line += 1
                    self.current_letter = 1
                else:
                    # Get ready to print the next letter
                    self.current_letter += 1

        close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))
        screen.blit(close_text, dest=(CENTER_X + 250, CENTER_Y + 290))


class Choice_TextBox(TextBox):
    """
    A special textbox that allows the player to make a YES/NO style decision. A different
    predefined set of textboxes will appear depending on the choice the player makes.
    """

    def __init__(self, size=(452, 93), lines=[], choices=None):
        """
            Parameters:
                size: The size of the textbox, represented as a list/tuple. Default size
                      is 452 x 93.
                lines: The prompt the choice textbox will display, represented as a list of
                       string, with each string representing a line.
                choices: A list containing the two possible choices that the user can make.
                         Set to "None" by default, as the parent textbox class does not
                         have this functionality.

            Return:
                Does not return anything; just creates a new Choice Textbox object.
        """
        super().__init__(size, lines)

        if choices is None:
            # If none, use default choices
            self.choices = [">YES                     NO", "YES                     >NO"]
        else:
            self.choices = choices
        self.choice_to_blit = 0

    def draw(self, screen, frames_since_shown, key_pressed = None):
        """
            Parameters:
                screen: the screen object to draw the textbox on
                frames_since_shown: How many frames has the textbox appeared in the screen so far
                key_pressed: the key that was pressed by the user; "None" means that no
                             key has been pressed

            Returns:
                Has no return value. The function just draws the textbox onto the PyGame screen.
        """
        if frames_since_shown <= 10:
            # Reset current line and letter to display an RPG dialogue transition effect 
            self.current_line = self.current_letter = 1
            return

        # self.image: the original img to transform
        # self.current_image: the transformed img that will actually be displayed
        self.current_image = pygame.transform.scale(self.image,
                                                    (self.final_size[0], self.final_size[1]))
        screen.blit(self.current_image, ((CENTER_X - self.final_size[0] / 2),
                                         (CENTER_Y - self.final_size[1] / 2) + 250))

        font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)

        # coordinates of the top left corner of the first line of text
        top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                    CENTER_Y - (self.final_size[1] / 2) + 375]

        # Render one new line each frame so that each line 
        # "pops up" like how they do in a typical RPG.
        for i in range(0, self.current_line):
            if i >= len(self.lines):
                # If we rendered the last line, end the loop. 
                break

            if i == self.current_line - 1:
                # Slice the string up to index "current_letter"
                line_to_render = self.lines[i][0:self.current_letter - 1]
            else:
                # Render the whole line
                line_to_render = self.lines[i]

            text = font.render(line_to_render, True, (255, 255, 255, 255))
            screen.blit(text, dest=top_left)

            # The next line of text will only differ from previous line by only the vertical coord
            top_left[1] += 40
            if frames_since_shown % 0.25 == 0:
                if self.current_letter >= len(self.lines[i]):
                    # Get ready for the next line
                    self.current_line += 1
                    self.current_letter = 1
                else:
                    # Get ready to print the next letter
                    self.current_letter += 1

        if key_pressed == "a":
            # If "A" is pressed, move option to YES
            self.choice_to_blit -= 1
        elif key_pressed == "d":
            # if "D" is pressed, move option to NO
            self.choice_to_blit += 1

        # We mod the choice to blit variable so that it is never an index outside of self.choices
        self.choice_to_blit %= len(self.choices)
        choice = font.render(self.choices[self.choice_to_blit], True, (255, 255, 255, 255))
        screen.blit(choice, dest = top_left)

        close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))
        screen.blit(close_text, dest=(CENTER_X + 250, CENTER_Y + 290))

        # return info on what text box was render by giving text box index in choices list
        # this will allow us to know what the user picked (i.e. if they picked "YES or "NO")
        return self.choice_to_blit
