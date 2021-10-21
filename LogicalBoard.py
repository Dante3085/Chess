'''
- Schachbrettklasse
- Figuren auf Brett
- Züge von Figuren
- Brett als String repräsentieren
- Brett als Bild repräsentieren
- Siegbedingung
- Game-Loop
- Startkonfigurationen (Normal, Beliebig, ...)
- Fehler abfangen (Illegale Züge etc.). Zum Beispiel "Bauer bewegt sich zurück" 
  (Erstmal nur, sodass alles funktioniert ohne Fehler abfangen)
- Bauern werden zu Königinnen, wenn sie in der ersten Reihe des Feindes ankommen.
'''

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


class LogicalBoard:
    def __init__(self, board=None) -> None:
        self.letterToColumn = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }

        # The empty piece represents the absence of any of the real pieces on a location.
        self.emptyPiece = "||"

        if board == None:
            self.board = [
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
                raise ValueError(
                    "Given board has incorrect dimensions. Must be 8x8.")
            else:
                self.board = board

                # Make sure that the self.emptyPiece character is used.
                """ for row in range(2, 6):
                    for col in range(0, 8):
                        self.board[row][col] = self.emptyPiece """

    def get_piece(self, pieceLoc):
        loc = self.traditional_to_array(pieceLoc)
        return self.get_piece_array(loc[0], loc[1])

    def get_piece_array(self, row, col):
        return self.board[row][col]

    def traditional_to_array(self, trad):
        '''Converts the traditional chess notation (e.g.: e8) to an array indexing notation (e.g.: e8 -> row=0, col=4)'''
        # 8 - i
        # 8 is the index of the last row on the board if you count 1 to 8.
        col = self.letterToColumn[trad[0]]
        row = 8 - int(trad[1])
        return (row, col)

    def move_piece_array(self, fromLocArray, toLocArray):
        if (not self.validate_move(fromLocArray, toLocArray)):
            raise ValueError("Given move '" + str(fromLocArray) +
                             " -> " + str(toLocArray) + "' is unvalid.")
        else:
            # move piece to new location
            self.board[toLocArray[0]][toLocArray[1]
            ] = self.board[fromLocArray[0]][fromLocArray[1]]

            # remove piece from old location
            self.board[fromLocArray[0]][fromLocArray[1]] = self.emptyPiece

        return str(fromLocArray) + " -> " + str(toLocArray)

    def move_piece_trad(self, fromLoc, toLoc):
        fromLocArray = self.traditional_to_array(fromLoc)
        toLocArray = self.traditional_to_array(toLoc)

        return self.move_piece_array(fromLoc, toLoc)

    def validate_move(self, fromLoc, toLoc):
        # Determine the type of piece that is about to be moved.
        pieceType = self.board[fromLoc[0]][fromLoc[1]][1]

        # For each type of piece delegate to a specific sub-method that checks move validity.
        if pieceType == "R":
            return toLoc in self.get_possible_moves_rook(fromLoc)
        elif pieceType == "K":
            return toLoc in self.get_possible_moves_king(fromLoc)
        elif pieceType == "S":
            return toLoc in self.get_possible_moves_knight(fromLoc)
        elif pieceType == "B":
            return toLoc in self.get_possible_moves_bishop(fromLoc)
        elif pieceType == "Q":
            return toLoc in self.get_possible_moves_queen(fromLoc)
        elif pieceType == "P":
            return toLoc in self.get_possible_moves_pawn(fromLoc)

    def get_possible_moves(self, position):
        piece = self.board[position[0]][position[1]]
        if "R" in piece:
            return self.get_possible_moves_rook(position)
        elif "K" in piece:
            return self.get_possible_moves_king(position)
        elif "S" in piece:
            return self.get_possible_moves_knight(position)
        elif "B" in piece:
            return self.get_possible_moves_bishop(position)
        elif "Q" in piece:
            return self.get_possible_moves_queen(position)
        elif "P" in piece:
            return self.get_possible_moves_pawn(position)

    def get_possible_moves_rook(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        rookColor = self.board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # up
        for i in range(fromRow - 1, -1, -1):
            newLocation = (i, fromCol)
            possibleLocations.append(newLocation)
            if self.board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # down
        for i in range(fromRow + 1, 8):
            newLocation = (i, fromCol)
            possibleLocations.append(newLocation)
            if self.board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # right
        for i in range(fromCol + 1, 8):
            newLocation = (fromRow, i)
            possibleLocations.append(newLocation)
            if self.board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        # left
        for i in range(fromCol - 1, -1, -1):
            newLocation = (fromRow, i)
            possibleLocations.append(newLocation)
            if self.board[newLocation[0]][newLocation[1]] != self.emptyPiece:
                break

        return self.remove_not_on_board_and_friendly(possibleLocations, rookColor)

    def get_possible_moves_king(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        kingColor = self.board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = [
            (fromRow - 1, fromCol),
            (fromRow, fromCol + 1),
            (fromRow + 1, fromCol),
            (fromRow, fromCol - 1)
        ]

        return self.remove_not_on_board_and_friendly(possibleLocations, kingColor)

    def get_possible_moves_bishop(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        bishopColor = self.board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # top left
        row = fromRow - 1
        col = fromCol - 1
        while row >= 0 and col >= 0:
            possibleLocations.append((row, col))

            # Break the loop if we encountered a piece
            if self.board[row][col] != self.emptyPiece:
                break

            row -= 1
            col -= 1

        # top right
        row = fromRow - 1
        col = fromCol + 1
        while row >= 0 and col <= 7:
            possibleLocations.append((row, col))

            if self.board[row][col] != self.emptyPiece:
                break

            row -= 1
            col += 1

        # bottom right
        row = fromRow + 1
        col = fromCol + 1
        while row <= 7 and col <= 7:
            possibleLocations.append((row, col))

            if self.board[row][col] != self.emptyPiece:
                break

            row += 1
            col += 1

        # bottom left
        row = fromRow + 1
        col = fromCol - 1
        while row <= 7 and col >= 0:
            possibleLocations.append((row, col))

            if self.board[row][col] != self.emptyPiece:
                break

            row += 1
            col -= 1

        return self.remove_not_on_board_and_friendly(possibleLocations, bishopColor)

    def get_possible_moves_queen(self, fromLoc):
        return self.get_possible_moves_bishop(fromLoc) + \
               self.get_possible_moves_rook(fromLoc)

    def get_possible_moves_knight(self, fromLoc):
        fromRow = fromLoc[0]
        fromCol = fromLoc[1]
        knightColor = self.board[fromLoc[0]][fromLoc[1]][0]

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

        return self.remove_not_on_board_and_friendly(possibleLocations, knightColor)

    def get_possible_moves_pawn(self, fromLoc):
        # Black or white pawn?
        pawnColor = self.board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # black pawn
        if pawnColor == "b":
            # No enemy piece in front
            if self.board[fromLoc[0] + 1][fromLoc[1]] == self.emptyPiece:
                possibleLocations.append((fromLoc[0] + 1, fromLoc[1]))

                # Is the pawn in it's initial location or has it already been moved?
                # 1 is the index of the row where all the black pawns start.
                if fromLoc[0] == 1:
                    possibleLocations.append((fromLoc[0] + 2, fromLoc[1]))

            # Enemy pieces diagonally
            # Pawn hugs left wall
            if fromLoc[1] == 0:
                if "w" in self.board[fromLoc[0] + 1][1]:
                    possibleLocations.append((fromLoc[0] + 1, 1))

            # Pawn hugs right wall
            elif fromLoc[1] == 7:
                if "w" in self.board[fromLoc[0] + 1][6]:
                    possibleLocations.append((fromLoc[0] + 1, 6))

            # Pawn doesn't hug a wall
            else:
                # left diagonal
                if "w" in self.board[fromLoc[0] + 1][fromLoc[1] - 1]:
                    possibleLocations.append(
                        (fromLoc[0] + 1, fromLoc[1] - 1))
                # right diagonal
                if "w" in self.board[fromLoc[0] + 1][fromLoc[1] + 1]:
                    possibleLocations.append(
                        (fromLoc[0] + 1, fromLoc[1] + 1))

        # white pawn
        else:
            # no piece in front
            if self.board[fromLoc[0] - 1][fromLoc[1]] == self.emptyPiece:
                possibleLocations.append((fromLoc[0] - 1, fromLoc[1]))

                # initial pos
                if fromLoc[0] == 6:
                    possibleLocations.append((fromLoc[0] - 2, fromLoc[1]))

            # enemy pieces diagonally
            # hugs left wall
            if fromLoc[1] == 0:
                if "b" in self.board[fromLoc[0] - 1][1]:
                    possibleLocations.append((fromLoc[0] - 1, 1))

            # hugs right wall
            elif fromLoc[1] == 7:
                if "b" in self.board[fromLoc[0] - 1][6]:
                    possibleLocations.append((fromLoc[0] - 1, 6))

            # doesnt hug wall
            else:
                # left diagonal
                if "b" in self.board[fromLoc[0] - 1][fromLoc[1] - 1]:
                    possibleLocations.append(
                        (fromLoc[0] - 1, fromLoc[1] - 1))
                # right diagonal
                if "b" in self.board[fromLoc[0] - 1][fromLoc[1] + 1]:
                    possibleLocations.append(
                        (fromLoc[0] - 1, fromLoc[1] + 1))

        return possibleLocations

    def remove_not_on_board_and_friendly(self, possibleLocations, pieceColor):
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
                    pieceColor == "w" and "w" in self.board[location[0]][location[1]] or
                    pieceColor == "b" and "b" in self.board[location[0]][location[1]]
                 ):
                locationsToRemove.append(location)

        finalLocations = deepcopy(possibleLocations)
        for location in locationsToRemove:
            finalLocations.remove(location)

        return finalLocations

    def __repr__(self) -> str:
        boardStr = ""
        rowIndex = 8

        for row in self.board:
            boardStr += str(rowIndex) + " "
            rowIndex -= 1
            for piece in row:
                boardStr += piece + " "
            boardStr += "\n"

        boardStr += "  a  b  c  d  e  f  g  h"

        return boardStr
