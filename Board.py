
from LogicalBoard import LogicalBoard
from BoardRenderer import BoardRenderer
from BoardInteractor import BoardInteractor

class Board:
    def __init__(self):
        self.logicalBoard = LogicalBoard()
        self.boardRenderer = BoardRenderer(self.logicalBoard)
        self.boardInteractor = BoardInteractor(self.boardRenderer)

    def update(self, screen):
        self.boardRenderer.update(screen)
        self.boardInteractor.update()

    def render(self, screen):
        self.boardRenderer.render(screen)

    def __repr__(self):
        return self.logicalBoard.__repr__()