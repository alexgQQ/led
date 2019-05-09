import random
import time
import pygame
import numpy

from client import Client
from tetris import Tetris


class TetrisApp(object):
    def __init__(self):
        pygame.display.init()
        pygame.key.set_repeat(250,25)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.width = 8
        self.height = 32
        self.delay = 750
        self.fps = 30
        self.tetris = Tetris(self.height, self.width)
        self.frame = self.pframe = numpy.repeat(self.tetris.board, 3).reshape((self.height, self.width, 3))
        self.client = Client()

    def gather_frame(self):
        # Process where the current piece is in the frame
        self.frame = numpy.copy(self.pframe)
        if self.tetris.cPiece is not None:
            for (y, x), value in numpy.ndenumerate(self.tetris.cPiece.shape):
                if value != 0:
                    if (y + self.tetris.cPiece.y) > -1:
                        loc = (y + self.tetris.cPiece.y,x + self.tetris.cPiece.x)
                        self.frame[loc] = self.tetris.cPiece.color
        self.pframe = self.frame

    def handle_move(self):
        """ Handle string command as a move """
        moves = ['left', 'right', 'none']
        cmd = random.choice(moves)
        if cmd == 'left':
            self.tetris.MoveLeft()
        elif cmd == 'right':
            self.tetris.MoveRight()

    def update(self):
        self.gather_frame()
        data = self.client.post(self.frame)

    def run(self):
        """ Main function to run aplication """
        #  NOTE: Wierd bug where the std output stream is blocked until client data is processed 
        #        Ex: using a print statement on pygame event will not print on event
        #            it will print when client data is received

        self.tetris.NewGame()

        #  Set pygame timer to trigger consistent events
        pygame.time.set_timer(pygame.USEREVENT+1, self.delay)
        pygame.time.set_timer(pygame.USEREVENT+2, random.randint(500, 2000))
        dont_burn_my_cpu = pygame.time.Clock()

        while True:
            #  Check for pygame events and process them by type
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    if not self.tetris.MoveDown():
                        self.tetris.NewGame()
                    self.update()
                elif event.type == pygame.USEREVENT+2:
                    self.handle_move()
                    self.update()
                    pygame.time.set_timer(pygame.USEREVENT+2, 0)
                    pygame.time.set_timer(pygame.USEREVENT+2, random.randint(500, 2000))

            #  Continue timer events
            dont_burn_my_cpu.tick(self.fps)

if __name__ == '__main__':
    print('Starting player...')
    app = TetrisApp()

    try:
        app.run()
    except Exception as error:
        print(error)
