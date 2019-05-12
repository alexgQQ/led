import numpy as np
import colorsys

from neopixel import Adafruit_NeoPixel, Color
from .config import LED_MATRIX_CONFIG


class ColorRGB:
    @classmethod
    def color(cls, red, green, blue):
        return cls.color_rgb(red, green, blue)

    @classmethod
    def color_rgb(cls, red, green, blue, white=0):
        """ Convert individual rgb colors to single integer """
        return int((white << 24) | (green << 16)| (red << 8) | blue)


class ColorHSV(ColorRGB):
    @classmethod
    def color(cls, hue, saturation, value):
        return cls.color_hsv(hue, saturation, value)

    @classmethod
    def hsv2rgb(cls, h, s, v):
        return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h,s,v))

    @classmethod
    def color_hsv(cls, hue, saturation, value):
        """ Convert individual hsv colors to single integer """
        return cls.color_rgb(*cls.hsv2rgb(hue, saturation, value))


class AbstractColorEncoder:
    COLOR_CLASS = None

    @classmethod
    def encode(cls, data):
        def color(values):
            return cls.COLOR_CLASS.color(*values)

        return np.apply_along_axis(color, 2, data)


class RGBColorEncoder(AbstractColorEncoder):
    COLOR_CLASS = ColorRGB


class HSVColorEncoder(AbstractColorEncoder):
    COLOR_CLASS = ColorHSV


class LedMatrix:
    def __init__(self, *args, **kwargs):
        self._led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self.color_encoder = kwargs.get('color_encoder', RGBColorEncoder)
        self._led.begin()
        self.width=32
        self.height=8

    def set_leds(self, data):
        led_data = self.color_encoder.encode(data)
        self._led._led_data[:] = led_data
        self._led.show()

    def clear_leds(self):
        self._led.clear()
