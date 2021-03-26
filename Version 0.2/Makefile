# Makefiles aren't needed for Python program, but using make commands
# makes running the video game and formatting code easier.

all: game

game: main.py
	python3 main.py

# Got the formatting command from this link:
# https://leimao.github.io/blog/YAPF-Quick-Tutorial/
format:
	yapf --in-place --recursive $(wildcard *.py)

