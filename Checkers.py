import pygame
import DrawBoard as draw

pygame.init()
pygame.display.set_caption("Checkers")

#CONSTANTS
WIDTH = 600
HEIGHT = 600

# COLORS
DARK_TEAL = (0, 104, 107)
LIGHT_TEAL = (0, 191, 196)

LIGHT_BROWN = (255,222,173)

screen = pygame.display.set_mode((600, 600))

class Game:
    def __init__(self, board):
        self.board = board
        self.player1 = Player(0)
        self.player2 = Player(0)
        self.player1, self.player2 = self.board.setupPieces(self.player1, self.player2)
        print(self.player2.tiles)
        print(self.player1.tiles)
    def play(self):
        screen.fill((LIGHT_BROWN))
        draw.drawBoard(screen, WIDTH, HEIGHT)
        pygame.display.update()

        self.board.printBoard()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            draw.updateBoard(screen, WIDTH, HEIGHT, self.board)
            pygame.display.update()

class Board:
    def __init__(self):
        # creates list of 8x8 to represent game board
        self.board = self.createBoard()
    def createBoard(self):
        board = []
        for row in range(8):
            row = []
            for j in range(8):
                row.append('')
            board.append(row)
        return board

    def setupPieces(self, player1, player2):
        board = self.board

        # set up red pieces (player2)
        for rowIndex, row in enumerate(self.board):
            for columnIndex, column in enumerate(row):
                if (rowIndex == 0 or rowIndex == 2) and player2.tiles <= 12:
                    if columnIndex % 2 == 0:
                        self.board[rowIndex][columnIndex] = 'X'
                        player2.tiles += 1
                elif rowIndex == 1:
                    if columnIndex % 2 != 0:
                        self.board[rowIndex][columnIndex] = 'X'
                        player2.tiles += 1

        # set up white pieces (player1)

        for rowIndex, row in enumerate(reversed(self.board)):
            for columnIndex, column in enumerate(reversed(row)):
                if rowIndex == len(self.board) - 1 or rowIndex == len(self.board) - 3:
                    if player2.tiles <= 12:
                        if columnIndex % 2 != 0:
                            self.board[rowIndex][columnIndex] = 'O'
                            player1.tiles += 1
                elif rowIndex == len(self.board) - 2:
                    if columnIndex % 2 == 0:
                        self.board[rowIndex][columnIndex] = 'O'
                        player1.tiles += 1
        return player1, player2




    def printBoard(self):
        for row in self.board:
            for index, space in enumerate(row):
                if index != 0:
                    print(f'{space} | ', end='')
                elif index == 0:
                    print(f'| {space} | ', end='')
            print()
            print('-' * 25)

class Player:
    def __init__(self, tiles):
        self.tiles = tiles

gameBoard = Board()
game = Game(gameBoard)
game.play()
