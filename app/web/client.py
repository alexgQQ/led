import requests
import random
import time
import json
import numpy as np
from ..base.config import CLIENT_CONFIG

class Client:
    def __init__(self):
        self.__dict__.update(CLIENT_CONFIG)
        self.URL = '{}{}:{}{}'.format(
            self.PROTOCOL, self.HOST, self.PORT, self.ROUTE)

    def serialize(self, data):
        payload = {}
        payload['data'] = data.tolist()
        return payload

    def post(self, data):
        """ Write color data as rgb or hsv """
        try:
            payload = self.serialize(data)
            response = requests.post(self.URL, json=payload)
            if response.status_code != 200:
                return False
        except Exception as error:
            print(error)
            return False

        return True


if __name__ == '__main__':

    client = Client()

    for _ in range(5):
        time.sleep(1)
        data = np.random.randint(0, high=256, size=(32, 8, 3))
        response = client.post(data)

    data = np.zeros((32, 8, 3), dtype=int)
    response = client.post(data)
