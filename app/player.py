import socket
import random
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def send():
    print('Sending...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        moves = ['right', 'left', 'none']
        move = random.choice(moves)
        s.connect((HOST, PORT))
        s.sendall(str.encode(move))
    time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    print('Starting client...')
    time.sleep(random.randint(1, 5))
    while True:
        send()

