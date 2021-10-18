
import pygame

class BoardInteractor:
    def __init__(self, boardRenderer):
        self.boardRenderer = boardRenderer

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.update_mouse_hover(mousePos)

    def update_mouse_hover(self, mousePos):
        for row in range(0, 8):
            for col in range(0, 8):
                if self.boardRenderer.boardCells[row][col].collidepoint(mousePos):
                    self.boardRenderer.mark_cell(row, col)
                    return
        self.boardRenderer.mark_cell(-1, -1)
        