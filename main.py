
# TODO: Enforce pip python styleguide to learn to write code that is consistent with one style.

from Chess import Board
from AI import RandomAgent
import pygame
import sys
import os
import threading
import time

def agent_make_move(board, agent):
    # input("Press Enter")
    # time.sleep(.1)

    # Get and parse the move
    move = agent.make_move(board.logicalBoard)
    fromAndTo = move.split("->")
    fromLoc = fromAndTo[0]
    toLoc = fromAndTo[1]

    # Make the move
    matchResult = board.move(fromLoc, toLoc)

    # Check whether the game has ended, if not make the next move.
    if matchResult == "w" or matchResult == "b":
        print("Es brauchte '" + str(board.logicalBoard.moveCounter) + "' Züge, um das Spiel zu beenden.")
        sys.exit()
    elif matchResult is None:
        threading.Thread(target=agent_make_move, args=[board, agent]).start()

board = Board()
screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE | pygame.DOUBLEBUF)

agent = RandomAgent(isWhite=True)

thread = threading.Thread(target=agent_make_move, args=[board, agent])
thread.start()

while 1:
    # check pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)
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
