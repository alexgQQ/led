import time
import random
import numpy as np
import sys
import unittest
import pickle as pkl

from neopixel import Adafruit_NeoPixel, Color
from config import LED_MATRIX_CONFIG


if __name__ == '__main__':
    led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
    led.begin()
    buffer = led.getPixels()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        sys.exit()

    with open(filename, 'rb') as f:
        animation = pkl.load(f)
    fps = animation.get('fps', 60)
    frames = animation.get('frames')

    try:
        while True:
            for each in frames:
                buffer[:] = each
                led.show()
                time.sleep(1.0/fps)
    except KeyboardInterrupt:
        pass
    led.clear()
