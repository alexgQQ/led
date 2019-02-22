import numpy as np
import random
import colorsys
import time
import traceback
import cairo

from base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV
from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


if __name__ == '__main__':
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()
    led_data = led.getPixels()

    WIDTH, HEIGHT = 32, 8

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, HEIGHT)
    ctx.set_line_width(0.01)
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0, 0, 0, 1)
    pat.add_color_stop_rgba(0, 1, 1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source(pat)
    ctx.fill()
    buf = surface.get_data()
    data = np.ndarray(shape=(WIDTH, HEIGHT),
                      dtype=np.uint32,
                      buffer=buf)

    try:
        led_data[:] = data
        while True:
            pass
    except KeyboardInterrupt:
        pass
    led.clear()
