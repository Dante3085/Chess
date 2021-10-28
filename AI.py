
'''
TODO: Maybe let the agent reward itself when it knows that the game is done?
    - Problem: When does the agent know that the game is a draw?
               Usually someone just decides that it is, no?
'''

import random

# class ChessAgent:
#     def __init__(self, isWhite) -> None:
#         self.isWhite = isWhite
#
#     def make_move(self, board):
#         """Returns the next best move based on the given board and whether
#            the Agent plays white or black."""
#
#         # The neural network gets the board and whether it plays white or black as inputs and
#         # outputs a move in the style of "e1->e4".
#
#         return "a2->a3"
#
#         pass
#
#     def give_reward(self, reward):
#         """Gives a reward to the agent for the three possible end states of a chess game:
#            winning(reward=1), losing(reward=0), draw(reward=0.5)"""
#         pass

class HumanPlayer:
    def make_move(self, board):
        move = input(">>")
        rowAndCol = move.split(sep="->")
        return (rowAndCol[0], rowAndCol[1])

class RandomAgent:
    """From all the available moves in a given situation, the RandomAgent executes a random one of those."""

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def make_move(self, board):
        allPossibleMoves = []
        if self.isWhite:
            allPossibleMoves = board.get_all_possible_moves_white()
        else:
            allPossibleMoves = board.get_all_possible_moves_black()
            
        # Return a random move from these moves.
        return allPossibleMoves[random.randint(0, len(allPossibleMoves)-1)]

class GreedyAgent:
    """From all the available moves in a given situation, the GreedyAgent picks any move that
       defeats an enemy. If no such move currently exists, it does a random move."""

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def make_move(self, board):
        allPossibleMoves = []
        if self.isWhite:
            allPossibleMoves = board.get_all_possible_moves_white()
        else:
            allPossibleMoves = board.get_all_possible_moves_black()

        # Do a move that defeats an enemy piece.
        for move in allPossibleMoves:
            pieceAtDestination = board.get_piece(move[1])
            if pieceAtDestination is not None:
                if (
                        (self.isWhite and "b" in pieceAtDestination) or
                        (not self.isWhite and "w" in pieceAtDestination)
                   ):
                    return move

        # Do a random move if no move defeating an enemy piece could be found.
        randomAgent = RandomAgent(self.isWhite)
        return randomAgent.make_move(board)