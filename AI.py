
import random

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