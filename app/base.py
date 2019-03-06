import numpy as np
import random
import colorsys
import time
import traceback
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


class BaseCanvas:
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
                self.shapes_buffer.append(shape)
        self.shapes = self.shapes_buffer
        # Add frame counter
        self.ticks += 1.0


class BaseColorScheme:
    """
    Base class to control color generation.
    """
    def __init__(self, shape, **kwargs):
        self.shape = shape

    def update(self, _time, locations):
        if locations is None:
            return None
        return self.generator(_time, locations)

    def generator(self, _time, locations):
        """
        Override this method for new colors. 
        This method must return an iterable of colors.
        """
        return [ColorRGB.color(50, 50, 50) for location in locations]


class BaseShape:
    """
    Base class to control shape generation.
    """
    def __init__(self, canvas=None, duration=None, origin=None, start_time=0.0, color_scheme=BaseColorScheme, **kwargs):
        self.canvas = canvas
        # Origin location of shape
        self.origin = origin
        if origin is None:
            self.origin = (random.randint(0, self.canvas.width - 1),
                           random.randint(0, self.canvas.height - 1))
        # Duration of shape in seconds
        self.duration = duration or random.uniform(3.0, 4.0)
        # Current time of creation
        self.time_start = start_time
        self.color_class = color_scheme
        self.color_scheme = color_scheme(self)

    def on_exit(self):
        # Make a new obj of the same class
        t = self.time_start + self.duration
        new_shape = self.__class__(self.canvas,
                                   start_time=t,
                                   color_scheme=self.color_class)
        self.canvas.shapes_buffer.append(new_shape)

    def clean_points(self, data):
        new_data = []
        for point in data:
            valid = (abs(point[0]) < self.canvas.width
                    and abs(point[1]) < self.canvas.height)
            if valid:
                try:
                    point = (int(point[0]), int(point[1]))
                    new_data.append(point)
                except:
                    pass
        return new_data

    def update(self, _time):
        # Normalize time for the shape
        _time = _time - self.time_start
        locations = self.generator(_time)
        # Updates over, remove from canvas
        if not locations:
            self.on_exit()
            return False
        locations = self.clean_points(locations)
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
    def __init__(self, led, canvas, testing=False, debug=None):
        self.testing = testing
        if not testing:
            self.led = led
            self.led_data = led.getPixels()
        self.fps = 60.0
        self.canvas = canvas
        self.debug = debug

    def debugger(self):
        import pprint
        print('### Pixels ###')
        pprint.pprint(self.canvas.pixels)
        print('### Shapes ###')
        for each in self.canvas.shapes:
            pprint.pprint(each.__dict__)
    
    def run(self):
        try:
            while True:
                self.canvas.update()
                if self.debug:
                    self.debugger()
                data = self.canvas.render_frame()
                if not self.testing:
                    self.led_data[:] = data
                    self.led.show()
                time.sleep(1.0/self.fps)
        except Exception as error:
            traceback.print_exc()
            print('!! Caught exception, ', error)
        except:
            print('!! Uncaught exception !!')
        print('Exiting application...')
        if not self.testing:
            self.led.clear()


class RainbowColorScheme(BaseColorScheme):
    def generator(self, _time, locations):
        hue = 0.5 * np.sin(2 * np.pi * 0.2 * _time) + 0.5
        return [ColorHSV.color(hue, 1.0, 0.7) for location in locations]


class PulsingColorScheme(BaseColorScheme):
    def generator(self, _time, locations):
        if not hasattr(self, 'hue'):
            self.hue = random.uniform(0.0, 1.0)
        val = 0.5 * np.sin(2 * np.pi * 0.2 * _time) + 0.5
        return [ColorHSV.color(self.hue, val, 0.7) for location in locations]


class MovingLineShape(BaseShape):
    def generator(self, _time):
        if _time > self.duration:
            return False
        N = np.around(5.0 * np.sin(2 * np.pi * 0.1 * _time) + 1.0)
        return [(self.origin[0] + n, self.origin[1]) for n in range(int(N))]


class MovingPoint(BaseShape):
    def generator(self, _time):
        if not hasattr(self, 'speed'):
            self.speed = random.uniform(1.0, 5.0)
        new_pos = self.origin[0] + (self.speed * _time)
        if new_pos >= self.canvas.width:
            return False
        return [(new_pos, self.origin[1])]


class FlareShape(BaseShape):
    def generator(self, _time):
        if not hasattr(self, 'speed'):
            self.speed = random.uniform(1.0, 5.0)
        if not hasattr(self, 'sway_freq'):
            self.sway_freq = random.uniform(0.1, 0.7)
        sway = 2 * np.sin(2 * np.pi * self.sway_freq * _time)
        new_pos = self.origin[0] + (self.speed * _time)
        if new_pos >= self.canvas.width:
            return False
        return [(new_pos, self.origin[1] + sway)]


if __name__ == '__main__':
    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    print('Running animation...')
    canvas = BaseCanvas()
    canvas.shapes = [BaseShape(canvas, color_scheme=BaseColorScheme) for _ in range(4)]
    runner = FrameRunner(led, canvas=canvas, debug=False)
    runner.run()
