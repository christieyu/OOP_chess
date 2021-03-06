# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.pieces import Piece
from .chess_moves import ChessMove

class ChessPiece(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_moves(self, board):
        possible_moves = []
        for direction in self.directions:
            cursor = self.location
            while self._get_adjacent(board, cursor, direction) in [0, 1]:
                adj_coord = self._get_adjacent(board, cursor, direction, True)
                possible_moves.append(ChessMove(self.location, adj_coord))
                if self.infinite == False:
                    break
                cursor = adj_coord
            if isinstance(self._get_adjacent(board, cursor, direction), ChessPiece) and self._get_adjacent(board, cursor, direction).color != self.color:
                adj_coord = self._get_adjacent(board, cursor, direction, True)
                move = ChessMove(self.location, adj_coord)
                move.captured = self._get_adjacent(board, cursor, direction)
                possible_moves.append(move)
        return possible_moves

class Pawn(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "pawn"
        if self.color == "black":
            self.directions = [(1, 0)]
            self.directions_first = [(2, 0)]
            self.directions_capture = [(1, 1), (1, -1)]
        else:
            self.directions = [(-1, 0)]
            self.directions_first = [(-2, 0)]
            self.directions_capture = [(-1, 1), (-1, -1)]
        self.already_moved = False
        self.infinite = False
        self.value = 1

    def calculate_moves(self, board):
        possible_moves = []
        # regular pawn moves
        for direction in self.directions:
            if self._get_adjacent(board, self.location, direction) in [0, 1]:
                adj_coord = self._get_adjacent(board, self.location, direction, True)
                possible_moves.append(ChessMove(self.location, adj_coord))
        # opening two-step pawn move
        for direction in self.directions_first:
            if self._get_adjacent(board, self.location, direction) in [0, 1] and self.already_moved == False:
                adj_coord = self._get_adjacent(board, self.location, direction, True)
                possible_moves.append(ChessMove(self.location, adj_coord))
        # diagonal capture
        for direction in self.directions_capture:
            if isinstance(self._get_adjacent(board, self.location, direction), ChessPiece) and self._get_adjacent(board, self.location, direction).color != self.color:
                adj_coord = self._get_adjacent(board, self.location, direction, True)
                move = ChessMove(self.location, adj_coord)
                move.captured = self._get_adjacent(board, self.location, direction)
                possible_moves.append(move)
        return possible_moves

    def __str__(self):
        return u'??????' if self.color == "black" else u'???'

class Rook(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "rook"
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.infinite = True
        self.value = 5

    def __str__(self):
        return u'???' if self.color == "black" else u'???'

class Knight(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "knight"
        self.directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.infinite = False
        self.value = 3

    def __str__(self):
        return u'???' if self.color == "black" else u'???'

class Bishop(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "bishop"
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.infinite = True
        self.value = 3

    def __str__(self):
        return u'???' if self.color == "black" else u'???'

class Queen(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "queen"
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.infinite = True
        self.value = 9

    def __str__(self):
        return u'???' if self.color == "black" else u'???'

class King(ChessPiece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "king"
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.infinite = False
        self.value = 100

    def __str__(self):
        return u'???' if self.color == "black" else u'???'