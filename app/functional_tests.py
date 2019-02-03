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

class TestLEDs(unittest.TestCase):

    def setUp(self):
        self.led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self.led.begin()
        self.data = self.led.getPixels()
        self.test_data = np.random.randint(
            0, Color(40, 40, 40), self.led.size)

    def tearDown(self):
        self.led._cleanup()
        del self.led

    def test_clear(self):
        expected = np.zeros((self.led.width, self.led.height))
        self.data[:] = self.test_data
        self.led.clear()
        self.assertTrue(np.array_equal(self.data[:], expected))

    def test_full_slice_show(self):
        self.data[:] = self.test_data
        self.led.show()

    def test_single_index_show(self, wait_ms=100):
        value = Color(40, 40, 40)
        for x in range(self.led.width):
            for y in range(self.led.height):
                self.data[x, y] = value
                self.led.show()
                time.sleep(wait_ms/1000.0)
                self.led.clear()

    def test_red(self, wait_ms=500):
        expected = np.full(self.led.size, Color(40, 0, 0))
        self.data[:] = expected
        self.led.show()
        time.sleep(wait_ms/1000.0)
        self.assertTrue(np.array_equal(self.data[:], expected))

    def test_green(self, wait_ms=500):
        expected = np.full(self.led.size, Color(0, 40, 0))
        self.data[:] = expected
        self.led.show()
        time.sleep(wait_ms/1000.0)
        self.assertTrue(np.array_equal(self.data[:], expected))

    def test_blue(self, wait_ms=500):
        expected = np.full(self.led.size, Color(0, 0, 40))
        self.data[:] = expected
        self.led.show()
        time.sleep(wait_ms/1000.0)
        self.assertTrue(np.array_equal(self.data[:], expected))


if __name__ == '__main__':
    unittest.main()
    # for x in range(leds.width):
    #     for y in range(leds.height):
    #         data = zeros
    #         data[x, y] = Color(30, 30, 30)
    #         leds.show()
    #         time.sleep(wait_ms/1000.0)
