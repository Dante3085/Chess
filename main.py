
"""
TODO: Improve code structure in entire project...
      1. Reduce dependencies between pieces of code(update/render, ...)

TODO: Enforce pip python styleguide to learn to write code that is consistent with one style.

TODO: Display pieces that have been beaten.

TODO: GUI-Widgets to control the chess game...
      1. Pause/Resume game
      2. Display who won the game with text.
      3. Display how many moves it took to win the game.
      4.
"""

from Chess import Board
from AI import *
import pygame
import sys
import os
import threading
import time

def checkMatchResult(matchResult, board):
    if matchResult == "w" or matchResult == "b":
        print("Es brauchte '" + str(board.logicalBoard.moveCounter) + "' Züge, um das Spiel zu beenden.")
        if matchResult == "w":
            print("Weiß hat gewonnen.")
        else:
            print("Schwarz hat gewonnen.")
        sys.exit()

def agent_make_move(board, agentWhite, agentBlack):
    # input("Press Enter")
    # time.sleep(.3)

    # Make white move and check if game has ended.
    whiteMove = agentWhite.make_move(board.logicalBoard)
    print("w:" + str(whiteMove), end=" ")

    matchResultAfterWhiteMove = board.move_trad(whiteMove[0], whiteMove[1])
    checkMatchResult(matchResultAfterWhiteMove, board)

    # Make black move and check if game has ended.
    blackMove = agentBlack.make_move(board.logicalBoard)
    print("b:" + str(blackMove))

    matchResultAfterBlackMove = board.move_trad(blackMove[0], blackMove[1])
    checkMatchResult(matchResultAfterBlackMove, board)

    # If game has not ended repeat this function.
    threading.Thread(target=agent_make_move, args=[board, agentWhite, agentBlack]).start()

board = Board()
screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE | pygame.DOUBLEBUF)

agentWhite = RandomAgent(isWhite=True)
agentBlack = GreedyAgent(isWhite=False)

thread = threading.Thread(target=agent_make_move, args=[board, agentWhite, agentBlack])
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
            elif event.key == pygame.K_SPACE:
                isPaused = not isPaused

            elif event.key == pygame.K_RETURN:
                print(board)

    board.update(screen)
    board.render(screen)

    # update display surface to screen
    pygame.display.flip()