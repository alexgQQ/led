import time
import random
import numpy as np
import argparse
import pymunk

from base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV, RainbowColorScheme
from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


class BouncyBalls(object):
    def __init__(self):
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Points that exist in the world
        self._balls = []
    
    def _step(self):
        self._space.step(self._dt)

    def _encode(self):
        points = []
        for ball in self._balls:
            x, y = ball._body.position.int_tuple
            x /= 10
            y /= 10
            points.append((int(x), int(y)))
        return points

    def _add_static_scenery(self):
        width = 320.0
        height = 80.0
        static_body = self._space.static_body
        static_lines = [pymunk.Segment(static_body, (0.0, 0.0), (width, 0.0), 0.0),
                        pymunk.Segment(static_body, (0.0, 0.0), (0.0, height), 0.0),
                        pymunk.Segment(static_body, (width, height), (0.0, height), 0.0),
                        pymunk.Segment(static_body, (width, height), (width, 0.0), 0.0),]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(static_lines)

    def _create_ball(self, position=None):
        mass = 3
        radius = 5
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 160, 70
        if position:
            body.position = position
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)
        return shape


class Canvas(BaseCanvas):
    def __init__(self, space):
        super().__init__()
        self.space = space

    def clean_shapes(self):
        shapes = []
        for shape in self.shapes:
            body = shape.body.body.position.int_tuple
            out_of_bounds = (body < (0.0, 0.0) or body > (80.0, 320.0))
            if out_of_bounds:
                self.space.remove(shape.body, shape.body.body)
                shapes.append(Shape(canvas=self, start_time=self.now, color_scheme=RainbowColorScheme))
            else:
                shapes.append(shape)
        self.shapes = shapes
                

    def update(self):
        super().update()
        self.space._step()
        self.clean_shapes()


class Shape(BaseShape):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        x, y = self.origin
        pos = (x * 10.0, y * 10.0)
        self.body = self.canvas.space._create_ball(position=pos)
        self.apply_force()

    def on_exit(self):
        pass

    def apply_force(self):
        self.body.body.apply_impulse_at_world_point(
            (random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)),
             (random.uniform(0.0, 320.0), random.uniform(0.0, 80.0)))

    def generator(self, _time):
        if self.body.body.velocity.length < 30.0:
            self.apply_force()
        x, y = self.body._body.position.int_tuple
        x /= 10
        y /= 10
        return [(int(x), int(y))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Config options for flare light application')

    parser.add_argument('-n', action="store", dest="n", type=int, const=1, nargs='?', default=1)
    results = parser.parse_args()

    num_of_lights = results.n

    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    sim = BouncyBalls()

    print('Running animation...')
    canvas = Canvas(sim)
    canvas.shapes = [Shape(canvas=canvas, color_scheme=RainbowColorScheme)
                     for _ in range(num_of_lights)]
    runner = FrameRunner(led, canvas=canvas, debug=False)
    runner.run()
