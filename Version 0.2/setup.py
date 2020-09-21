""" The code that I need in order for PyInstaller to work will go here.
    Got some help here:
    - https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe"""
import sys
import os

""" I need this resource_path so that my file location code (whenever I try to upload a sprite into the game)
    will not mess up PyInstaller. """
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

