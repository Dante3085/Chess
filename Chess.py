'''
b := black
w := white

R := Rook
K := King
S := Springer/Knight
B := Bishop
Q := Queen
P := Pawn
'''

from copy import deepcopy
import pygame
import math


class LogicalBoard:
    def __init__(self, board=None) -> None:
        self.__letterToColumn = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }

        self.__columnToLetter = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h"
        }

        self.moveCounter = 0

        # The empty piece represents the absence of any of the real pieces on a location.
        self.emptyPiece = "||"

        if board is None:
            self.__board = [
                ["bR", "bS", "bB", "bQ", "bK", "bB", "bS", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,
                 self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, ],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,
                 self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, ],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,
                 self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, ],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,
                 self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, ],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wS", "wB", "wQ", "wK", "wB", "wS", "wR"]
            ]
        else:
            if len(board) != 8 or len(board[0]) != 8:
                raise ValueError("Given board has incorrect dimensions. Must be 8x8.")
            else:
                self.__board = board

    def game_has_finished(self):
        """Returns 'w' if white has won, 'b' if black has won and None
           if the game is still going."""

        whiteKingDefeated = True
        blackKingDefeated = True
        for row in self.__board:
            if "wK" in row: whiteKingDefeated = False
            if "bK" in row: blackKingDefeated = False

        if whiteKingDefeated:
            return "b"
        elif blackKingDefeated:
            return "w"
        else:
            return None

    def get_piece(self, pieceLoc):
        """Returns the piece on the board at the given location(e.g. a4, e3)"""
        loc = self.__traditional_to_array(pieceLoc)
        return self.get_piece_array(loc[0], loc[1])

    def get_piece_array(self, row, col):
        """Returns the piece on the board at the given row and column."""
        return self.__board[row][col]

    def get_all_white_pieces(self):
        '''Returns a list with the locations for all the white pieces.'''
        locations = []
        for row in range(0, 8):
            for col in range(0, 8):
                if "w" in self.__board[row][col]:
                    locations.append((row, col))
        return locations

    def get_all_black_pieces(self):
        '''Returns a list with the locations for all the black pieces.'''
        locations = []
        for row in range(0, 8):
            for col in range(0, 8):
                if "b" in self.__board[row][col]:
                    locations.append((row, col))
        return locations
        pass

    def __traditional_to_array(self, trad):
        '''Converts the traditional chess notation (e.g.: e8) to an array indexing notation (e.g.: e8 -> row=0, col=4)'''
        # 8 - i
        # 8 is the index of the last row on the board if you count 1 to 8.
        col = self.__letterToColumn[trad[0]]
        row = 8 - int(trad[1])
        return (row, col)

    def __array_to_trad(self, rowAndCol):
        return self.__columnToLetter[rowAndCol[1]] + str(8 - rowAndCol[0])

    def move_piece_array(self, fromLocArray, toLocArray):
        if not self.validate_move(fromLocArray, toLocArray):
            raise ValueError("Given move '" + str(fromLocArray) +
                             " -> " + str(toLocArray) + "' is unvalid.")
        else:
            # increment move counter
            self.moveCounter += 1

            # move piece to new location
            self.__board[toLocArray[0]][toLocArray[1]] = self.__board[fromLocArray[0]][fromLocArray[1]]

            # remove piece from old location
            self.__board[fromLocArray[0]][fromLocArray[1]] = self.emptyPiece

        return str(fromLocArray) + " -> " + str(toLocArray)

    def move_piece(self, fromLoc, toLoc):
        fromLocArray = self.__traditional_to_array(fromLoc)
        toLocArray = self.__traditional_to_array(toLoc)

        return self.move_piece_array(fromLocArray, toLocArray)

    def validate_move(self, fromLoc, toLoc):
        # Determine the type of piece that is about to be moved.
        pieceType = self.__board[fromLoc[0]][fromLoc[1]][1]

        # For each type of piece delegate to a specific sub-method that checks move validity.
        if pieceType == "R":
            return toLoc in self.__get_possible_moves_rook(fromLoc)
        elif pieceType == "K":
            return toLoc in self.__get_possible_moves_king(fromLoc)
        elif pieceType == "S":
            return toLoc in self.__get_possible_moves_knight(fromLoc)
        elif pieceType == "B":
            return toLoc in self.__get_possible_moves_bishop(fromLoc)
        elif pieceType == "Q":
            return toLoc in self.__get_possible_moves_queen(fromLoc)
        elif pieceType == "P":
            return toLoc in self.__get_possible_moves_pawn(fromLoc)

    def get_possible_moves(self, position):
        piece = self.__board[position[0]][position[1]]
        if "R" in piece:
            return self.__get_possible_moves_rook(position)
        elif "K" in piece:
            return self.__get_possible_moves_king(position)
        elif "S" in piece:
            return self.__get_possible_moves_knight(position)
        elif "B" in piece:
            return self.__get_possible_moves_bishop(position)
        elif "Q" in piece:
            return self.__get_possible_moves_queen(position)
        elif "P" in piece:
            return self.__get_possible_moves_pawn(position)

    def get_all_possible_moves_white(self):
        allWhitePieces = self.get_all_white_pieces()
        allPossibleMovesWhite = []
        for whitePiecePosition in allWhitePieces:
            whitePiecePossibleDestinations = self.get_possible_moves(whitePiecePosition)
            for destination in whitePiecePossibleDestinations:
                allPossibleMovesWhite.append(
                    (self.__array_to_trad(whitePiecePosition), self.__array_to_trad(destination)))

        return allPossibleMovesWhite

    def get_all_possible_moves_black(self):
        allBlackPieces = self.get_all_black_pieces()
        allPossibleMovesBlack = []
        for blackPiecePosition in allBlackPieces:
            blackPiecePossibleDestinations = self.get_possible_moves(blackPiecePosition)
            for destination in blackPiecePossibleDestinations:
                allPossibleMovesBlack.append(
                    (self.__array_to_trad(blackPiecePosition), self.__array_to_trad(destination)))

        return allPossibleMovesBlack

    def __get_possible_moves_rook(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        rookColor = self.__board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # up
        for i in range(fromRow - 1, -1, -1):
            newLocation = (i, fromCol)
            possibleLocations.append(newLocation)
            if self.__board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # down
        for i in range(fromRow + 1, 8):
            newLocation = (i, fromCol)
            possibleLocations.append(newLocation)
            if self.__board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # right
        for i in range(fromCol + 1, 8):
            newLocation = (fromRow, i)
            possibleLocations.append(newLocation)
            if self.__board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # left
        for i in range(fromCol - 1, -1, -1):
            newLocation = (fromRow, i)
            possibleLocations.append(newLocation)
            if self.__board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        return self.__remove_not_on_board_and_friendly(possibleLocations, rookColor)

    def __get_possible_moves_king(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        kingColor = self.__board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = [
            (fromRow - 1, fromCol),
            (fromRow, fromCol + 1),
            (fromRow + 1, fromCol),
            (fromRow, fromCol - 1)
        ]

        return self.__remove_not_on_board_and_friendly(possibleLocations, kingColor)

    def __get_possible_moves_bishop(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        bishopColor = self.__board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # top left
        row = fromRow - 1
        col = fromCol - 1
        while row >= 0 and col >= 0:
            possibleLocations.append((row, col))

            # Break the loop if we encountered a piece
            if self.__board[row][col] != self.emptyPiece:
                break

            row -= 1
            col -= 1

        # top right
        row = fromRow - 1
        col = fromCol + 1
        while row >= 0 and col <= 7:
            possibleLocations.append((row, col))

            if self.__board[row][col] != self.emptyPiece:
                break

            row -= 1
            col += 1

        # bottom right
        row = fromRow + 1
        col = fromCol + 1
        while row <= 7 and col <= 7:
            possibleLocations.append((row, col))

            if self.__board[row][col] != self.emptyPiece:
                break

            row += 1
            col += 1

        # bottom left
        row = fromRow + 1
        col = fromCol - 1
        while row <= 7 and col >= 0:
            possibleLocations.append((row, col))

            if self.__board[row][col] != self.emptyPiece:
                break

            row += 1
            col -= 1

        return self.__remove_not_on_board_and_friendly(possibleLocations, bishopColor)

    def __get_possible_moves_queen(self, fromLoc):
        return self.__get_possible_moves_bishop(fromLoc) + \
               self.__get_possible_moves_rook(fromLoc)

    def __get_possible_moves_knight(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        knightColor = self.__board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = [
            (fromRow + 2, fromCol + 1),
            (fromRow + 2, fromCol - 1),

            (fromRow - 2, fromCol + 1),
            (fromRow - 2, fromCol - 1),

            (fromRow + 1, fromCol + 2),
            (fromRow + 1, fromCol - 2),

            (fromRow - 1, fromCol + 2),
            (fromRow - 1, fromCol - 2)
        ]

        return self.__remove_not_on_board_and_friendly(possibleLocations, knightColor)

    def __get_possible_moves_pawn(self, fromLoc):
        if fromLoc[0] == 7 or fromLoc[0] == 0:
            return []

        # Black or white pawn?
        pawnColor = self.__board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # black pawn
        if pawnColor == "b":
            # No enemy piece in front
            if self.__board[fromLoc[0] + 1][fromLoc[1]] == self.emptyPiece:
                possibleLocations.append((fromLoc[0] + 1, fromLoc[1]))

                # Is the pawn in it's initial location or has it already been moved?
                # 1 is the index of the row where all the black pawns start.
                if fromLoc[0] == 1:
                    possibleLocations.append((fromLoc[0] + 2, fromLoc[1]))

            # Enemy pieces diagonally
            # Pawn hugs left wall
            if fromLoc[1] == 0:
                if "w" in self.__board[fromLoc[0] + 1][1]:
                    possibleLocations.append((fromLoc[0] + 1, 1))

            # Pawn hugs right wall
            elif fromLoc[1] == 7:
                if "w" in self.__board[fromLoc[0] + 1][6]:
                    possibleLocations.append((fromLoc[0] + 1, 6))

            # Pawn doesn't hug a wall
            else:
                # left diagonal
                if "w" in self.__board[fromLoc[0] + 1][fromLoc[1] - 1]:
                    possibleLocations.append(
                        (fromLoc[0] + 1, fromLoc[1] - 1))
                # right diagonal
                if "w" in self.__board[fromLoc[0] + 1][fromLoc[1] + 1]:
                    possibleLocations.append(
                        (fromLoc[0] + 1, fromLoc[1] + 1))

        # white pawn
        else:
            # no piece in front
            if self.__board[fromLoc[0] - 1][fromLoc[1]] == self.emptyPiece:
                possibleLocations.append((fromLoc[0] - 1, fromLoc[1]))

                # initial pos
                if fromLoc[0] == 6:
                    possibleLocations.append((fromLoc[0] - 2, fromLoc[1]))

            # enemy pieces diagonally
            # hugs left wall
            if fromLoc[1] == 0:
                if "b" in self.__board[fromLoc[0] - 1][1]:
                    possibleLocations.append((fromLoc[0] - 1, 1))

            # hugs right wall
            elif fromLoc[1] == 7:
                if "b" in self.__board[fromLoc[0] - 1][6]:
                    possibleLocations.append((fromLoc[0] - 1, 6))

            # doesnt hug wall
            else:
                # left diagonal
                if "b" in self.__board[fromLoc[0] - 1][fromLoc[1] - 1]:
                    possibleLocations.append(
                        (fromLoc[0] - 1, fromLoc[1] - 1))
                # right diagonal
                if "b" in self.__board[fromLoc[0] - 1][fromLoc[1] + 1]:
                    possibleLocations.append(
                        (fromLoc[0] - 1, fromLoc[1] + 1))

        return possibleLocations

    def __remove_not_on_board_and_friendly(self, possibleLocations, pieceColor):
        '''From a list of (row, col) board coordinates this method removes the
           coordinates that are either outside of the board or contain a friendly
           piece relative to the given pieceColor.'''

        locationsToRemove = []
        for location in possibleLocations:
            if (
                    location[0] < 0 or location[0] > 7 or
                    location[1] < 0 or location[1] > 7
            ):
                locationsToRemove.append(location)
            elif (
                    pieceColor == "w" and "w" in self.__board[location[0]][location[1]] or
                    pieceColor == "b" and "b" in self.__board[location[0]][location[1]]
            ):
                locationsToRemove.append(location)

        finalLocations = deepcopy(possibleLocations)
        for location in locationsToRemove:
            finalLocations.remove(location)

        return finalLocations

    def __repr__(self) -> str:
        boardStr = ""
        rowIndex = 8

        for row in self.__board:
            boardStr += str(rowIndex) + " "
            rowIndex -= 1
            for piece in row:
                boardStr += piece + " "
            boardStr += "\n"

        boardStr += "  a  b  c  d  e  f  g  h"

        return boardStr

class BoardRenderer:
    def __init__(self, logicalBoard: LogicalBoard) -> None:

        # board stuff
        self.logicalBoard = logicalBoard
        self.boardCells = []
        self.boardColor1 = (118, 150, 86)
        self.boardColor2 = (238, 238, 210)
        self.markColor = (0, 0, 255)
        self.markedCell = (-1, -1)
        self.possibleMoves = []
        self.cellPieceToMove = (-1, -1)
        self.mousePos = (-1, -1)

        self.init_pieces_images()

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

    def init_pieces_images(self):
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
                self.logicalBoard.get_piece_array(self.markedCell[0],
                                                  self.markedCell[1]) != self.logicalBoard.emptyPiece):
            self.possibleMoves = self.logicalBoard.get_possible_moves((self.markedCell[0], self.markedCell[1]))
        else:
            self.possibleMoves = []

    def update_board_cells(self, cellSize, marginSize, boardPosition):
        self.boardCells = []
        for row in range(0, 8):
            self.boardCells.append([])
            for col in range(0, 8):
                cell = pygame.Rect(boardPosition[0] + col * cellSize,
                                   boardPosition[1] + row * cellSize,
                                   cellSize, cellSize)
                self.boardCells[row].append(cell)

    def update_chess_pieces(self, cellSize):
        self.whitePawnImage = pygame.transform.smoothscale(self.originalWhitePawnImage, (int(cellSize), int(cellSize)))
        self.whiteQueenImage = pygame.transform.smoothscale(self.originalWhiteQueenImage,
                                                            (int(cellSize), int(cellSize)))
        self.whiteRookImage = pygame.transform.smoothscale(self.originalWhiteRookImage, (int(cellSize), int(cellSize)))
        self.whiteKnightImage = pygame.transform.smoothscale(self.originalWhiteKnightImage,
                                                             (int(cellSize), int(cellSize)))
        self.whiteBishopImage = pygame.transform.smoothscale(self.originalWhiteBishopImage,
                                                             (int(cellSize), int(cellSize)))
        self.whiteKingImage = pygame.transform.smoothscale(self.originalWhiteKingImage, (int(cellSize), int(cellSize)))

        self.blackPawnImage = pygame.transform.smoothscale(self.originalBlackPawnImage, (int(cellSize), int(cellSize)))
        self.blackQueenImage = pygame.transform.smoothscale(self.originalBlackQueenImage,
                                                            (int(cellSize), int(cellSize)))
        self.blackRookImage = pygame.transform.smoothscale(self.originalBlackRookImage, (int(cellSize), int(cellSize)))
        self.blackKnightImage = pygame.transform.smoothscale(self.originalBlackKnightImage,
                                                             (int(cellSize), int(cellSize)))
        self.blackBishopImage = pygame.transform.smoothscale(self.originalBlackBishopImage,
                                                             (int(cellSize), int(cellSize)))
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

    def render_possible_moves(self, screen, cellSize):
        if len(self.possibleMoves) > 0:
            circleRadius = math.sqrt((0.05 * pow(cellSize, 2)) / math.pi)
            for possibleMove in self.possibleMoves:
                pygame.draw.circle(screen, (0, 255, 0), self.boardCells[possibleMove[0]][possibleMove[1]].center,
                                   radius=circleRadius)

    def render_pieces(self, screen, cellSize, boardPosition):
        '''Renders the chess pieces on to the chess board.'''

        for row in range(0, 8):
            for col in range(0, 8):
                currentPiece = self.logicalBoard.get_piece_array(row, col)

                destination = (-1, -1)
                if self.cellPieceToMove == (row, col):
                    destination = self.mousePos
                else:
                    destination = self.boardCells[row][col].topleft

                if currentPiece == "wP":
                    screen.blit(self.whitePawnImage, dest=destination)
                elif currentPiece == "wK":
                    screen.blit(self.whiteKingImage, dest=destination)
                elif currentPiece == "wR":
                    screen.blit(self.whiteRookImage, dest=destination)
                elif currentPiece == "wS":
                    screen.blit(self.whiteKnightImage, dest=destination)
                elif currentPiece == "wB":
                    screen.blit(self.whiteBishopImage, dest=destination)
                elif currentPiece == "wQ":
                    screen.blit(self.whiteQueenImage, dest=destination)

                elif currentPiece == "bP":
                    screen.blit(self.blackPawnImage, dest=destination)
                elif currentPiece == "bK":
                    screen.blit(self.blackKingImage, dest=destination)
                elif currentPiece == "bR":
                    screen.blit(self.blackRookImage, dest=destination)
                elif currentPiece == "bS":
                    screen.blit(self.blackKnightImage, dest=destination)
                elif currentPiece == "bB":
                    screen.blit(self.blackBishopImage, dest=destination)
                elif currentPiece == "bQ":
                    screen.blit(self.blackQueenImage, dest=destination)

    def render_board(self, screen):
        '''Renders the chess board on to the screen.'''

        for row in range(0, 8):
            for col in range(0, 8):
                if (row, col) == self.markedCell:
                    pygame.draw.rect(screen, self.markColor, self.boardCells[row][col])
                else:
                    pygame.draw.rect(screen, self.boardColor1 if (row + col) % 2 == 0 else self.boardColor2,
                                     self.boardCells[row][col])

    def render_text(self, screen, cellSize, marginSize, boardPosition):
        '''Renders the chess board numbers and letters on to the chess board.'''

        # numbers
        for row in range(0, 8):
            currentCell = self.boardCells[row][0]
            currentText = self.numberTexts[7 - row]
            textPos = (currentCell.left + 0.1 * currentCell.width,
                       currentCell.top + 0.1 * currentCell.height)
            screen.blit(currentText, dest=textPos, area=currentText.get_rect())

        # letters
        for col in range(0, 8):
            currentCell = self.boardCells[7][col]
            currentText = self.letterTexts[col]
            textPos = (currentCell.right - 0.2 * currentCell.width,
                       currentCell.bottom - 0.4 * currentCell.height)
            screen.blit(currentText, dest=textPos, area=currentText.get_rect())

    def cell_is_empty(self, row, col):
        return self.logicalBoard.get_piece_array(row, col) == self.logicalBoard.emptyPiece

    def move_piece(self, fromCell, toPosition):
        '''Moves the piece at the given cell to the given position.'''
        self.cellPieceToMove = fromCell
        self.mousePos = toPosition

    def get_cell_size(self):
        '''Returns the side length every board's cell.'''
        return self.boardCells[0][0].size[0]

class BoardInteractor:
    def __init__(self, boardRenderer):
        self.boardRenderer = boardRenderer
        self.leftMousePressed = False
        self.previousLeftMousePressed = False
        self.markedCellOnMove = None

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
            self.markedCellOnMove = markedCell

            # if that cell has a piece on it, remember that as being the piece
            # that should be moved.
            if not self.boardRenderer.cell_is_empty(markedCell[0], markedCell[1]):
                self.cellPieceToMove = markedCell
            else:
                return

        # stop moving the piece when the left mouse button is released and
        # put it to the current marked cell (the new location) if that move
        # is possible. Otherwise put the piece back to it's original location.
        elif self.on_left_mouse_released():
            markedCellOnMouseRelease = self.boardRenderer.markedCell
            if (
                    not self.boardRenderer.cell_is_empty(self.markedCellOnMove[0], self.markedCellOnMove[1]) and
                    markedCellOnMouseRelease in self.boardRenderer.logicalBoard.get_possible_moves(
                    self.markedCellOnMove)
            ):
                self.boardRenderer.logicalBoard.move_piece_array(self.markedCellOnMove, markedCellOnMouseRelease)
            else:
                self.boardRenderer.move_piece(self.cellPieceToMove,
                                              self.boardRenderer.boardCells[self.markedCellOnMove[0]][
                                                  self.markedCellOnMove[1]])
            self.cellPieceToMove = None

        # if there is a piece to move, move it to the position of the mouse cursor.
        if self.cellPieceToMove is not None:
            cellSize = self.boardRenderer.get_cell_size()
            destination = (mousePos[0] - (cellSize / 2), mousePos[1] - (cellSize / 2))
            self.boardRenderer.move_piece(self.cellPieceToMove, destination)

    def update_mouse_hover(self, mousePos):
        for row in range(0, 8):
            for col in range(0, 8):
                if self.boardRenderer.boardCells[row][col].collidepoint(mousePos):
                    self.boardRenderer.markedCell = (row, col)
                    return
        self.boardRenderer.markedCell = (-1, -1)

class Board:
    def __init__(self):
        self.logicalBoard = LogicalBoard()
        self.boardRenderer = BoardRenderer(self.logicalBoard)
        self.boardInteractor = BoardInteractor(self.boardRenderer)

    def update(self, screen):
        self.boardRenderer.update(screen)
        self.boardInteractor.update()

    def check_win_condition(self):
        return self.logicalBoard.game_has_finished()

    def render(self, screen):
        self.boardRenderer.render(screen)

    def move_array(self, fromLoc, toLoc):
        self.logicalBoard.move_piece(fromLoc, toLoc)
        return self.check_win_condition()

    def move_trad(self, fromLoc, toLoc):
        self.logicalBoard.move_piece(fromLoc, toLoc)
        return self.check_win_condition()

    def __repr__(self):
        return self.logicalBoard.__repr__()
