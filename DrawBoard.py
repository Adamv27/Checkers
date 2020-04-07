import pygame

def drawBoard(WINDOW, WIDTH, HEIGHT):
    for count, column in enumerate(range(9)):
        pygame.draw.line(WINDOW, (0,0,0), (count * 75, 0), (count * 75, HEIGHT))

    for count, row in enumerate(range(9)):
        pygame.draw.line(WINDOW, (0,0,0), (0, count * 75), (WIDTH, count * 75))

def updateBoard(WINDOW, WIDTH, HEIGHT, board):
    for chipRow, row in enumerate(board.board):
        for chipColumn, space in enumerate(row):
            if space != '':
                if space == 'X':
                    drawChip(WINDOW, chipColumn, chipRow,  'player1')
                else:
                    drawChip(WINDOW, chipColumn, chipRow, 'player2')


def drawChip(WINDOW, chipX, chipY, player):
    RED = (255,0,0)
    WHITE = (255,255,255)
    if player == 'player1':
        color = RED
    else:
        color = WHITE

    X = (chipX * 75) + 37
    Y = (chipY * 75) + 37

    pygame.draw.circle(WINDOW, color, (X , Y), 35)
    pygame.display.update()
