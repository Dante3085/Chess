
'''
TODO: Maybe let the agent reward itself when it knows that the game is done?
    - Problem: When does the agent know that the game is a draw?
               Usually someone just decides that it is, no?
'''

class ChessAgent:
    def __init__(self, isWhite) -> None:
        self.isWhite = isWhite

    def make_move(self, board):
        '''Returns the next best move based on the given board and whether
           the Agent plays white or black.'''

        # The neural network gets the board and whether it plays white or black as inputs and
        # outputs a move in the style of "e1->e4".

        return "a2->a3"

        pass

    def give_reward(self, reward):
        '''Gives a reward to the agent for the three possible end states of a chess game:
           winning(reward=1), losing(reward=0), draw(reward=0.5)'''
        pass
