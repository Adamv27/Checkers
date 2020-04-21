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
        self.board.setupPieces(self.player1, self.player2)

    def play(self):
        self.refreshBoard()
        self.board.printBoard()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            if self.turn % 2 == 0:
                self.player1.getMove(self.board, self.board.areas)
                pygame.display.update()
                self.board.printBoard()
                self.turn += 1
                print()
            else:
                self.player2.getMove(self.board, self.board.areas)
                pygame.display.update()
                self.turn += 1
                self.board.printBoard()
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
        self.board[0][4] = 'X'
        self.board[7][3] = 'O'

        return

    def getAreas(self):
        areas = []
        for row in range(8):
            for column in range(8):
                areas.append(pygame.Rect((row * 75), (column * 75), 75, 75))
        return areas

    def playMove(self, row, column, tileRow, tileColumn, symbol):
        self.board[row][column] = symbol
        self.board[tileRow][tileColumn] = ''
        draw.refreshTile(screen, self.board, row, column)
        draw.refreshTile(screen, self.board, tileRow, tileColumn)
        return self.board

    def jump(self, row, column):
        self.board[row][column] = ''
        draw.refreshTile(screen, self.board, row, column)
        return self.board

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
        self.king = symbol + 'K'
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
                                    if board.board[row][column] in [self.symbol, self.king]:
                                        draw.drawHighlight(screen, row, column)
                                        pygame.display.update()
                                        selectedTile.append(row)
                                        selectedTile.append(column)
                                        clicks = 1
                                else:
                                    if row == selectedTile[0] and column == selectedTile[1]:
                                        clicks = 0
                                        selectedTile = []
                                        draw.refreshTile(screen, board.board, row, column)
                                        continue
                                    else:
                                        currentMove = Move(board.board, row, column, selectedTile[0], selectedTile[1], board.board[selectedTile[0]][selectedTile[1]])
                                        if currentMove.isValid:
                                            symbol = board.board[selectedTile[0]][selectedTile[1]]
                                            if currentMove.isKingMove:
                                                if symbol == 'X':
                                                    symbol = 'XK'
                                                elif symbol == 'O':
                                                    symbol = 'OK'

                                            print('valid')

                                            if currentMove.isJump:
                                                print('jump')
                                                board.playMove(row, column, selectedTile[0], selectedTile[1], symbol)
                                                board.jump(currentMove.jumpCords[0], currentMove.jumpCords[1])
                                            else:
                                                board.playMove(row, column, selectedTile[0], selectedTile[1], symbol)
                                            return
                                        else:
                                            #if currentMove.validMultiJump:
                                                #print('valid')
                                            #else:
                                                print('not valid')

class Move(object):
    def __init__(self, board, row, column, tileRow, tileColumn, symbol):
        self.board = board
        self.row = row
        self.column = column
        self.tileRow = tileRow
        self.tileColumn = tileColumn
        self.symbol = symbol
        self.isJump = False
        self.jumpCords = []
        self.isValid = self.validMove(self.row, self.column, self.tileRow, self.tileColumn, self.symbol, self.board)
        self.isKingMove = self.isKing()

    def validMove(self, row, column, tileRow, tileColumn, symbol, board):
        print(row, column)
        print()
        print(tileRow, tileColumn)
        if symbol in ['X', 'O', 'XK', 'OK']:
            if tileRow - row == 1:
                if symbol == 'X':
                    return False
                if abs(tileColumn - column) == 1:
                    if board[row][column] == '':
                        return True
            elif tileRow - row == -1:
                if symbol == 'O':
                    return False
                if abs(tileColumn - column) == 1:
                    if board[row][column] == '':
                        return True
            else:
                if self.validJump(row, column, tileRow, tileColumn, symbol, board):
                    self.isJump = True
                    return True
        return False

    def validJump(self, row, column, tileRow, tileColumn, symbol, board):
        if symbol in ['X', 'XK']:
            opposites = ['O', 'OK']
        else:
            opposites = ['X', 'XK']

        if tileRow - row == 2:
            if symbol == 'X':
                return False
            if tileColumn - column == 2:
                if board[tileRow - 1][tileColumn - 1] in opposites:
                    self.jumpCords.append(self.tileRow - 1)
                    self.jumpCords.append(self.tileColumn - 1)
                    return True
            elif tileColumn - column == -2:
                if board[tileRow - 1][tileColumn + 1] in opposites:
                    self.jumpCords.append(self.tileRow - 1)
                    self.jumpCords.append(self.tileColumn + 1)
                    return True
        elif tileRow - row == -2:
            if symbol == 'O':
                return False
            if tileColumn - column == 2:
                if board[tileRow + 1][tileColumn - 1] in opposites:
                    self.jumpCords.append(self.tileRow + 1)
                    self.jumpCords.append(self.tileColumn - 1)
                    return True
            elif tileColumn - column == -2:
                print('test')
                if board[tileRow + 1][tileColumn + 1] in opposites:
                    self.jumpCords.append(self.tileRow + 1)
                    self.jumpCords.append(self.tileColumn + 1)
                    return True
        return False

    def isKing(self):
        if self.symbol == 'O' and self.row == 0:
            return True
        elif self.symbol == 'X' and self.row == 7:
            return True

gameBoard = Board()
game = Game(gameBoard, 0)
game.play()
