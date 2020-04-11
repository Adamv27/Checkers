import math
import pygame
import DrawBoard as draw

pygame.init()
pygame.display.set_caption("Checkers")

#CONSTANTS
WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((600, 600))

class Game:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        self.player1 = Player('player1', 0, 'O')
        self.player2 = Player('player2', 0, 'X')
        self.player1, self.player2 = self.board.setupPieces(self.player1, self.player2)

    def play(self):
        self.refreshBoard()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            if self.turn % 2 == 0:
                newRow, newCol, delRow, delCol = self.player1.getMove(self.board, self.board.areas)
                self.board.board[newRow][newCol] = self.player1.symbol
                self.board.board[delRow][delCol] = ''
                draw.refreshTile(screen, self.board.board, delRow, delCol, self.player1.title)
                draw.refreshTile(screen, self.board.board, newRow, newCol, self.player1.title)
                self.turn += 1
                self.board.printBoard()
                print()
            else:
                newRow, newCol, delRow, delCol = self.player2.getMove(self.board, self.board.areas)
                self.board.board[newRow][newCol] = self.player2.symbol
                self.board.board[delRow][delCol] = ''
                draw.refreshTile(screen, self.board.board, delRow, delCol, self.player2.title)
                draw.refreshTile(screen, self.board.board, newRow, newCol, self.player2.title)
                self.turn += 1
                print()

    def refreshBoard(self):
        draw.drawBoard(screen, WIDTH, HEIGHT)
        draw.updateBoard(screen, WIDTH, HEIGHT, self.board)
        pygame.display.update()

class Board:
    def __init__(self):
        # creates list of 8x8 to represent game board
        self.board = self.createBoard()
        self.areas = self.getAreas()

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

    def getAreas(self):
        areas = []
        for row in range(8):
            for column in range(8):
                areas.append(pygame.Rect((row * 75), (column * 75), 75, 75))
        return areas

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
    def __init__(self, title, tiles, symbol):
        self.title = title
        self.tiles = tiles
        self.symbol = symbol
    def getMove(self, board, areas):
        clicks = 0
        selectedTile = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for area in areas:
                            if area.collidepoint(event.pos):
                                row = areas.index(area) % 8
                                column = math.floor(areas.index(area) / 8)
                                if clicks == 0:
                                    if board.board[row][column] == self.symbol:
                                        draw.drawHighlight(screen, row, column)
                                        pygame.display.update()
                                        selectedTile.append(row)
                                        selectedTile.append(column)
                                        clicks = 1
                                else:
                                    if row == selectedTile[0] and column == selectedTile[1]:
                                        clicks = 0
                                        selectedTile = []
                                        draw.refreshTile(screen, board.board, row, column, self.title)
                                        continue
                                    elif self.validMove(board, selectedTile, row, column):

                                        return row, column, selectedTile[0], selectedTile[1]
                                    else:
                                        print('not allowed')

    def validMove(self, board, selectedTile, row, column):
        print(selectedTile)
        print(row, column)
        if self.symbol == 'O':
            # Tile must move up a row and
            # one column to left or right
            # for white pieces
            if selectedTile[0] - row == 1:
                if abs(selectedTile[1] - column) == 1:
                    if board.board[row][column] not in ['X', 'O']:
                        return True
                else:
                    return False
            # If the player selected a tile two rows up
            # and two columns over check for a possible jump
            elif selectedTile[0] - row == 2:
                if selectedTile[1] - column == 2:
                    if board.board[selectedTile[0] - 1][selectedTile[1] - 1] == 'X':
                        return True
                elif selectedTile[1] - column == -2:
                    if board.board[selectedTile[0] - 1][selectedTile[1] + 1] == 'X':
                        return True

        elif self.symbol == 'X':
            if row - selectedTile[0] == 1:
                if abs(column - selectedTile[1]) == 1:
                    if board.board[row][column] not in ['X', 'O']:
                        return True
                else:
                    return False
            elif row - selectedTile[0] == 2:
                if column - selectedTile[1] == 2:
                    if board.board[selectedTile[0] + 1][selectedTile[1] + 1] == 'O':
                        return True
                elif column - selectedTile[1] == -2:
                    if board.board[selectedTile[0] + 1][selectedTile[1] - 1] == 'O':
                        return True
        return False

gameBoard = Board()
game = Game(gameBoard, 0)
game.play()
