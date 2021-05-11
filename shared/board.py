# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from .pieces import Piece
from .moves import Move

class Board:
    def __init__(self, p1="human", p2="human", history="off"):
        self.draw_counter = 0

    def print_board(self):
        """Prints board matrix as unicode GUI."""
        for i, row in enumerate(self.board):
            print(i + 1, end=" ")
            for j in row:
                print(u'◼', end=" ") if j == 0 else print(u'◻', end=" ") if j == 1 else print(j, end=" ")
            print("")
        print("  a b c d e f g h")
    
    def _convert_to_coord(self, coord):
        """Given a coord (e.g: 'b4'), returns numerical coordinates (e.g: 4, 1)."""
        col = coord[:1]
        row = coord[1:]
        col = ord(col) - 96
        row = int(row)
        return (row - 1, col - 1)