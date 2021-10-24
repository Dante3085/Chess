
# TODO: Enforce pip python styleguide to learn to write code that is consistent with one style.

from Chess import Board
import pygame
import sys
import threading

def make_move(board):
    move = input(">>")
    fromAndTo = move.split("->")
    fromLoc = fromAndTo[0]
    toLoc = fromAndTo[1]
    board.move(fromLoc, toLoc)

    threading.Thread(target=make_move, args=[board]).start()

board = Board()
screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE | pygame.DOUBLEBUF)

thread = threading.Thread(target=make_move, args=[board])
thread.start()

while 1:
    # check pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitEvent = pygame.event.Event(pygame.QUIT, {})
                pygame.event.post(quitEvent)

            elif event.key == pygame.K_RETURN:
                print(board)

    board.update(screen)
    board.render(screen)

    # update display surface to screen
    pygame.display.flip()
