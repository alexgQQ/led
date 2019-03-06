import time
import random
import numpy as np
import argparse
import pymunk

from app.base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV, RainbowColorScheme
from neopixel import Adafruit_NeoPixel, Color
from app.config import LED_MATRIX_CONFIG


class SimSpace(object):

    def __init__(self):
        self.width = 320.0
        self.height = 80.0
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)
        self._dt = 1.0 / 60.0
        self.objects = []
        self.boundary = Boundary(self, self.width, self.height)

    def step(self):
        self._space.step(self._dt)

    def remove_shapes(self):
        for shape in self._space.shapes:
            position = shape.body.position 
            out_of_bounds = (position < (-20.0, -20.0) or position > (340.0, 100.0))
            if out_of_bounds:
                self._space.remove(shape, shape.body)


class Boundary(object):

    def __init__(self, space, width, height):
        self.space = space._space
        static_body = self.space.static_body
        self.static_lines = [
            pymunk.Segment(
                static_body, (0.0, 0.0), (width, 0.0), 0.0),
            pymunk.Segment(
                static_body, (0.0, 0.0), (0.0, height), 0.0),
            pymunk.Segment(
                static_body, (width, height), (0.0, height), 0.0),
            pymunk.Segment(
                static_body, (width, height), (width, 0.0), 0.0),
            ]
        for line in self.static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self.space.add(self.static_lines)


class BouncyBall(object):

    def __init__(self, space, position):
        self.space = space
        self.mass = 5
        self.radius = 5
        self.friction = 0.9
        self.elasticity = 0.95
        inertia = pymunk.moment_for_circle(
            self.mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = position
        self.shape = pymunk.Circle(
            self.body, self.radius, (0, 0))
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.space.add(self.body)


class Canvas(BaseCanvas):

    def __init__(self, space):
        super().__init__()
        self.space = space
        self._space = space._space

    def remove_shapes(self):
        shapes = []
        for shape in self.shapes:
            position = shape.position 
            out_of_bounds = (position < (-20.0, -20.0) or position > (340.0, 100.0))
            if out_of_bounds:
                self._space.remove(shape.shape, shape.shape.body)
                shape = self.create_shape(position=self.random_position)
            shapes.append(shape)
        self.shapes = shapes

    def random_position(self):
        return (random.randint(0, self.width - 1),
            random.randint(0, self.height - 1))

    def create_shape(self, position=None):
        if not position:
            position = self.random_position()

        x, y = position
        ball = BouncyBall(self._space, (x * 10.0, y * 10.0))
        return Shape(ball, canvas=self, origin=position, color_scheme=RainbowColorScheme)

    def update(self):
        super().update()
        self.space.step()
        self.remove_shapes()


class Shape(BaseShape):
    def __init__(self, ball, **kwargs):
        super().__init__(**kwargs)
        self.shape = ball.shape
        self.body = ball.body
        self.apply_force()

    def on_exit(self):
        pass

    def apply_force(self):
        self.body.apply_impulse_at_world_point(
            (random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)),
             (random.uniform(0.0, 320.0), random.uniform(0.0, 80.0)))

    @property
    def position(self):
        x, y = self.shape._body.position.int_tuple
        x /= 10
        y /= 10
        return (int(x), int(y))

    def generator(self, _time):
        return [self.position]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Config options for flare light application')

    parser.add_argument('-n', action="store", dest="n", type=int, const=1, nargs='?', default=1)
    results = parser.parse_args()

    num_of_lights = results.n

    print('Starting Adafruit LED driver...')
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()

    sim = SimSpace()

    print('Running animation...')
    canvas = Canvas(sim)
    canvas.shapes = [canvas.create_shape() for _ in range(num_of_lights)]
    runner = FrameRunner(led, canvas=canvas, debug=False)
    runner.run()
