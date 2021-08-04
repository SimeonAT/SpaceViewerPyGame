""" Manages the music playing capabilities for the video game. """
import pygame
import os
from random import randint
from setup import resource_path


def fill_music_lists(file_location, music_list):
    """
    Goes into each music folder, and grabs all of the file locations for each song.
    - file_location -> location of folder with all of the songs
    - music_list -> list to put file locations in
    """
    for filename in os.listdir(file_location):
        if filename.endswith(".wav"):
            music_list.append(file_location + "/" + filename)

    # Make each file location in music_list compatible with PyInstaller
    for song in music_list:
        song = resource_path(song)


# Organize game music by function (main loop music, battle music, etc):
main_loop = []
fill_music_lists(os.path.join("Music"), main_loop)


def initialize_music():
    """ Initializes the music library. """
    pygame.mixer.init()


def play_music(music_list):
    """
    Plays a random song.
    Got help here: https://stackoverflow.com/questions/7746263/how-can-i-play-an-mp3-with-pygame
    """
    if not pygame.mixer.music.get_busy():
        random_num = randint(0, len(music_list) - 1)
        pygame.mixer.music.load(resource_path(music_list[random_num]))
        pygame.mixer.music.play()
