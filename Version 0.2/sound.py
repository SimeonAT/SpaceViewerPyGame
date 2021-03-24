""" Manages the music playing capabilities for the video game. """
import pygame
import os
from random import randint
from setup import resource_path


""" A function that goes to each music folder, grabs all the file locations for each song. """
def fill_music_lists(file_location, music_list):
    """ @params: file_location -> location of folder with all the music songs
                 music_list -> list to put file locations in """
    for filename in os.listdir(file_location):
        if filename.endswith(".wav"):
            music_list.append(file_location + filename)

    # Make each file location in music_list compatible with PyInstaller
    for song in music_list:
        song = resource_path(song)

# Organize game music by function (main loop music, battle music, etc):
main_loop = []
fill_music_lists(os.path.join("Music"), main_loop)


def initialize_music():
    """ Initialize the music library. """
    pygame.mixer.init()

def play_music(music_list):
    """ Cycles through each song and loops back to playing each one
        after playing all of them.
        Got some help here: https://stackoverflow.com/questions/7746263/how-can-i-play-an-mp3-with-pygame """

    if not pygame.mixer.music.get_busy():  # if a song is not playing, play a random main loop song
        random_num = randint(0, len(music_list) - 1)
        pygame.mixer.music.load(resource_path(music_list[random_num]))
        pygame.mixer.music.play()
