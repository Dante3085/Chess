
from LogicalBoard import LogicalBoard
from BoardRenderer import BoardRenderer

class Board:
    def __init__(self):
        self.logicalBoard = LogicalBoard()
        self.boardRenderer = BoardRenderer(self.logicalBoard)

    def update(self, screen):
        self.boardRenderer.update(screen)

    def render(self, screen):
        self.boardRenderer.render(screen)

    def __repr__(self):
        return self.logicalBoard.__repr__()