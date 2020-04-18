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
                    drawChip(WINDOW, chipColumn, chipRow,  'player1', False)
                elif space == 'OK':
                    drawChip(WINDOW, column, row, 'player1', True)
                elif space == 'X':
                    drawChip(WINDOW, chipColumn, chipRow, 'player2', False)
                elif space == 'XK':
                    drawChip(WINDOW, column, row, 'player2', True)

def drawChip(WINDOW, chipX, chipY, player, isKing):
    RED = (255,0,0)
    WHITE = (255,255,255)
    if player == 'player1':
        color = WHITE
    else:
        color = RED

    X = (chipX * 75) + 37
    Y = (chipY * 75) + 37

    pygame.draw.circle(WINDOW, color, (X , Y), 33)

    if isKing:
        image = pygame.image.load('crown.png')
        image = pygame.transform.scale(image, (55,55))
        WINDOW.blit(image, (X - 28,Y - 28))
    pygame.display.update()

def drawHighlight(WINDOW, row, column):
    pygame.draw.rect(WINDOW, (23,188,23), ((column * 75) + 1, (row * 75)  + 1, 72, 72), 4)

def refreshTile(WINDOW, board, row, column):
    if (row + column) % 2 == 0:
        color = DARK_BROWN
    else:
        color = LIGHT_BROWN

    pygame.draw.rect(WINDOW, (color), ((column * 75, row * 75, 75, 75)))
    if board[row][column] == 'O':
        drawChip(WINDOW, column, row, 'player1', False)
    elif board[row][column] == 'OK':
        drawChip(WINDOW, column, row, 'player1', True)
    elif board[row][column] == 'X':
        drawChip(WINDOW, column, row, 'player2', False)
    elif board[row][column] == 'XK':
        drawChip(WINDOW, column, row, 'player2', True)
