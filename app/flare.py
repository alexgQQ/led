import time
import random
import numpy as np
import sys
import unittest
import colorsys
import pickle as pkl

from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


def color_rgb(red, green, blue, white=0):
    """ Convert individual rgb colors to single integer """
    return (white << 24) | (green << 16)| (red << 8) | blue

def hsv2rgb(h,s,v):
    return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h,s,v))

def color_hsv(hue, saturation, value):
    """ Convert individual hsv colors to single integer """
    return color_rgb(*hsv2rgb(hue, saturation, value))

hue_min = 0.0
hue_max = 1.0

time_start = time.time()

def calc_hues():
    t = time.time() - time_start
    hue_max = 0.5 * np.sin(2 * np.pi * 0.2 * t ) + 0.5
    hue_min = 0.4 * np.sin(2 * np.pi * 0.2 * t ) + 0.5


class Flare:
    def __init__(self):
        self.width = (0, 31)
        self.height = (0, 7)
        self.loc = (random.randint(*self.width), random.randint(*self.height))
        self.hue = random.uniform(hue_min, hue_max)
        self.sat = 1.0
        self.val = random.uniform(0.7, 1.0)
        self.fps = 60.0
        self.up_duration = random.uniform(0.5, 1.5)
        self.up_rate = self.val / (self.up_duration * self.fps)
        self.up = True
        self.down_duration = random.uniform(1.0, 3.0)
        self.down_rate = self.val / (self.down_duration * self.fps)
        self.buffer = 0.0

    def __call__(self):
        return self.update()

    def update(self):
        color = None
        if self.up:
            color = color_hsv(self.hue, self.sat, self.buffer)
            self.buffer += self.up_rate
            if self.buffer >= self.val:
                self.up = False
            return color
        elif self.val >= 0.0:
            color = color_hsv(self.hue, self.sat, self.val)
            self.val -= self.down_rate
        return color


def generate_frame(flares):
    frame = np.zeros((32, 8), dtype=int)
    for index, flare in enumerate(flares):
        color = flare()
        if color is None:
            flare = Flare()
            flares[index] = flare
            color = flare()
        frame[flare.loc] = int(color)
    return np.array(frame)

if __name__ == '__main__':
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()
    buffer = led.getPixels()

    if len(sys.argv) > 1:
        points = int(sys.argv[1])
    else:
        points = 15

    hue_max = 1.0
    hue_max = 0.9
    FLARES = [Flare() for _ in range(points)]

    try:
        while True:
            calc_hues()
            buffer[:] = generate_frame(FLARES)
            led.show()
            time.sleep(1.0/60.0)
    except:
        pass
    led.clear()
