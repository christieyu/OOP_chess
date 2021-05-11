# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.board import Board
from .chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
from .chess_moves import ChessMove

class ChessBoard(Board):
    def __init__(self, p1="human", p2="human", history="off"):
        super().__init__()
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""
        self.board = [[Rook("black", (0, 0)),   Knight("black", (0, 1)),    Bishop("black", (0, 2)),    Queen("black", (0, 3)),     King("black", (0, 4)),      Bishop("black", (0, 5)),    Knight("black", (0, 6)),    Rook("black", (0, 7))],
                      [Pawn("black", (1, 0)),   Pawn("black", (1, 1)),      Pawn("black", (1, 2)),      Pawn("black", (1, 3)),      Pawn("black", (1, 4)),      Pawn("black", (1, 5)),      Pawn("black", (1, 6)),      Pawn("black", (1, 7))],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [Pawn("white", (1, 0)),   Pawn("white", (1, 1)),      Pawn("white", (1, 2)),      Pawn("white", (1, 3)),      Pawn("white", (1, 4)),      Pawn("white", (1, 5)),      Pawn("white", (1, 6)),      Pawn("white", (1, 7))],
                      [Rook("white", (0, 0)),   Knight("white", (0, 1)),    Bishop("white", (0, 2)),    Queen("white", (0, 3)),     King("white", (0, 4)),      Bishop("white", (0, 5)),    Knight("white", (0, 6)),    Rook("white", (0, 7))]]
        self.draw_counter = 0

    def check_movability(self, possible_moves, total_moves):
        return True

    def calculate_moves(self, position, already_coords=False):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_checker_coord(position) if already_coords == False else position
        piece = self.board[row][col]
        pass

    def execute_move(self, move):
        """Given the user's selected move, executes it and updates piece position."""
        b = move.beginning
        e = move.end
        pass