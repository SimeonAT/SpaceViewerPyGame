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
        self.final_size = size  # the actual size of text box
        self.current_size = [0, 0]  # the size of the tex box on screen (0 x 0 so that text box can 'transition' by enlarging itself)
        self.lines = lines

        # These variables are needed to give the RPG dialogue text "pop up" effect
        self.total_lines = len(self.lines)
        self.current_line = 1               # which new line to render up to for a given frame; always starts at first line
        self.current_letter = 1             # which letter to render up to for a given frame; always starts at first letter of first line

        # set up the text box sprite/image
        self.file_loc = resource_path(os.path.join("Graphics", "text_box.png"))
        self.image = pygame.image.load(self.file_loc).convert()  # load up text box sprite from file location
        self.image.set_colorkey((0, 0, 0))  # make img transparent to black

        # The coordinates for the top left corner of the textbox
        self.top_left = ( (CENTER_X - self.final_size[0] / 2),
                                  (CENTER_Y -  self.final_size[1] / 2) + 250 )


    """ Method to display textbox onto screen """
    def draw(self, screen, frames_since_shown, key_pressed = None):
        """@params -> screen: the screen to draw text box on
                      frames_since_shown: how many frames has it appeared on screen so far
                       key_pressed: doesn't do anything in this function, but needed as some text boxes use key_pressed """
        """ --- THE TEXT BOX APPEARANCE TRANSITION --- """
        if frames_since_shown <= 30:
            # Reset self.current_line and self.current_letter to give RPG dialogue transition effect
            self.current_line = self.current_letter = 1
            return   # don't transition if the object just popped up

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

        # self.image is the original img to transform; self.current_image is the transformed img to be displayed on screen
        self.current_image = pygame.transform.scale(self.image, (self.current_size[0], self.current_size[1]))
        screen.blit(self.current_image, ( (CENTER_X - self.current_size[0] / 2),
                                  (CENTER_Y -  self.current_size[1] / 2) + 250 ))  # display image at given coordinates

        # Display text on the textbox
        if frames_since_shown > 35:
            font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)  # Upload the m5x7 font by Daniel Linssen

            """ Display what is intended to be displayed:
                Render one new line each frame so that each line "pops up" like how they do in a typical RPG. """
            top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                        CENTER_Y - (self.final_size[1] / 2) + 375]  # coordinates of the top left corner of the first line of text

            for i in range(0, self.current_line):
                if i >= len(self.lines):
                    # Double check if we just rendered the last line,
                    # if we do, leave loop and don't get ready for next line (because there isn't a next line to get ready for)
                    break

                if i == self.current_line - 1:
                    line_to_render = self.lines[i][0:self.current_letter - 1]   # slice string up to where current_letter is "referring to"
                else:
                    line_to_render = self.lines[i]  # render whole line

                text = font.render(line_to_render, True, (255, 255, 255, 255))
                screen.blit(text, dest=top_left)
                top_left[1] += 40  # the next line of text will be under the previous line of text
                if frames_since_shown % 0.25 == 0:   # a new letter appears every 0.25 frames
                    if self.current_letter >= len(self.lines[i]):  # need >= to account for when self.current_letter is > than amount of lines
                        # If we already printed out all letters for given line, get ready for next line
                        self.current_line += 1
                        self.current_letter = 1   # reset self.current_letter so that we can print first letter of next line
                    else:
                        # if not finished printing out whole line, get ready to print next letter in next frame
                        self.current_letter += 1


            close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))  # Textbox Call-To-Action
            screen.blit(close_text, dest = (CENTER_X + 250, CENTER_Y + 290))


class Extension_TextBox(TextBox):
    """ This inheritance of textbox is the classes for text boxes that follow after the first textbox, and thus their
        text, but not their textbox, needs to be redrawn. """

    def draw(self, screen, frames_since_shown, key_pressed = None):
        """@params -> screen: the screen to draw text box on
                      frames_since_shown: how many frames has it appeared on screen so far
                      key_pressed: doesn't do anything in this function, but needed as some text boxes use key_pressed """
        if frames_since_shown <= 10:
            # Reset self.current_line and self.current_letter to give RPG dialogue transition effect
            self.current_line = self.current_letter = 1
            return

        # self.image is the original img to transform; self.current_image is the transformed img to be displayed on screen
        self.current_image = pygame.transform.scale(self.image, (self.final_size[0], self.final_size[1]))
        screen.blit(self.current_image, ( (CENTER_X - self.final_size[0] / 2),
                                  (CENTER_Y -  self.final_size[1] / 2) + 250))  # display image at given coordinates

        # Display text on the textbox
        font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)  # Upload the m5x7 font by Daniel Linssen

        """ Display what is intended to be displayed:
            Render one new line each frame so that each line "pops up" like how they do in a typical RPG. """
        top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                    CENTER_Y - (self.final_size[1] / 2) + 375]  # coordinates of the top left corner of the first line of text

        for i in range(0, self.current_line):
            if i >= len(self.lines):
                # Double check if we just rendered the last line,
                # if we do, leave loop and don't get ready for next line (because there isn't a next line to get ready for)
                break

            if i == self.current_line - 1:
                line_to_render = self.lines[i][0:self.current_letter - 1]   # slice string up to where current_letter is "referring to"
            else:
                line_to_render = self.lines[i]  # render whole line

            text = font.render(line_to_render, True, (255, 255, 255, 255))
            screen.blit(text, dest=top_left)
            top_left[1] += 40  # the next line of text will be under the previous line of text
            if frames_since_shown % 0.25 == 0:   # a new letter appears every 0.25 frames
                if self.current_letter >= len(self.lines[i]):  # need >= to account for when self.current_letter is > than amount of lines
                    # If we already printed out all letters for given line, get ready for next line
                    self.current_line += 1
                    self.current_letter = 1   # reset self.current_letter so that we can print first letter of next line
                else:
                    # if not finished printing out whole line, get ready to print next letter in next frame
                    self.current_letter += 1


        close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))  # Textbox Call-To-Action
        screen.blit(close_text, dest = (CENTER_X + 250, CENTER_Y + 290))


class Choice_TextBox(TextBox):
    """ This type of textbox allows the user to make YES/NO choices using the WASD keys. """

    def __init__(self, size = (452, 93), lines = [], choices = None):
        """ @paramaters: 'choices' -> a list that contains all of the possible strings that the user will see when
                                      using WASD or Arrow Keys to select options. """
        super().__init__(size, lines)   # do everything in the regular TextBox constructor first

        if choices == None:
            # If none, use default choices
            self.choices = [">YES                     NO", "YES                     >NO"]    # The possible choices of the textbox
        else:
            self.choices = choices
        self.choice_to_blit = 0  # which text to render; corresponds to index in choices list

    def draw(self, screen, frames_since_shown, key_pressed = None):
        """@params -> screen: the screen to draw text box on
                      frames_since_shown: how many frames has it appeared on screen so far
                      key_pressed: the key that was pressed by user input; 'None' means no key was pressed  """
        if frames_since_shown <= 10:
            # Reset self.current_line and self.current_letter to give RPG dialogue transition effect
            self.current_line = self.current_letter = 1
            return

        # self.image is the original img to transform; self.current_image is the transformed img to be displayed on screen
        self.current_image = pygame.transform.scale(self.image, (self.final_size[0], self.final_size[1]))
        screen.blit(self.current_image, ((CENTER_X - self.final_size[0] / 2),
                                         (CENTER_Y - self.final_size[1] / 2) + 250))  # display image at given coordinates

        # Display text on the textbox
        font = pygame.font.Font(resource_path(os.path.join("Graphics", "m5x7.ttf")), 40)  # Upload the m5x7 font by Daniel Linssen

        """ Display what is intended to be displayed:
            Render one new line each frame so that each line "pops up" like how they do in a typical RPG. """
        top_left = [CENTER_X - (self.final_size[0] / 2) + 100,
                    CENTER_Y - (self.final_size[1] / 2) + 375]  # coordinates of the top left corner of the first line of text

        for i in range(0, self.current_line):
            if i >= len(self.lines):
                # Double check if we just rendered the last line,
                # if we do, leave loop and don't get ready for next line (because there isn't a next line to get ready for)
                break

            if i == self.current_line - 1:
                line_to_render = self.lines[i][0:self.current_letter - 1]  # slice string up to where current_letter is "referring to"
            else:
                line_to_render = self.lines[i]  # render whole line

            text = font.render(line_to_render, True, (255, 255, 255, 255))
            screen.blit(text, dest=top_left)
            top_left[1] += 40  # the next line of text will be under the previous line of text
            if frames_since_shown % 0.25 == 0:  # a new letter appears every 0.25 frames
                if self.current_letter >= len(
                        self.lines[i]):  # need >= to account for when self.current_letter is > than amount of lines
                    # If we already printed out all letters for given line, get ready for next line
                    self.current_line += 1
                    self.current_letter = 1  # reset self.current_letter so that we can print first letter of next line
                else:
                    # if not finished printing out whole line, get ready to print next letter in next frame
                    self.current_letter += 1

        """ Determine which choice to render """
        if key_pressed == "a":
            # If "A" is pressed, move option to YES
            self.choice_to_blit -= 1
        elif key_pressed == "d":
            # if "D" is pressed, move option to NO
            self.choice_to_blit += 1

        self.choice_to_blit %= len(self.choices)  # We % it so that the choice_to_blit will always be an index in self.choices
        choice = font.render(self.choices[self.choice_to_blit], True, (255, 255, 255, 255))   # display the choice onto the screen
        screen.blit(choice, dest = top_left)

        close_text = font.render("Press ENTER to continue.", True, (255, 255, 255, 255))  # Textbox Call-To-Action
        screen.blit(close_text, dest=(CENTER_X + 250, CENTER_Y + 290))

        return self.choice_to_blit     # return info on what text box was render by giving text box index in choices list
                                       # this will allow us to know what the user picked (i.e. if they picked "YES or "NO")
