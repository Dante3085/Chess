
'''
Um diese Klasse umzusetzen, muss ich erst noch mehr über PyGame wissen.
Folgende Stichworte:
- Game-Loop
- Fenstersystem (Worauf soll gerendert werden?)
- Board als Bild oder einzelne Rectangles?
- TODO: Schrift relativ zur Bildschirmgröße.
'''

import pygame
import math

class Piece:
    def __init__(self, image, pos=(0, 0)):
        self.pos = pos
        self.image = image

class BoardRenderer:
    def __init__(self, logicalBoard) -> None:

        # board stuff
        self.logicalBoard = logicalBoard
        self.boardCells = []
        self.boardColor1 = (118,150,86)
        self.boardColor2 = (238,238,210)
        self.markColor = (0, 0, 255)
        self.markedCell = (-1, -1)
        self.possibleMoves = []
        self.pieces = []
        self.movingPiece = None

        self.init_pieces()

        # font stuff
        pygame.font.init()
        self.textColor = (255, 0, 0)

    def update_text(self, cellSize):
        fontSize = math.floor(math.sqrt(0.1 * pow(cellSize, 2)))
        self.myFont = pygame.font.SysFont("Times New Roman", fontSize)

        self.numberTexts = [
            self.myFont.render("1", True, self.textColor),
            self.myFont.render("2", True, self.textColor),
            self.myFont.render("3", True, self.textColor),
            self.myFont.render("4", True, self.textColor),
            self.myFont.render("5", True, self.textColor),
            self.myFont.render("6", True, self.textColor),
            self.myFont.render("7", True, self.textColor),
            self.myFont.render("8", True, self.textColor)
        ]

        self.letterTexts = [
            self.myFont.render("a", True, self.textColor),
            self.myFont.render("b", True, self.textColor),
            self.myFont.render("c", True, self.textColor),
            self.myFont.render("d", True, self.textColor),
            self.myFont.render("e", True, self.textColor),
            self.myFont.render("f", True, self.textColor),
            self.myFont.render("g", True, self.textColor),
            self.myFont.render("h", True, self.textColor)
        ]

    def init_pieces(self):
        '''Loads all the images for the chess pieces.'''
        
        self.originalWhitePawnImage = pygame.image.load("pieces/whitePawn.png")
        self.whitePawnImage = self.originalWhitePawnImage
        self.originalWhiteKingImage = pygame.image.load("pieces/whiteKing.png")
        self.whiteKingImage = self.originalWhiteKingImage
        self.originalWhiteQueenImage = pygame.image.load("pieces/whiteQueen.png")
        self.whiteQueenImage = self.originalWhiteQueenImage
        self.originalWhiteRookImage = pygame.image.load("pieces/whiteRook.png")
        self.whiteRookImage = self.originalWhiteRookImage
        self.originalWhiteBishopImage = pygame.image.load("pieces/whiteBishop.png")
        self.whiteBishopImage = self.originalWhiteBishopImage
        self.originalWhiteKnightImage = pygame.image.load("pieces/whiteKnight.png")
        self.whiteKnightImage = self.originalWhiteKnightImage

        self.originalBlackPawnImage = pygame.image.load("pieces/blackPawn.png")
        self.blackPawnImage = self.originalBlackPawnImage
        self.originalBlackKingImage = pygame.image.load("pieces/blackKing.png")
        self.blackKingImage = self.originalBlackKingImage
        self.originalBlackQueenImage = pygame.image.load("pieces/blackQueen.png")
        self.blackQueenImage = self.originalBlackQueenImage
        self.originalBlackRookImage = pygame.image.load("pieces/blackRook.png")
        self.blackRookImage = self.originalBlackRookImage
        self.originalBlackBishopImage = pygame.image.load("pieces/blackBishop.png")
        self.blackBishopImage = self.originalBlackBishopImage
        self.originalBlackKnightImage = pygame.image.load("pieces/blackKnight.png")
        self.blackKnightImage = self.originalWhiteKnightImage

    def update(self, screen):
        '''Updates the visual representation of the board according to the screen's properties'''

        cellSize = screen.get_height() / 8
        marginSize = (screen.get_width() - screen.get_height()) / 2
        boardPosition = (marginSize, 0)

        self.update_text(cellSize)
        self.update_board_cells(cellSize, marginSize, boardPosition)
        self.update_chess_pieces(cellSize)
        self.update_mark_possible_moves()

    def update_mark_possible_moves(self):
        # if the marked cell has a piece in it, show the possible moves that it can make.
        if (self.markedCell != (-1, -1) and 
            self.logicalBoard.get_piece_array(self.markedCell[0], self.markedCell[1]) != self.logicalBoard.emptyPiece):
            self.possibleMoves = self.logicalBoard.get_possible_moves((self.markedCell[0], self.markedCell[1]))
        else:
            self.possibleMoves = []


    def update_board_cells(self, cellSize, marginSize, boardPosition):
        self.boardCells = []
        for row in range(0, 8):
            self.boardCells.append([])
            for col in range(0, 8):
                cell = pygame.Rect(boardPosition[0] + col*cellSize,
                                   boardPosition[1] + row*cellSize, 
                                   cellSize, cellSize)
                self.boardCells[row].append(cell)

    def update_chess_pieces(self, cellSize):
        self.whitePawnImage = pygame.transform.smoothscale(self.originalWhitePawnImage, (int(cellSize), int(cellSize)))
        self.whiteQueenImage = pygame.transform.smoothscale(self.originalWhiteQueenImage, (int(cellSize), int(cellSize)))
        self.whiteRookImage = pygame.transform.smoothscale(self.originalWhiteRookImage, (int(cellSize), int(cellSize)))
        self.whiteKnightImage = pygame.transform.smoothscale(self.originalWhiteKnightImage, (int(cellSize), int(cellSize)))
        self.whiteBishopImage = pygame.transform.smoothscale(self.originalWhiteBishopImage, (int(cellSize), int(cellSize)))
        self.whiteKingImage = pygame.transform.smoothscale(self.originalWhiteKingImage, (int(cellSize), int(cellSize)))

        self.blackPawnImage = pygame.transform.smoothscale(self.originalBlackPawnImage, (int(cellSize), int(cellSize)))
        self.blackQueenImage = pygame.transform.smoothscale(self.originalBlackQueenImage, (int(cellSize), int(cellSize)))
        self.blackRookImage = pygame.transform.smoothscale(self.originalBlackRookImage, (int(cellSize), int(cellSize)))
        self.blackKnightImage = pygame.transform.smoothscale(self.originalBlackKnightImage, (int(cellSize), int(cellSize)))
        self.blackBishopImage = pygame.transform.smoothscale(self.originalBlackBishopImage, (int(cellSize), int(cellSize)))
        self.blackKingImage = pygame.transform.smoothscale(self.originalBlackKingImage, (int(cellSize), int(cellSize)))

    def render(self, screen):
        '''Renders the visual representation of the board to the given surface'''

        cellSize = screen.get_height() / 8
        marginSize = (screen.get_width() - screen.get_height()) / 2
        boardPosition = (marginSize, 0)

        self.render_board(screen)
        self.render_text(screen, cellSize, marginSize, boardPosition)
        self.render_pieces(screen, cellSize, boardPosition)
        self.render_possible_moves(screen, cellSize)

    def mark_cell(self, row, col):
        self.markedCell = (row, col)

    """ def move_piece(self, row, col, newPos):
        cell = self.boardCells[row][col]

        if self.movingPiece == None:
            for piece in self.pieces:
                if piece.pos == cell.topleft:
                    self.movingPiece = piece
                    break """

    """ def stop_moving_piece(self):
        self.movingPiece = None """

    def get_marked_cell(self):
        if self.markedCell == (-1, -1):
            return None
        else:
            return self.boardCells[self.markedCell[0]][self.markedCell[1]]

    def render_possible_moves(self, screen, cellSize):
        if len(self.possibleMoves) > 0:
            circleRadius = math.sqrt((0.05*pow(cellSize, 2)) / math.pi)
            for possibleMove in self.possibleMoves:
                pygame.draw.circle(screen, (0, 255, 0), self.boardCells[possibleMove[0]][possibleMove[1]].center, 
                                   radius=circleRadius)

    def render_pieces(self, screen, cellSize, boardPosition):
        '''Renders the chess pieces on to the chess board.'''

        for row in range(0, 8):
            for col in range(0, 8):
                currentPiece = self.logicalBoard.board[row][col]
                if currentPiece == "wP":
                    screen.blit(self.whitePawnImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "wK":
                    screen.blit(self.whiteKingImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "wR":
                    screen.blit(self.whiteRookImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "wS":
                    screen.blit(self.whiteKnightImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "wB":
                    screen.blit(self.whiteBishopImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "wQ":
                    screen.blit(self.whiteQueenImage, dest=self.boardCells[row][col].topleft)
                
                elif currentPiece == "bP":
                    screen.blit(self.blackPawnImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "bK":
                    screen.blit(self.blackKingImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "bR":
                    screen.blit(self.blackRookImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "bS":
                    screen.blit(self.blackKnightImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "bB":
                    screen.blit(self.blackBishopImage, dest=self.boardCells[row][col].topleft)
                elif currentPiece == "bQ":
                    screen.blit(self.blackQueenImage, dest=self.boardCells[row][col].topleft) 

    def render_board(self, screen):
        '''Renders the chess board on to the screen.'''

        for row in range(0, 8):
            for col in range(0, 8):
                if (row, col) == self.markedCell:
                    pygame.draw.rect(screen, self.markColor, self.boardCells[row][col])
                else:
                    pygame.draw.rect(screen, self.boardColor1 if (row+col) % 2 == 0 else self.boardColor2,
                                 self.boardCells[row][col])

    def render_text(self, screen, cellSize, marginSize, boardPosition):
        '''Renders the chess board numbers and letters on to the chess board.'''

        # numbers
        for row in range(0, 8):
            currentCell = self.boardCells[row][0]
            currentText = self.numberTexts[row]
            textPos = (currentCell.left + 0.1 * currentCell.width,
                       currentCell.top  + 0.1 * currentCell.height)
            screen.blit(currentText, dest=textPos, area=currentText.get_rect())

        # letters
        for col in range(0, 8):
            currentCell = self.boardCells[7][col]
            currentText = self.letterTexts[col]
            textPos = (currentCell.right - 0.2 * currentCell.width,
                       currentCell.bottom - 0.4 * currentCell.height)
            screen.blit(currentText, dest=textPos, area=currentText.get_rect())

        """ screen.blit(self.text_1, dest=self.add_tuples(boardPosition, (10, 0)), area=self.text_1.get_rect())
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
        screen.blit(self.text_h, dest=self.add_tuples(boardPosition, (8*cellSize - 20, yLetters)), area=self.text_h.get_rect()) """

    def add_tuples(self, tuple1, tuple2):
        tupleAsList = list(tuple1)
        for i in range(0, len(tuple1)):
            tupleAsList[i] += tuple2[i]
        return tuple(tupleAsList)