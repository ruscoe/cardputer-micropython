"""Bounce.

Designed for the M5Stack Cardputer.

A ball bounces on the screen, changing direction and color when it hits the sides.

Author: Dan Ruscoe (danruscoe@protonmail.com)
Version: 1.0.0
"""

import time

from lib.display import Display
from lib.hydra.color import color565, hsv_to_rgb
from lib.hydra.config import Config
from lib.userinput import UserInput
from machine import reset
from random import randint

_DISPLAY_HEIGHT = const(135)
_DISPLAY_WIDTH = const(240)
_FRAME_INTERVAL = const(10)
_BALL_DIAMETER = const(12)
_BALL_SPEED = const(2)

tft = Display()
config = Config()
kb = UserInput()

ball_color = color565(randint(0, 255), randint(0, 255), randint(0, 255))
ball_x = (_DISPLAY_WIDTH // 2)
ball_y = (_DISPLAY_HEIGHT // 2)
ball_direction_x = 1
ball_direction_y = 1

def process_input():
    keys = kb.get_new_keys()

    if keys:
        # "G0" button exits to the launcher.
        if "G0" in keys:
            reset()

def update_ball_position():
    global ball_color
    global ball_x
    global ball_y
    global ball_direction_x
    global ball_direction_y

    ball_x += (ball_direction_x * _BALL_SPEED)
    ball_y += (ball_direction_y * _BALL_SPEED)

    if ((ball_x >= (_DISPLAY_WIDTH - _BALL_DIAMETER)) or (ball_x <= _BALL_DIAMETER)):
        ball_direction_x = (ball_direction_x * -1)
        ball_color = color565(randint(0, 255), randint(0, 255), randint(0, 255))

    if ((ball_y >= (_DISPLAY_HEIGHT - _BALL_DIAMETER)) or (ball_y <= _BALL_DIAMETER)):
        ball_direction_y = (ball_direction_y * -1)
        ball_color = color565(randint(0, 255), randint(0, 255), randint(0, 255))

def draw_ball():
    global ball_x
    global ball_y
    global ball_color

    tft.ellipse(ball_x, ball_y, _BALL_DIAMETER, _BALL_DIAMETER, ball_color, True)

def main_loop():
    while True:
        tft.fill(config.palette[2])

        process_input()
        update_ball_position()
        draw_ball()

        tft.show()

        time.sleep_ms(_FRAME_INTERVAL)

main_loop()
