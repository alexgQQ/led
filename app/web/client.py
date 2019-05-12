import requests
import random
import time
import json
import numpy as np

class Client:
    def __init__(self):
        PROTOCOL = 'http://'
        HOST = '192.168.0.16'  
        PORT = 5000        
        ROUTE = '/board'
        self.URL = '{}{}:{}{}'.format(PROTOCOL, HOST, PORT, ROUTE)

    def serialize(self, data):
        return {field: val.tostring() for field, val in data.items()}

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
