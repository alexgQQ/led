import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from ..base.base import (
    ColorRGB,
    ColorHSV,
    RGBColorEncoder,
    HSVColorEncoder,
    LedMatrix,
)
from ..web.web_api import app


class TestColorClasses(unittest.TestCase):

    def test_color_rgb(self):
        test_data = np.random.randint(0, high=256, size=(3,))
        result = ColorRGB.color(*test_data)
        self.assertIsInstance(result, int)

    def test_color_hsv(self):
        test_data = np.random.rand(3)
        result = ColorHSV.color(*test_data)
        self.assertIsInstance(result, int)


class TestColorEncoders(unittest.TestCase):

    def test_color_rgb(self):
        test_data = np.random.randint(0, high=256, size=(32, 8, 3))
        result = RGBColorEncoder.encode(test_data)
        self.assertEqual(result.shape, (32, 8))

    def test_color_hsv(self):
        test_data = np.random.rand(32, 8, 3)
        result = HSVColorEncoder.encode(test_data)
        self.assertEqual(result.shape, (32, 8))


class TestLedMatrix(unittest.TestCase):

    @patch('app.base.base.Adafruit_NeoPixel.begin')
    def test_led_matrix(self, begin_mock):
        led = LedMatrix()
        self.assertIsInstance(led, LedMatrix)
        self.assertIs(led.color_encoder, RGBColorEncoder)


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.web.web_api.led')
    def test_board_post(self, led_mock):
        led_mock.set_leds.return_value = True
        payload = np.random.randint(0, high=256, size=(32, 8, 3)).tolist()
        response = self.app.post('/board', json=dict(data=payload))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
