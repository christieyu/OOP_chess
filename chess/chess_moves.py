# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.moves import Move

class ChessMove(Move):
    pass

class OneStep(ChessMove):
    """For pawns, kings. Moves the piece one step in some direction."""
    pass

class TwoStep(ChessMove):
    """For opening pawns. Moves the piece two steps in forward direction."""
    pass

class Straight(ChessMove):
    """For rooks, queens. Moves the piece in some direction up to as far as allowed."""
    pass

class Diagonal(ChessMove):
    """For bishops, queens. Moves the piece in some direction up to as far as allowed."""
    pass

class L(ChessMove):
    """For knights. Moves the piece in an L-shape, allowing jumps over other pieces."""
    pass