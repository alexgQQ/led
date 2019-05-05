from flask import Flask, request, abort
from flask.json import jsonify
import numpy as np
from neopixel import Adafruit_NeoPixel
from config import LED_MATRIX_CONFIG
from base import ColorRGB, ColorHSV


class LED:
    def __init__(self, *args, **kwargs):
        self._led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self._led.begin()

        self.color_type = kwargs.get('color_type', 'RGB')
        self.color_class = ColorHSV if self.color_type == 'HSV' else ColorRGB
        self.width = 32
        self.height = 8
        value = np.empty((), dtype=object)
        value[()] = (0, 0, 0)
        self.board = np.full((self.width, self.height), value, dtype=object)

    def convert_board(self):
        """ Converts color board to integers for led driver """
        def color(values):
            return self.color_class.color(*values)

        self._led._led_data[:] = np.apply_along_axis(color, 2, self.board).astype('int')
        self._led.show()

    def data(self):
        return dict(
            array=self.board.tolist()
        )

    def meta(self):
        return dict(
            color_type=self.color_type,
        )

led = LED()
app = Flask(__name__)

@app.route('/board', methods=['GET', 'POST'])
def board():
    try:
        if request.method == 'POST':
            led.board = np.array(request.json.get('array'))
            led.convert_board()
        return jsonify(led.to_dict())
    except Exception:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
