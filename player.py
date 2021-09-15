"""
This Python file houses the code for the Player class
and the tutorial NPC that guides the player on how to play the game.
"""
import pygame
from setup import resource_path
from random import randint
from spritesheet import get_frames
from text_box import *
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_SIZE = [10, 10]

CENTER_X = int(SCREEN_WIDTH / 2)
CENTER_Y = int(SCREEN_HEIGHT / 2)

# The factor to increase the size of each player HUD sprite by
SIZE_MULTIPLE = 5

# The furthest distance that sprites can be from the edge of the screen;
# prevents them from being drawn right at the end of the scren
OFFSET = 10

class Heart:
    """
    A class describing the behaviors and attributes for each heart
    icon displayed on the Player HUD.
    """
    def __init__(self):
        self.heart_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects", "heart.png"))).convert_alpha()
        self.x, self.y, self.width, self.height = self.heart_image.get_rect()
        self.width *= SIZE_MULTIPLE
        self.height *= SIZE_MULTIPLE
        self.heart_image = pygame.transform.scale(self.heart_image,
                           (self.width, self.height))

        # The explosion sprite will have the same dimensions are the heart sprite
        self.explosion_image = pygame.image.load(resource_path(
            os.path.join("Graphics", "Player Objects","explosion.png"))).convert_alpha()
        self.explosion_frames, self.num_expl_frames = get_frames(7, 10, 100, 100,
                                                                hanging_frames=4)

        # destroyed == True indiciates that the player lost one life and this heart
        # object corresponds to that lost life. In that case, we will play the explosion
        # sprite animation before deleting this heart.
        self.destroyed = False

        # Should the draw_hud() function in the Player class delete this heart object.
        # If self.pop == True, then yes; otherwise no.
        self.pop = False

        # This is the multiple to scale the dimensions of each sprite frame by.
        # I found that this multiple gives the best lookt & fit through experimentation
        self.expl_sprite_factor = 2

        # The actual explosion sprite does not begin at the left-corner of its sprite frame:
        # the sprite is right in the middle of the frame. The offset holds how much we need to 
        # move from the top-left corner of the sprite frame so that the top-left corner of the
        # actual sprite art is at (self.x, self.y).
        self.exp_offset_x = -80
        self.exp_offset_y = -75

        self.frames_since_shown = 0
        self.hover_direction = 1

        self.explosion_frames_since_shown = 0
        self.explosion_frame_num = 0

        # The offset from the actual y-value that heart sprite will 
        # temporaily take and change every few frames in order to give 
        # it a bouncing/hovering effect
        self.offset_from_real_y = 0

        return

    def draw(self, screen, position = None):
        """
        Wrapper function to determine whether or not we should
        draw the heart icon or the explosion of the heart (when the
        plaer loses a life)
        """
        if not self.destroyed:
            self.draw_alive(screen, position)
        else:
            self.draw_explosion(screen, position)

        return

    def draw_explosion(self, screen, position = None):
        """
        Draw the explosion of the heart icon before it is destroyed
        (after the player loses a life).
        """
        if position == None:
            position = (self.x, self.y)

        if self.explosion_frames_since_shown % 4 == 0:
            self.explosion_frame_num += 1

        # If we rendered all the frames of the explosion, then we
        # indicate that this heart object should be removed from player obj
        if self.explosion_frame_num > self.num_expl_frames - 1:
            self.pop = True
            return

        frame_image = self.explosion_image.subsurface(
            self.explosion_frames[self.explosion_frame_num])

        # Resize the explosion frame pixel art so that it big enough to be seen on screen
        _, _, exp_width, exp_height = frame_image.get_rect()
        frame_image = pygame.transform.scale(frame_image,
                      (exp_width * self.expl_sprite_factor, exp_height * self.expl_sprite_factor))

        screen.blit(frame_image,
                   (position[0] + self.exp_offset_x, position[1] + self.exp_offset_y))

        self.explosion_frames_since_shown += 1
        return

    def draw_alive(self, screen, position = None):
        """
        Draws the heart icon onto the screen.

        Parameters:
            The screen to draw on
            The (x, y) position as a tuple or list
        """
        if position == None:
            position = (self.x, self.y)

        # Change the direction and position every 13 frames (I found that doing so
        # gives the best effect)
        # so the heart displays a "hovering effect" similar to the asteroids
        if self.frames_since_shown % 13 == 0:
            self.hover_direction *= -1

            # How much the heart hovers will always be a random distance from its
            # actual/original y-value
            self.offset_from_real_y = self.y + (self.hover_direction * randint(1, 3))

        screen.blit(self.heart_image, (self.x, self.offset_from_real_y))
        return

    def increment_frames(self):
        self.frames_since_shown += 1
        return


class Player:

    def __init__(self):
        self.lives = 3
        self.max_lives = 7
        self.heart_icons = []
        for i in range(0, self.lives):
            self.heart_icons.append(Heart())

        # The HUD that shows the statistics of the player's spaceship.
        # Can be opened/closed by pressing the "T" key.
        self.stats_display = TextBox(lines = ["Stats Display TBD"])
        self.stats_display_frames = 0

        # Determine the position that each heart icon will be in:
        # They will all appear at the top left corner of the screen with
        # OFFSET spaces apart
        for i in range(0, self.lives):
            # The distance that top left coord of current heart needs to be in order 
            # to be right next to the previous heart icon 
            dist_from_prev_heart = self.heart_icons[i].width * i

            # The distance that the ith heart is from the first heart. Each heart
            # will be be OFFSET spaces away from each other.
            x_offset = OFFSET * (i + 1)

            (self.heart_icons[i].x,
             self.heart_icons[i].y) = (dist_from_prev_heart + x_offset, OFFSET)

        return

    def give_life(self):
        """
        Gives the player one extra life.
        """
        if self.lives > self.max_lives:
            return

        self.lives += 1
        new_life = Heart()

        # Find the position where the new heart should be in a similar fashion
        # to the for loop in the constructor
        next_available_heart_index = len(self.heart_icons)
        last_heart_index = next_available_heart_index - 1
        dist_from_prev_heart = self.heart_icons[last_heart_index].width \
                * next_available_heart_index
        x_offset = OFFSET * (next_available_heart_index + 1)

        (new_life.x, new_life.y) = (dist_from_prev_heart + x_offset, OFFSET)
        self.heart_icons.append(new_life)

        return

    def lose_life(self):
        """
        Takes away one life from the player. Labels the last heart icon as
        'destroyed', so that heart icon can play the explosion animation. After
        the heart icon explodes, the draw_hud() function will remove it from
        the list of heart_icons, essentially deleting it.
        """
        self.heart_icons[len(self.heart_icons) - 1].destroyed = True
        return

    def draw_hud(self, screen):
        """
        Draws the Player HUD onto the screen.

        Parameter(s):
            The screen in which to draw the HUD on
        """
        for heart in self.heart_icons:
            if heart.pop:
                self.heart_icons.remove(heart)
                self.lives -= 1
            else:
                heart.draw(screen)
        return

    def draw_stats(self, screen):
        """
        Draws the player stats display onto the screen.
        """
        self.stats_display.draw(screen, self.stats_display_frames)
        self.stats_display_frames += 1
        return

    def increment_frames(self):
        """
        Increment the number of frames that the player HUD has been displayed on screen.

        The Player object itself will not have a frame counter; rather the sprites that make
        up the player HUD will have frame counters, at they will be displayed on screen.
        """
        for heart in self.heart_icons:
            heart.increment_frames()
        return

