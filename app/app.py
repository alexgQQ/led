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

    # canvas = np.zeros((led.width+6, led.height))
    # canvas[0:3, 3] = np.full((3,), Color(50, 0, 0))

    # for _ in range(canvas.shape[0]):
    #     buffer[:] = canvas[3:35, :]
    #     led.show()
    #     time.sleep(100.0/1000.0)
    #     canvas = np.roll(canvas, (1, 0), axis=(0, 1))

    # if len(sys.argv) > 1:
    #     filename = sys.argv[1]
    # else:
    #     sys.exit()

    # with open(filename, 'rb') as f:
    #     frames = pkl.load(f)

    # try:
    #     while True:
    #         for each in frames:
    #             buffer[:] = each
    #             led.show()
    #             time.sleep(100.0/1000.0)
    # except KeyboardInterrupt:
    #     pass
    # led.clear()

    frames = []
    arr = np.zeros((led.width, led.height))
    for red in range(255):
        for green in range(255):
            for blue in range(255):
                arr[8:25, 2:5] = Color(red, green, blue)
                frames.append(arr)

    try:
        while True:
            for each in frames:
                buffer[:] = each
                led.show()
                time.sleep(100.0/1000.0)
    except KeyboardInterrupt:
        pass
    led.clear()
