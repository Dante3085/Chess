
import pygame

class BoardInteractor:
    def __init__(self, boardRenderer):
        self.boardRenderer = boardRenderer
        self.leftMousePressed = False
        self.previousLeftMousePressed = False
        
        self.cellPieceToMove = None

    def update(self):
        mousePos = pygame.mouse.get_pos()

        self.previousLeftMousePressed = self.leftMousePressed
        self.leftMousePressed = pygame.mouse.get_pressed()[0]

        self.update_mouse_hover(mousePos)
        self.update_moving_piece(mousePos)

    def on_left_mouse_pressed(self):
        return self.leftMousePressed and not self.previousLeftMousePressed

    def on_left_mouse_released(self):
        return not self.leftMousePressed and self.previousLeftMousePressed

    def update_moving_piece(self, mousePos):
        '''Moves chess piece that is clicked on by the mouse'''
        
        # on left mouse button being pressed, get the cell where the piece that should
        # be moved is on.
        if self.on_left_mouse_pressed():
            markedCell = self.boardRenderer.markedCell

            # if that cell has a piece on it, remember that as being the piece
            # that should be moved.
            if not self.boardRenderer.cell_is_empty(markedCell[0], markedCell[1]):
                self.cellPieceToMove = markedCell

        # stop moving the piece when the left mouse button is released and
        # put it to it's new cell
        elif self.on_left_mouse_released():
            # self.boardRenderer.move_piece(, mousePos)
            self.cellPieceToMove = None

        # if there is a piece to move, move it to the position of the mouse cursor.
        if self.cellPieceToMove != None:
            cellSize = self.boardRenderer.get_cell_size()
            destination = (mousePos[0] - (cellSize/2), mousePos[1] - (cellSize/2))
            self.boardRenderer.move_piece(self.cellPieceToMove, destination)

    def update_mouse_hover(self, mousePos):
        for row in range(0, 8):
            for col in range(0, 8):
                if self.boardRenderer.boardCells[row][col].collidepoint(mousePos):
                    self.boardRenderer.markedCell = (row, col)
                    return
        self.boardRenderer.markedCell = (-1, -1)
        