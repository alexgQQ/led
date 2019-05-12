from flask import Flask, request, abort
import numpy as np
import json

from ..base.base import LedMatrix

led = None
app = Flask(__name__)


@app.route('/board', methods=['POST'])
def board():
    try:
        if request.method == 'POST':
            data = json.loads(request.data.decode())
            array = np.array(data['data'])
            led.set_leds(array)
        return 'Ok'
    except Exception as error:
        app.logger.error(error)
        abort(400)

if __name__ == '__main__':
    led = LedMatrix()
    app.run(host='0.0.0.0')
