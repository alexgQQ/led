import time
import random
import numpy as np
import argparse
import pymunk

from base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV, RainbowColorScheme
from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


class SimSpace(object):
    """
    Simple class to represent pymunk usage with an LED Canvas.
    """

    def __init__(self):
        self.width = 320.0
        self.height = 80.0
        self.space = pymunk.Space()

        # Invert gravity to work with led positions, can be switched
        self.space.gravity = (0.0, 900.0)
        self._dt = 1.0 / 60.0
        self.objects = []
        self.add_boundaries()

    def step(self):
        """
        Increment the simulation time.
        """
        self.space.step(self._dt)

    def add_boundaries(self):
        """
        Add static lines to enclose the canvas space.
        """
        static_body = self.space.static_body
        self.boundaries = {
            'bottom': pymunk.Segment(
                static_body, (0.0, 0.0), (self.width, 0.0), 0.0),
            'left': pymunk.Segment(
                static_body, (0.0, 0.0), (0.0, self.height), 0.0),
            'top': pymunk.Segment(
                static_body, (self.width, self.height), (0.0, self.height), 0.0),
            'right': pymunk.Segment(
                static_body, (self.width, self.height), (self.width, 0.0), 0.0),
        }
        for key, line in self.boundaries.items():
            line.elasticity = 0.95
            line.friction = 0.9
            self.space.add(line)


class BouncyBall(BaseShape):
    """
    LED shape representation of a pymunk physics object
    """

    def __init__(self, space, **kwargs):
        super().__init__(**kwargs)

        # Pymunk physics setup
        self.space = space
        body_position = (n * 10.0 for n in self.origin)
        mass = 5
        radius = 5
        friction = 0.9
        elasticity = 0.95
        inertia = pymunk.moment_for_circle(
            mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = body_position
        self.shape = pymunk.Circle(
            self.body, radius, (0, 0))
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.space.add(self.body)

    def __del__(self):
        """
        Remove object from simulation when the shape is removed
        """
        # self.space.remove(self.shape, self.shape.body)

    def on_exit(self):
        """
        Create new bouncy ball if one is removed.
        """
        self.canvas.create_shape()

    def apply_force(self):
        """
        Applies random force to the body in the physics simulation
        """
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
        x, y = self.position
        out_of_bounds = (x < 0.0 or x > 31.0 or y < 0.0 or y > 7.0)
        if out_of_bounds:
            return False
        return [self.position]


class PhysicsCanvas(BaseCanvas):

    def __init__(self):
        super().__init__()
        self.sim_space = SimSpace()
        self.space = self.sim_space.space

    def random_position(self):
        return (random.randint(0, self.width - 1),
            random.randint(0, self.height - 1))

    def create_shape(self, position=None):
        if not position:
            position = self.random_position()

        x, y = position
        ball = BouncyBall(self.space, origin=(x, y), canvas=self)
        self.shapes.append(ball)
        return ball

    def update(self):
        super().update()
        self.sim_space.step()


def main(*args, **kwargs):

    parser = argparse.ArgumentParser(description='Number of bouncy balls to generate')
    parser.add_argument('-n', action="store", dest="n", type=int, const=1, nargs='?', default=1)
    parser.add_argument('--fake', action='store_false')
    results = parser.parse_args()
    num_of_lights = results.n
    no_led = results.fake

    canvas = PhysicsCanvas()
    [canvas.create_shape() for _ in range(num_of_lights)]

    print('Starting Adafruit LED driver...')
    led=False
    if no_led:
        led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        led.begin()

    print('Running animation...')
    testing = not no_led
    runner = FrameRunner(led, canvas=canvas, testing=testing, debug=False)
    runner.run()


if __name__ == '__main__':
    main()
