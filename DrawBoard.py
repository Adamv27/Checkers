import pygame
DARK_BROWN = (115,64,18)
LIGHT_BROWN = (255,222,173)

def drawBoard(WINDOW, WIDTH, HEIGHT):
    WINDOW.fill((LIGHT_BROWN))
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(WINDOW, DARK_BROWN, (row * 75, column * 75, 75, 75))

def updateBoard(WINDOW, WIDTH, HEIGHT, board):
    for chipRow, row in enumerate(board.board):
        for chipColumn, space in enumerate(row):
            if space != '':
                if space == 'O':
                    drawChip(WINDOW, chipColumn, chipRow,  'player1')
                else:
                    drawChip(WINDOW, chipColumn, chipRow, 'player2')

def drawChip(WINDOW, chipX, chipY, player):
    RED = (255,0,0)
    WHITE = (255,255,255)
    if player == 'player1':
        color = WHITE
    else:
        color = RED

    X = (chipX * 75) + 37
    Y = (chipY * 75) + 37

    pygame.draw.circle(WINDOW, color, (X , Y), 33)
    pygame.display.update()

def drawHighlight(WINDOW, row, column):
    pygame.draw.rect(WINDOW, (23,188,23), ((column * 75) + 1, (row * 75)  + 1, 72, 72), 4)

def refreshTile(WINDOW, row, column, player):
    if (row + column) % 2 == 0:
        color = DARK_BROWN
    else:
        color = LIGHT_BROWN

    pygame.draw.rect(WINDOW, (color), ((column * 75, row * 75, 75, 75)))

    if player == 'player1':
        drawChip(WINDOW, column, row, 'player1')
    else:
        drawChip(WINDOW, column, row, 'player2')
