import pygame

def drawBoard(WINDOW, WIDTH, HEIGHT):
    for count, column in enumerate(range(9)):
        pygame.draw.line(WINDOW, (0,0,0), (count * 75, 0), (count * 75, HEIGHT))

    for count, row in enumerate(range(9)):
        pygame.draw.line(WINDOW, (0,0,0), (0, count * 75), (WIDTH, count * 75))
