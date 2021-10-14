
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
'''

'''
b := black
w := white

R := Rook
K := Knight
B := Bishop
Q := Queen
P := Pawn
'''

class Board:
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
                ["bR", "bK", "bB", "bQ", "bK", "bB", "bK", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                [self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece, self.emptyPiece,],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wK", "wB", "wQ", "wK", "wB", "wK", "wR"]
            ]
        else:
            if len(board) != 8 or len(board[0] != 8):
                raise ValueError("Given board has incorrect dimensions. Must be 8x8.")
            else:
                self.board = board

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

    def validate_move(self, fromLoc, toLoc):
        # Determine the type of piece that is about to be moved.
        piece = self.board[fromLoc[0]][fromLoc[1]]

        # Determine the possible locations that piece can move to from it's current location.
        possibleLocations = []

        # Is the piece black or white
        # Black
        if piece[0] == "b":

            # Pawn
            if piece[1] == "P":
                # Is the pawn in it's initial location or has it already been moved?
                # 1 is the index of the row where all the black pawns start.
                if fromLoc[0] == 1:
                    possibleLocations.append((fromLoc[0] + 1, fromLoc[1]))
                    possibleLocations.append((fromLoc[0] + 2, fromLoc[1]))
                else:
                    pass
        # White
        """ else:
            pass """

        # Is the given location the piece is about to be moved to in these possible locations?
        if toLoc in possibleLocations: return True
        else: return False
        

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
