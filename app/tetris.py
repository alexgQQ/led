import numpy
import random
import pygame
import socket
import sys
import errno
from time import sleep

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class Pieces():

    allPieces = numpy.array([[[0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 1, 1, 0],
                              [0, 0, 1, 0]],
                             [[0, 0, 0, 0],
                              [0, 0, 2, 0],
                              [0, 2, 2, 0],
                              [0, 2, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 3, 0, 0],
                              [0, 3, 0, 0],
                              [0, 3, 3, 0]],
                             [[0, 0, 0, 0],
                              [0, 0, 4, 0],
                              [0, 0, 4, 0],
                              [0, 4, 4, 0]],
                             [[0, 0, 5, 0],
                              [0, 0, 5, 0],
                              [0, 0, 5, 0],
                              [0, 0, 5, 0]],
                             [[0, 0, 0, 0],
                              [0, 6, 6, 0],
                              [0, 6, 6, 0],
                              [0, 0, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 7, 7, 7],
                              [0, 0, 7, 0],
                              [0, 0, 0, 0]]])
    names = ['-', 'S', 'Z', 'L', 'J', 'I', 'O', 'T']
    # colors for the pieces
    # (black, green, magenta, orange, red, yellow, blue, cyan)
    colors = [(40,247,54), (253,76,252), (253,146,38), (252,42,28),
        (254,249,55), (16,63,251), (44,252,254)]

    def GetNewPiece():
        pieceNumber = random.randint(1, 7)
        return Piece(Pieces.names[pieceNumber], Pieces.allPieces[pieceNumber], Pieces.colors[pieceNumber])

    GetNewPiece = staticmethod(GetNewPiece)

class Piece():
    x = 0
    y = 0

    def __init__(self, pieceName, pieceShape, pieceColor):
        self.name = pieceName
        self.shape = pieceShape
        self.color = pieceColor

    # set the position of the piece
    def SetPosition(self, x, y):
        self.x = x
        self.y = y

    # move the piece one row down
    def MoveDown(self):
        self.y += 1

    # move the piece one column left
    def MoveLeft(self):
        self.x -= 1

    # move the piece one column right
    def MoveRight(self):
        self.x += 1

    # rotate the piece left (not implemented yet)
    def RotateLeft(self):
        self.shape = numpy.rot90(self.shape, 3)

    # rotate the piece right (not implemented yet)
    def RotateRight(self):
        self.shape = numpy.rot90(self.shape)


class Tetris():

    pointsPerRows = [10, 30, 100, 400]
    speedIncrease = 50
    cPiece = None
    cSpeed = 600

    def __init__(self, board_height, board_width):
        self.BOARD_HEIGHT = board_height
        self.BOARD_WIDTH = board_width
        self.board = numpy.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH), numpy.int8)

    # called when a new game is started
    def NewGame(self):
        self.board.fill(0) # clear board
        self.points = 0 # reset points
        self.linesRemoved = 0 # counts how often lines removed not the lines itself
        self.level = 1
        self.cPiece = Pieces.GetNewPiece() # generate current piece
        self.cPiece.SetPosition(self.BOARD_WIDTH // 2 - 2, -5) # new piece start above the board
        self.nPiece = Pieces.GetNewPiece() # generate nex piece

    def MoveDown(self):
        if self.MoveDownPossible():
            self.cPiece.MoveDown() # move current piece one row down
        else:
            if self.CheckGameOver():
                return False
            self.CopyPieceToBoard()
            self.CheckFullLines()
            if self.linesRemoved > 10:
                self.cSpeed -= self.speedIncrease
                self.level += 1
                self.linesRemoved = 0
            self.cPiece = self.nPiece
            self.cPiece.SetPosition(self.BOARD_WIDTH // 2 - 2, -5) # new piece start above the board
            self.nPiece = Pieces.GetNewPiece() # generate next piece
        return True

    def MoveLeft(self):
        if self.MoveLeftPossible():
            self.cPiece.MoveLeft()

    def MoveRight(self):
        if self.MoveRightPossible():
            self.cPiece.MoveRight()

    def CheckGameOver(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            if value != 0 and self.cPiece.y + y < 0:
                    return True
        return False

    def MoveDownPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x
            ty = self.cPiece.y + 1
            if value != 0 and ty + y >= 0:
                if ty + y >= self.BOARD_HEIGHT or self.board[ty +y, tx + x] != 0:
                    return False
        return True

    def MoveLeftPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x - 1
            ty = self.cPiece.y
            if value != 0 and ty + y >= 0:
                if tx + x < 0 or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def MoveRightPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x + 1
            ty = self.cPiece.y
            if value != 0 and tx + x >= 0 and ty + y >= 0:
                if tx + x >= self.BOARD_WIDTH or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def RotatePieceRightPossible(self):
        return self.RotatePiecePossible(numpy.rot90(self.cPiece.shape))

    def RotatePieceLeftPossible(self):
        return self.RotatePiecePossible(numpy.rot90(self.cPiece.shape, 3))

    def RotatePiecePossible(self, shape):
        for (y, x), value in numpy.ndenumerate(shape):
            tx = self.cPiece.x
            ty = self.cPiece.y
            if value != 0 and ty + y >= 0:
                if ty + y >= self.BOARD_HEIGHT or tx + x < 0 or tx + x >= self.BOARD_WIDTH or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def RotatePiece(self):
        if self.RotatePieceRightPossible():
            self.cPiece.RotateRight()
        elif self.RotatePieceLeftPossible():
            self.cPiece.RotateLeft()

    def CopyPieceToBoard(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            if value != 0:
                self.board[self.cPiece.y + y, self.cPiece.x + x] = value

    def CheckFullLines(self):
        removedLinesCount = numpy.count_nonzero(numpy.all(self.board != 0, 1))
        if removedLinesCount != 0:
            removedLines = self.board[numpy.all(self.board != 0, 1)]
            removedLines.fill(0)
            cleanBoard= self.board[numpy.any(self.board == 0, 1)]
            self.board = numpy.vstack((removedLines, cleanBoard))
            self.points += self.pointsPerRows[removedLinesCount - 1]
            self.linesRemoved += 1


# class TetrisApp(object):
#     def __init__(self):
#         pygame.init()
#         pygame.key.set_repeat(250,25)
#         self.init_led()
#         self.width = 8
#         self.height = 32
#         self.delay = 750
#         self.fps = 30
#         self.tetris = Tetris(self.height, self.width)
#         self.frame = self.tetris.board
        
#         pygame.event.set_blocked(pygame.MOUSEMOTION)

#     def init_led(self):
#         self.led = Adafruit_NeoPixel(**LED_MATRIX_CONFIG)
#         self.led.begin()
#         self.led_buffer = self.led.getPixels()

#     def show_led(self):
#         self.led_buffer[:] = self.frame.astype('int')
#         self.led.show()

#     def gather_frame(self):
#         # Process where the current piece is in the frame
#         self.frame = numpy.copy(self.tetris.board)
#         if self.tetris.cPiece is not None:
#             for (y, x), value in numpy.ndenumerate(self.tetris.cPiece.shape):
#                 if value != 0:
#                     if (y + self.tetris.cPiece.y) > -1:
#                         loc = (y + self.tetris.cPiece.y,x + self.tetris.cPiece.x)
#                         self.frame[loc] = ColorRGB.color(*self.tetris.cPiece.color)

#         self.show_led()
#         # print(self.frame)

#     def handle_move(self):
#         """ Handle string command as a move """
#         moves = ['left', 'right', 'none']
#         cmd = random.choice(moves)
#         if cmd == 'left':
#             self.tetris.MoveLeft()
#         elif cmd == 'right':
#             self.tetris.MoveRight()

#     def run(self):
#         """ Main function to run aplication """
#         #  NOTE: Wierd bug where the std output stream is blocked until client data is processed 
#         #        Ex: using a print statement on pygame event will not print on event
#         #            it will print when client data is received

#         self.tetris.NewGame()

#         #  Set pygame timer to trigger consistent events
#         pygame.time.set_timer(pygame.USEREVENT+1, self.delay)
#         pygame.time.set_timer(pygame.USEREVENT+2, random.randint(500, 2000))
#         dont_burn_my_cpu = pygame.time.Clock()

#         #  Start hosting basic TCP connection for client bot player
#         # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         #     s.bind((HOST, PORT))
#         #     s.listen()

#         while True:
#             #  Check for pygame events and process them by type
#             for event in pygame.event.get():
#                 if event.type == pygame.USEREVENT+1:
#                     if not self.tetris.MoveDown():
#                         self.tetris.NewGame()
#                     self.gather_frame()
#                 elif event.type == pygame.USEREVENT+2:
#                     self.handle_move()
#                     self.gather_frame()
#                     pygame.time.set_timer(pygame.USEREVENT+2, 0)
#                     pygame.time.set_timer(pygame.USEREVENT+2, random.randint(500, 2000))

#             #  Continue timer events
#             dont_burn_my_cpu.tick(self.fps)

#                 # #  Look for client connections but unblock the operation
#                 # client, info = s.accept()
#                 # client.setblocking(0)

#                 # #  Try to process data if it is there or report conneciton errors
#                 # with client:
#                 #     try:
#                 #         msg = client.recv(100)
#                 #         if len(msg):
#                 #             self.handle_move(msg)
#                 #     except socket.error as e:
#                 #         err = e.args[0]
#                 #         if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
#                 #             print('No data available')
#                 #             continue
#                 #         else:
#                 #             # a "real" error occurred
#                 #             print(e)
#                 #             sys.exit(1)


# if __name__ == '__main__':
#     App = TetrisApp()
#     App.run()
