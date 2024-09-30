"""Pet Fish.

Designed for the M5Stack Cardputer.

A fish swims across the screen.

Press "P" to enter play mode and the fish will swim through a hoop.
Press "ESC" to return to default mode.
Press "G0" to exit.

Author: Dan Ruscoe (danruscoe@protonmail.com)
Version: 1.0.0
"""

import time

from lib.display import Display
from lib.hydra.config import Config
from lib.userinput import UserInput
from machine import reset

_DISPLAY_HEIGHT = const(135)
_DISPLAY_WIDTH = const(240)

_FISH_WIDTH = const(25)
_FISH_HEIGHT = const(12)
_FISH_TAIL_LENGTH = const(10)
_FISH_EYE_SIZE = const(2)
_FISH_SPEED = const(1)
_FISH_HOOP_DIAMETER = const(40)

tft = Display()
config = Config()
kb = UserInput()

fish_direction = 1
fish_x = _DISPLAY_WIDTH // 2
fish_y = _DISPLAY_HEIGHT // 2
play_mode = False

def process_input():
    global play_mode

    keys = kb.get_new_keys()

    if keys:
        # "G0" button exits to the launcher.
        if "G0" in keys:
            reset()
        # Esc with or without Fn key to exit all modes.
        if "ESC" in keys or "`" in keys:
            play_mode = False
        # P to enter play mode.
        if "p" in keys:
            play_mode = True

def draw_fish():
    global fish_x
    global fish_y
    global play_mode

    # Draw the fish's body.
    tft.ellipse(fish_x, fish_y, _FISH_WIDTH, _FISH_HEIGHT, config.palette[8], True)
    # Draw the fish's eye.
    tft.ellipse((fish_x + ((_FISH_WIDTH - 10) * fish_direction)), fish_y, _FISH_EYE_SIZE, _FISH_EYE_SIZE, config.palette[0], True)
    # Draw the fish's tail.
    for i in range(0, _FISH_TAIL_LENGTH):
        tft.line(((fish_x - (_FISH_WIDTH * fish_direction)) - (i * fish_direction)), (fish_y + i), ((fish_x - (_FISH_WIDTH * fish_direction )) - (i * fish_direction)), (fish_y - i), config.palette[8])

    if (play_mode == True):
        draw_hoop()

def draw_hoop():
    tft.ellipse(_DISPLAY_WIDTH // 2, _DISPLAY_HEIGHT // 2, _FISH_HOOP_DIAMETER, _FISH_HOOP_DIAMETER, config.palette[8], False)

def move_fish():
    global fish_direction
    global fish_x
    global fish_y

    # Move fish forwards (relative to the fish's direction).
    fish_x += (_FISH_SPEED * fish_direction)

    # Reverse the fish's direction if it reaches the edge of the screen.
    if ((fish_direction == 1) & (fish_x >= _DISPLAY_WIDTH)):
        fish_direction = -1
    elif ((fish_direction == -1) & (fish_x <= 0)):
        fish_direction = 1

def main_loop():
    while True:
        tft.fill(config.palette[2])

        process_input()
        move_fish()
        draw_fish()

        tft.show()

        time.sleep_ms(10)

main_loop()
