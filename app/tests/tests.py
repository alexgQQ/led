import time
import random
import numpy as np
import sys
from neopixel import Adafruit_NeoPixel, Color
import unittest

from unittest.mock import patch

from .base import BaseCanvas, BaseColorScheme, FrameRunner, BaseShape, ColorHSV, ColorRGB
from .config import LED_MATRIX_CONFIG
from .physics import PhysicsCanvas, BouncyBalls


class TestPhysics(unittest.TestCase):

    def test_physics(self, led_mock):
        canvas = PhysicsCanvas()
        canvas.shapes = [canvas.create_shape() for _ in range(5)]
        canvas.update()


# class TestWrapper(unittest.TestCase):

#     def setUp(self):
#         self.led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
#         self.led.begin()
#         self.data = self.led.getPixels()
#         self.test_data = np.random.randint(
#             0, Color(255, 255, 255), self.led.size)

#     def tearDown(self):
#         self.led._cleanup()
#         del self.led

#     def test_single_index(self):
#         x = random.randint(0, self.led.width - 1)
#         y = random.randint(0, self.led.height - 1)
#         value = self.test_data[x, y]
#         self.data[x, y] = self.test_data[x, y]
#         self.assertEqual(self.data[x, y], value)

#     def test_full_slice(self):
#         self.data[:] = self.test_data
#         for data, test in zip(self.data[:], self.test_data):
#             self.assertTrue(np.array_equal(data, test))


class TestBaseShape(unittest.TestCase):

    def setUp(self):
        self.canvas = BaseCanvas()
        self.shape = BaseShape(canvas=self.canvas)

    def false(*args):
        return False

    def tearDown(self):
        del self.canvas

    @patch.object(BaseShape, 'generator', false)
    @patch('base.BaseShape.on_exit')
    def test_update_false(self, exit_mock):
        value = self.shape.update(0.0)
        self.assertTrue(exit_mock.called)
        self.assertFalse(value)

    def test_update(self):
        expected_value = {
            self.shape.origin: ColorRGB.color(50, 50, 50)
        }
        value = self.shape.update(0.0)
        self.assertDictEqual(value, expected_value)

    def test_clean_points(self):
        test_data = [
            (random.randint(0, self.canvas.width + 100),
                random.randint(0, self.canvas.height + 100))
            for _ in range(100)
                ]
        clean_points = self.shape.clean_points(test_data)
        for point in clean_points:
            x, y = point
            self.assertTrue(x < self.canvas.width)
            self.assertTrue(y < self.canvas.height)


class TestBaseCanvas(unittest.TestCase):

    def setUp(self):
        self.canvas = BaseCanvas()

    def tearDown(self):
        del self.canvas

    def test_pixels_no_shape(self):
        shapes = []
        expected_pixels = {}
        self.canvas.shapes = shapes
        self.canvas.update()
        self.assertDictEqual(self.canvas.pixels, expected_pixels)

    def test_pixels_single_shape(self):
        shapes = [BaseShape(canvas=self.canvas)]
        shape = shapes[0]
        expected_pixels = {
            shape.origin: ColorRGB.color(50, 50, 50),
        }
        self.canvas.shapes = shapes
        self.canvas.update()
        self.assertDictEqual(self.canvas.pixels, expected_pixels)

    def test_pixels_multiple_shapes(self):
        shapes = []
        expected_pixels = {}
        for x in range(32):
            for y in range(8):
                expected_pixels[(x, y)] = ColorRGB.color(50, 50, 50)
                shapes.append(BaseShape(
                    canvas=self.canvas, origin=(x, y)
                    ))
        self.canvas.shapes = shapes
        self.canvas.update()
        self.assertDictEqual(self.canvas.pixels, expected_pixels)

    def test_render_frame(self):
        shape = BaseShape(canvas=self.canvas)
        self.canvas.shapes = [shape]
        self.canvas.update()
        expected_frame = np.zeros((self.canvas.width, self.canvas.height))
        expected_frame[shape.origin] = ColorRGB.color(50, 50, 50)

        frame = self.canvas.render_frame()
        np.testing.assert_array_equal(frame, expected_frame)


if __name__ == '__main__':
    unittest.main()
