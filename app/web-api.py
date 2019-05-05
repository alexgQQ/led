from flask import Flask, request
from flask.json import jsonify
import numpy as np
from neopixel import Adafruit_NeoPixel
from config import LED_MATRIX_CONFIG
from base import ColorRGB


class LED:
    def __init__(self):
        self._led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self._led.begin()

        self.width = 32
        self.height = 8
        value = np.empty((), dtype=object)
        value[()] = (0, 0, 0)
        self.board = np.full((self.width, self.height), value, dtype=object)

    def convert_board(self):
        func = np.vectorize(ColorRGB.color)
        self._led._led_data[:] = func(self.board).astype('int')

    def to_dict(self):
        return dict(
            array=self.board.tolist()
        )

led = LED()
app = Flask(__name__)

@app.route('/board', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        led.board = np.array(request.json.get('array'))
        led.convert_board()
        return jsonify(led.to_dict())
    else:
        return jsonify(led.to_dict())

if __name__ == '__main__':
    app.run()