
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
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wS", "wB", "wQ", "wK", "wB", "wS", "wR"]
            ]
        else:
            if len(board) != 8 or len(board[0]) != 8:
                raise ValueError("Given board has incorrect dimensions. Must be 8x8.")
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
    
    def move_piece(self, fromLoc, toLoc):
        fromLocArray = self.traditional_to_array(fromLoc)
        toLocArray = self.traditional_to_array(toLoc)

        if (not self.validate_move(fromLocArray, toLocArray)):
            raise ValueError("Given move '" + fromLoc + " -> " + toLoc + "' is unvalid.")
        else:
            # move piece to new location
            self.board[toLocArray[0]][toLocArray[1]] = self.board[fromLocArray[0]][fromLocArray[1]]

            # remove piece from old location
            self.board[fromLocArray[0]][fromLocArray[1]] = self.emptyPiece
        
        return fromLoc + " -> " + toLoc

    def validate_move(self, fromLoc, toLoc):
        # Determine the type of piece that is about to be moved.
        pieceType = self.board[fromLoc[0]][fromLoc[1]][1]

        # For each type of piece delegate to a specific sub-method that checks move validity.
        if pieceType == "R": return self.validate_move_rook(fromLoc, toLoc)
        elif pieceType == "K": return self.validate_move_king(fromLoc, toLoc)
        elif pieceType == "S": return self.validate_move_knight(fromLoc, toLoc)
        elif pieceType == "B": return self.validate_move_bishop(fromLoc, toLoc)
        elif pieceType == "Q": return self.validate_move_queen(fromLoc, toLoc)
        elif pieceType == "P": return self.validate_move_pawn(fromLoc, toLoc)

    def validate_move_pawn(self, fromLoc, toLoc):
        # Black or white pawn?
        pawnColor = self.board[fromLoc[0]][fromLoc[1]][0]

        possibleLocations = []

        # black pawn
        if pawnColor == "b":
            # Is the pawn in it's initial location or has it already been moved?
            # 1 is the index of the row where all the black pawns start.
            if fromLoc[0] == 1:
                possibleLocations.append((fromLoc[0] + 1, fromLoc[1]))
                possibleLocations.append((fromLoc[0] + 2, fromLoc[1]))
            else:
                # No enemy piece in front
                if self.board[fromLoc[0] + 1][fromLoc[1]] == self.emptyPiece:
                    possibleLocations.append((fromLoc[0] + 1, fromLoc[1]))

                # Enemy pieces diagonally
                # Pawn hugs left wall
                if fromLoc[1] == 0:
                    if "w" in self.board[fromLoc[0] + 1][1]:
                        possibleLocations.append((fromLoc[0] + 1, 1))

                # Pawn hugs right wall
                elif fromLoc[1] == 7:
                    if "w" in self.board[fromLoc[0] + 1][6]:
                        possibleLocations.append((fromLoc[0] + 1, 6))

                # Pawn doesn't a wall
                else:
                    # left diagonal
                    if "w" in self.board[fromLoc[0] + 1][fromLoc[1] - 1]:
                        possibleLocations.append((fromLoc[0] + 1, fromLoc[1] - 1))
                    # right diagonal
                    if "w" in self.board[fromLoc[0] + 1][fromLoc[1] + 1]:
                        possibleLocations.append((fromLoc[0] + 1, fromLoc[1] + 1))

        # white pawn    
        else:
            # initial pos
            if fromLoc[0] == 6:
                possibleLocations.append((fromLoc[0] - 1, fromLoc[1]))
                possibleLocations.append((fromLoc[0] - 2, fromLoc[1]))
            else:
                # no piece in front
                if self.board[fromLoc[0] - 1][fromLoc[1]] == self.emptyPiece:
                    possibleLocations.append((fromLoc[0] - 1, fromLoc[1]))

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
                        possibleLocations.append((fromLoc[0] - 1, fromLoc[1] - 1))
                    # right diagonal
                    if "b" in self.board[fromLoc[0] - 1][fromLoc[1] + 1]:
                        possibleLocations.append((fromLoc[0] - 1, fromLoc[1] + 1))

        if toLoc in possibleLocations:
            return True
        return False
        
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
