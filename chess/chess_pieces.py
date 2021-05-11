# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import enum
from shared.pieces import Piece
from .chess_moves import Straight, Diagonal, L

class ChessPiece(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Pawn(ChessPiece):
    def __str__(self):
        return u'♟︎' if self.color == "black" else u'♙'

class Rook(ChessPiece):
    def __str__(self):
        return u'♜' if self.color == "black" else u'♖'

class Knight(ChessPiece):
    def __str__(self):
        return u'♞' if self.color == "black" else u'♘'

class Bishop(ChessPiece):
    def __str__(self):
        return u'♝' if self.color == "black" else u'♗'

class Queen(ChessPiece):
    def __str__(self):
        return u'♛' if self.color == "black" else u'♕'

class King(ChessPiece):
    def __str__(self):
        return u'♚' if self.color == "black" else u'♔'