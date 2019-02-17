import time
import random
import numpy as np
import sys
import colorsys

from base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV
from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


class FlareColorScheme(BaseColorScheme):
    def generator(self, _time, locations):
        if not hasattr(self, 'hue'):
            hue_max = 0.5 * np.sin(2 * np.pi * 0.5 * self.shape.time_start ) + 0.5
            hue_min = 0.4 * np.sin(2 * np.pi * 0.5 * self.shape.time_start ) + 0.5
            self.hue = random.uniform(hue_min, hue_max)
        if not hasattr(self, 'pulse_freq'):
            duration = self.shape.duration * 2.0
            self.pulse_freq = 1.0/duration
        val = 0.9 * np.sin(2 * np.pi * self.pulse_freq * _time)
        return [ColorHSV.color(self.hue, 1.0, val) for location in locations]


if __name__ == '__main__':
    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    print('Running animation...')
    canvas = BaseCanvas()
    canvas.shapes = [BaseShape(canvas, color_scheme=FlareColorScheme) for _ in range(4)]
    runner = FrameRunner(led, canvas=canvas, debug=False)
    runner.run()
