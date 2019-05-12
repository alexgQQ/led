import time
import random
import numpy as np
import argparse

from canvas import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV
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
    parser = argparse.ArgumentParser(description='Config options for flare light application')

    parser.add_argument('-n', action="store", dest="n", type=int, const=1, nargs='?', default=1)
    results = parser.parse_args()

    num_of_lights = results.n

    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    print('Running animation...')
    canvas = BaseCanvas()
    canvas.shapes = [BaseShape(canvas, color_scheme=FlareColorScheme) for _ in range(num_of_lights)]
    runner = FrameRunner(led, canvas=canvas, debug=False)
    runner.run()
