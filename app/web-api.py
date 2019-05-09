from flask import Flask, request, abort
import numpy as np
from neopixel import Adafruit_NeoPixel
from config import LED_MATRIX_CONFIG
from base import ColorRGB, ColorHSV


class LED:
    def __init__(self, *args, **kwargs):
        self._led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
        self._led.begin()

        self.width = 32
        self.height = 8
        self.shape = (self.width, self.height, 3)

        self.color_type = kwargs.get('color_type', 'RGB')
        self.color_class = ColorHSV if self.color_type == 'HSV' else ColorRGB

    def convert_colors(self, data):
        """ Converts color board to integers for led driver """
        def color(values):
            return self.color_class.color(*values)

        return np.apply_along_axis(color, 2, data)

    def set_leds(self, data):
        led_data = self.convert_colors(data)
        self._led._led_data[:] = led_data
        self._led.show()


led = LED()
app = Flask(__name__)


@app.route('/board', methods=['POST'])
def board():
    try:
        if request.method == 'POST':
            data = request.json.copy()
            array = np.array(data['data'])
            led.set_leds(array)
        return 'Ok'
    except Exception as error:
        app.logger.error(error)
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
