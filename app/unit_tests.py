import time
import random
import numpy as np
import sys
from neopixel import Adafruit_NeoPixel, Color
import unittest

LED_MATRIX_CONFIG = dict(
    num=(32, 8),        # Size of LED pixels.
    pin=18,             # GPIO pin connected to the pixels (18 uses PWM! 10 uses SPI /dev/spidev0.0).
    freq_hz=800000,     # LED signal frequency in hertz (usually 800khz)
    dma=10,             # DMA channel to use for generating signal (try 10)
    brightness=100,     # Set to 0 for darkest and 255 for brightest
    invert=False,       # True to invert the signal (when using NPN transistor level shift)
    channel=0,          # set to '1' for GPIOs 13, 19, 41, 45 or 53
)

class TestWrapper(unittest.TestCase):

    def setUp(self):
        self.led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self.led.begin()
        self.data = self.led.getPixels()
        self.test_data = np.random.randint(
            0, Color(255, 255, 255), self.led.size)

    def tearDown(self):
        self.led._cleanup()
        del self.led

    def test_single_index(self):
        x = random.randint(0, self.led.width - 1)
        y = random.randint(0, self.led.height - 1)
        value = self.test_data[x, y]
        self.data[x, y] = self.test_data[x, y]
        self.assertEqual(self.data[x, y], value)

    def test_full_slice(self):
        self.data[:] = self.test_data
        for data, test in zip(self.data[:], self.test_data):
            self.assertTrue(np.array_equal(data, test))


if __name__ == '__main__':
    unittest.main()
    # for x in range(leds.width):
    #     for y in range(leds.height):
    #         data = zeros
    #         data[x, y] = Color(30, 30, 30)
    #         leds.show()
    #         time.sleep(wait_ms/1000.0)
