
from Board import Board

board = Board(board=[
    ["bR", "bS", "bB", "bQ", "bK", "bB", "bS", "bR"],
    ["bP", "bP", "bP", "bP", "||", "bP", "bP", "bP"],
    ["||", "||", "||", "||", "||", "||", "||", "||",],
    ["||", "||", "||", "||", "bP", "||", "bP", "||",],
    ["||", "||", "||", "||", "||", "wP", "||", "||",],
    ["||", "||", "||", "||", "||", "||", "||", "||",],
    ["wP", "wP", "wP", "wP", "wP", "||", "wP", "wP"],
    ["wR", "wS", "wB", "wQ", "wK", "wB", "wS", "wR"]
])

print(board)

board.move_piece("f4", "e5")

print(board)