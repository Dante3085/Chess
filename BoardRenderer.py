
'''
Um diese Klasse umzusetzen, muss ich erst noch mehr über PyGame wissen.
Folgende Stichworte:
- Game-Loop
- Fenstersystem (Worauf soll gerendert werden?)
- Board als Bild oder einzelne Rectangles?
'''

import pygame

class BoardRenderer:
    def __init__(self, board) -> None:

        # board stuff
        self.board = board
        # self.boardImage = pygame.image.load("Chess_Board.png")
        self.boardColor1 = (118,150,86)
        self.boardColor2 = (238,238,210)

        # font stuff
        pygame.font.init()
        myFont = pygame.font.SysFont("Times New Roman", 25)

        self.textColor = (255, 0, 0)

        self.text_1 = myFont.render("1", True, self.textColor)
        self.text_2 = myFont.render("2", True, self.textColor)
        self.text_3 = myFont.render("3", True, self.textColor)
        self.text_4 = myFont.render("4", True, self.textColor)
        self.text_5 = myFont.render("5", True, self.textColor)
        self.text_6 = myFont.render("6", True, self.textColor)
        self.text_7 = myFont.render("7", True, self.textColor)
        self.text_8 = myFont.render("8", True, self.textColor)

        self.text_a = myFont.render("a", True, self.textColor)
        self.text_b = myFont.render("b", True, self.textColor)
        self.text_c = myFont.render("c", True, self.textColor)
        self.text_d = myFont.render("d", True, self.textColor)
        self.text_e = myFont.render("e", True, self.textColor)
        self.text_f = myFont.render("f", True, self.textColor)
        self.text_g = myFont.render("g", True, self.textColor)
        self.text_h = myFont.render("h", True, self.textColor)

    def render(self, screen):
        self.render_board(screen)
        self.render_text(screen)

    def render_board(self, screen):
        cellSize = screen.get_height() / 8
        marginSize = (screen.get_width() - screen.get_height()) / 2
        boardPosition = (marginSize, 0)

        for row in range(0, 8):
            for col in range(0, 8):
                cell = pygame.Rect(boardPosition[0] + col*cellSize,
                                   boardPosition[1] + row*cellSize, 
                                   cellSize, cellSize)
                pygame.draw.rect(screen, self.boardColor1 if (row+col) % 2 == 0 else self.boardColor2, cell)

    def render_text(self, screen):
        marginSize = (screen.get_width() - screen.get_height()) / 2
        boardPosition = (marginSize, 0)
        cellSize = screen.get_height() / 8

        screen.blit(self.text_1, dest=self.add_tuples(boardPosition, (10, 0)), area=self.text_1.get_rect())
        screen.blit(self.text_2, dest=self.add_tuples(boardPosition, (10, cellSize)), area=self.text_2.get_rect())
        screen.blit(self.text_3, dest=self.add_tuples(boardPosition, (10, 2*cellSize)), area=self.text_3.get_rect())
        screen.blit(self.text_4, dest=self.add_tuples(boardPosition, (10, 3*cellSize)), area=self.text_4.get_rect())
        screen.blit(self.text_5, dest=self.add_tuples(boardPosition, (10, 4*cellSize)), area=self.text_5.get_rect())
        screen.blit(self.text_6, dest=self.add_tuples(boardPosition, (10, 5*cellSize)), area=self.text_6.get_rect())
        screen.blit(self.text_7, dest=self.add_tuples(boardPosition, (10, 6*cellSize)), area=self.text_7.get_rect())
        screen.blit(self.text_8, dest=self.add_tuples(boardPosition, (10, 7*cellSize)), area=self.text_8.get_rect())

        yLetters = screen.get_height() - 30

        screen.blit(self.text_a, dest=self.add_tuples(boardPosition, (1*cellSize - 20, yLetters)), area=self.text_a.get_rect())
        screen.blit(self.text_b, dest=self.add_tuples(boardPosition, (2*cellSize - 20, yLetters)), area=self.text_b.get_rect())
        screen.blit(self.text_c, dest=self.add_tuples(boardPosition, (3*cellSize - 20, yLetters)), area=self.text_c.get_rect())
        screen.blit(self.text_d, dest=self.add_tuples(boardPosition, (4*cellSize - 20, yLetters)), area=self.text_d.get_rect())
        screen.blit(self.text_e, dest=self.add_tuples(boardPosition, (5*cellSize - 20, yLetters)), area=self.text_e.get_rect())
        screen.blit(self.text_f, dest=self.add_tuples(boardPosition, (6*cellSize - 20, yLetters)), area=self.text_f.get_rect())
        screen.blit(self.text_g, dest=self.add_tuples(boardPosition, (7*cellSize - 20, yLetters)), area=self.text_g.get_rect())
        screen.blit(self.text_h, dest=self.add_tuples(boardPosition, (8*cellSize - 20, yLetters)), area=self.text_h.get_rect())

    def add_tuples(self, tuple1, tuple2):
        tupleAsList = list(tuple1)
        for i in range(0, len(tuple1)):
            tupleAsList[i] += tuple2[i]
        return tuple(tupleAsList)