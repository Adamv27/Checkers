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

class Board:
    board = []

    def resetBoard():
        board = []
        for row in range(8):
            row = []
            for column in range(8):
                row.append('')
            board.append(row)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    Board.printBoard()
    input()

    screen.fill((LIGHT_BROWN))
    draw.drawBoard(screen, WIDTH, HEIGHT)
    pygame.display.update()
