
# TODO: Enforce pip python styleguide to learn to write code that is consistent with one style.

from Chess import Board
from AI import ChessAgent
import pygame
import sys
import threading

def agent_make_move(board, agent):
    input("Press Enter")

    # Get and parse the move
    move = agent.make_move(board)
    fromAndTo = move.split("->")
    fromLoc = fromAndTo[0]
    toLoc = fromAndTo[1]

    # Make the move
    matchResult = board.move(fromLoc, toLoc)

    # Check whether the game has ended, if not make the next move.
    if matchResult == "w":
        if agent.isWhite: agent.give_reward(1)
        else: agent.give_reward(0)
    elif matchResult == "b":
        if agent.isWhite: agent.give_reward(0)
        else: agent.give_reward(1)
    elif matchResult == None:
        threading.Thread(target=agent_make_move, args=[board, agent]).start()

board = Board()
screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE | pygame.DOUBLEBUF)

agent = ChessAgent(isWhite=True)

thread = threading.Thread(target=agent_make_move, args=[board, agent])
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
