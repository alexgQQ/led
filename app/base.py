import numpy as np
import random
import colorsys
import time
from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


class ColorRGB:
    @classmethod
    def color(cls, red, green, blue):
        return cls.color_rgb(red, green, blue)

    @classmethod
    def color_rgb(cls, red, green, blue, white=0):
        """ Convert individual rgb colors to single integer """
        return (white << 24) | (green << 16)| (red << 8) | blue


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


class BaseCavas:
    def __init__(self):
        self.ticks = 0.0
        self.width = 32
        self.height = 8
        self.fps = 60.0
        # Dictionary mapping of pixel loctions and colors
        self.pixels = {}
        # List of shapes in the canvas
        self.shapes = []

    def render_frame(self):
        frame = np.zeros((self.width, self.height))
        for pixel, color in self.pixels.items():
            frame[pixel] = color
        return frame
    
    @property
    def now(self):
        return self.ticks/60.0

    def update(self):
        self.pixels = {}
        self.shapes_buffer = []
        time = self.now

        # Call update on each shape
        for shape in self.shapes:
            updates = shape.update(time)
            # Only take valid data, let shape handle deconstruction
            if updates:
                self.pixels.update(updates)
                self.handle_update(shape)
            else:
                self.handle_removal(shape)
        self.shapes = self.shapes_buffer
        # Add frame counter
        self.ticks += 1.0

    def handle_update(self, obj):
        self.shapes_buffer.append(obj)

    def handle_removal(self, obj):
        self.shapes_buffer.append(obj.__class__(self, start_time=self.now))


class BaseColorScheme:
    """
    Base class to control color generation.
    """
    def __init__(self, shape):
        self.shape = shape

    def update(self, _time, locations):
        if locations is None:
            return None
        return self.generator(_time, locations)

    def generator(self, _time, locations):
        """
        Override this method for new colors. 
        This method must return an iterable of colors, or False.
        """
        return [ColorRGB.color(50, 50, 50) for location in locations]


class BaseShape:
    """
    Base class to control shape generation.
    """
    def __init__(self, canvas, origin=None, start_time=0.0, color_scheme=BaseColorScheme):
        self.canvas = canvas
        # Origin location of shape
        self.origin = origin
        if origin is None:
            self.origin = (random.randint(0, self.canvas.width - 1),
                           random.randint(0, self.canvas.height - 1))
        # Duration of shape in seconds
        self.duration = 3.0
        # Current time of creation
        self.time_start = start_time
        self.color_scheme = color_scheme(self)

    def update(self, _time):
        # Normalize time for the shape
        _time = _time - self.time_start
        locations = self.generator(_time)
        # Updates over, remove from canvas
        if not locations:
            return False
        self.colors = self.color_scheme.update(_time, locations)
        return dict(zip(locations, self.colors))

    def generator(self, _time):
        """
        Override this method for new shapes. 
        This method must return an iterable of points as tuples, or False.
        """
        if _time > self.duration:
            return False
        return [self.origin]


class FrameRunner:
    def __init__(self, led, canvas):
        self.led = led
        self.led_data = led.getPixels()
        self.fps = 60.0
        self.canvas = canvas
    
    def run(self):
        try:
            while True:
                self.canvas.update()
                self.led_data[:] = self.canvas.render_frame()
                self.led.show()
                time.sleep(1.0/self.fps)
        except Exception as error:
            print('!! Caught exception, ', error)
        except:
            print('!! Uncaught exception !!')
        print('Exiting application...')
        self.led.clear()


class RainbowColorScheme(BaseColorScheme):
    def generator(self, _time, locations):
        hue = 0.5 * np.sin(2 * np.pi * 0.2 * _time) + 0.5
        return [ColorHSV.color(hue, 1.0, 0.7) for location in locations]


class MovingLineShape(BaseShape):
    def generator(self, _time):
        if _time > self.duration:
            return False
        N = np.around(5.0 * np.sin(2 * np.pi * 0.1 * _time) + 1.0)
        return [(self.origin[0] + n, self.origin[1]) for n in range(int(N))]


class Canvas(BaseCavas):
    def handle_removal(self, obj):
        self.shapes_buffer.append(MovingLineShape(
            self, start_time=self.now, color_scheme=RainbowColorScheme))


if __name__ == '__main__':
    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    print('Running animation...')
    canvas = BaseCavas()
    canvas.shapes = [BaseShape(canvas, color_scheme=BaseColorScheme) for _ in range(5)]
    runner = FrameRunner(led, canvas=canvas)
    runner.run()
