
'''
TODO: Maybe let the agent reward itself when it knows that the game is done?
    - Problem: When does the agent know that the game is a draw?
               Usually someone just decides that it is, no?
'''

import random

class ChessAgent:
    def __init__(self, isWhite) -> None:
        self.isWhite = isWhite

    def make_move(self, board):
        """Returns the next best move based on the given board and whether
           the Agent plays white or black."""

        # The neural network gets the board and whether it plays white or black as inputs and
        # outputs a move in the style of "e1->e4".

        return "a2->a3"

        pass

    def give_reward(self, reward):
        """Gives a reward to the agent for the three possible end states of a chess game:
           winning(reward=1), losing(reward=0), draw(reward=0.5)"""
        pass

class RandomAgent:
    def __init__(self, isWhite):
        self.isWhite = isWhite

    def make_move(self, board):
        # Get all pieces of the right color.
        allPieces = []
        if self.isWhite:
            allPieces = board.get_all_white_pieces()
        else:
            allPieces = board.get_all_black_pieces()

        # Get all the possible moves these pieces can make.
        # And eliminate pieces that don't have any moves.
        possibleMoves = []
        for piece in allPieces:
            piecePossibleMoves = board.get_possible_moves(piece)
            for piecePossibleMove in piecePossibleMoves:
                possibleMoves.append(board.array_to_trad(piece) + "->" + board.array_to_trad(piecePossibleMove))
            
        # Return a random move from these moves.
        return possibleMoves[random.randint(0, len(possibleMoves)-1 )]