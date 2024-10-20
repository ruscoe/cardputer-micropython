"""Fireworks.

Designed for the M5Stack Cardputer.

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
_GRAVITY = const(1)
_DRAG = const(1)

tft = Display()
config = Config()
kb = UserInput()

particles = []

def process_input():
    keys = kb.get_new_keys()

    if keys:
        # "G0" button exits to the launcher.
        if "G0" in keys:
            reset()

def spawn_firework(x, y):
    global particles

    for i in range(0, 10):
        particle = {
            "x": x,
            "y": y,
            "dx": randint(-5, 5),
            "dy": randint(-5, 5),
            "color": color565(randint(0, 255), randint(0, 255), randint(0, 255))
        }

        particles.append(particle)

def update_particles():
    global particles

    for particle in particles:
        particle["dy"] += _GRAVITY
        particle["dy"] -= _DRAG

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        if particle["y"] > _DISPLAY_HEIGHT:
            particles.remove(particle)

def draw_particles():
    global particles

    for particle in particles:
        tft.pixel(particle["x"], particle["y"], particle["color"])

def main_loop():

    spawn_firework((_DISPLAY_WIDTH // 2), (_DISPLAY_HEIGHT // 2))

    while True:
        tft.fill(config.palette[2])

        process_input()

        update_particles()

        draw_particles()

        tft.show()

        time.sleep_ms(_FRAME_INTERVAL)

main_loop()
