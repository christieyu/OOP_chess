# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.board import Board
from .chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
from .chess_moves import ChessMove

class ChessBoard(Board):
    def __init__(self):
        super().__init__()
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""
        self.board = [[Rook("black", (0, 0)),   Knight("black", (0, 1)),    Bishop("black", (0, 2)),    Queen("black", (0, 3)),     King("black", (0, 4)),      Bishop("black", (0, 5)),    Knight("black", (0, 6)),    Rook("black", (0, 7))],
                      [Pawn("black", (1, 0)),   Pawn("black", (1, 1)),      Pawn("black", (1, 2)),      Pawn("black", (1, 3)),      Pawn("black", (1, 4)),      Pawn("black", (1, 5)),      Pawn("black", (1, 6)),      Pawn("black", (1, 7))],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [Pawn("white", (6, 0)),   Pawn("white", (6, 1)),      Pawn("white", (6, 2)),      Pawn("white", (6, 3)),      Pawn("white", (6, 4)),      Pawn("white", (6, 5)),      Pawn("white", (6, 6)),      Pawn("white", (6, 7))],
                      [Rook("white", (7, 0)),   Knight("white", (7, 1)),    Bishop("white", (7, 2)),    Queen("white", (7, 3)),     King("white", (7, 4)),      Bishop("white", (7, 5)),    Knight("white", (7, 6)),    Rook("white", (7, 7))]]
        self.blank_board = [[1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1]]
        self.draw_counter = 0

    def calculate_moves(self, position, already_coords=False):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_to_coord(position) if already_coords == False else position
        piece = self.board[row][col]
        return piece.calculate_moves(self.board)

    def execute_move(self, move):
        """Given the user's selected move, executes it and updates piece position."""
        b = move.beginning
        e = move.end
        # mark that the pawn can no longer do two-step opening
        if isinstance(self.board[b[0]][b[1]], Pawn):
            self.board[b[0]][b[1]].already_moved = True
        # execute move
        self.board[e[0]][e[1]] = self.board[b[0]][b[1]]                 # new territory, conquered!!
        self.board[b[0]][b[1]] = self.blank_board[b[0]][b[1]]           # deserted land left in the wake of battle
        self.board[e[0]][e[1]].location = e                             # update the piece instance's location attribute