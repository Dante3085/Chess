
from LogicalBoard import LogicalBoard
from BoardRenderer import BoardRenderer
from BoardInteractor import BoardInteractor

class Board:
    def __init__(self):
        self.logicalBoard = LogicalBoard(board=[
                ["bR", "bS", "bB", "bQ", "bK", "bB", "bS", "bR"],
                ["bP", "bP", "bP", "bP", "||", "||", "bP", "bP"],
                ["||", "||", "||", "||", "||", "||", "||", "||",],
                ["||", "||", "||", "||", "||", "bP", "||", "||",],
                ["||", "||", "||", "||", "||", "||", "wP", "||",],
                ["||", "||", "||", "||", "bP", "||", "||", "||",],
                ["wP", "wP", "wP", "wP", "wP", "wP", "||", "wP"],
                ["wR", "wS", "wB", "wQ", "wK", "wB", "wS", "wR"]
        ])
        self.boardRenderer = BoardRenderer(self.logicalBoard)
        self.boardInteractor = BoardInteractor(self.boardRenderer)

    def update(self, screen):
        self.boardRenderer.update(screen)
        self.boardInteractor.update()

    def render(self, screen):
        self.boardRenderer.render(screen)

    def __repr__(self):
        return self.logicalBoard.__repr__()