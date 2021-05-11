# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.board import Board
from .checkers_pieces import CheckersPiece, Pawn, King
from .checkers_moves import CheckersMove, Simple, Jump

class CheckersBoard(Board):
    def __init__(self, p1="human", p2="human", history="off"):
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""
        super().__init__()
        self.board = [[Pawn("black", (0, 0)), 0, Pawn("black", (0, 2)), 0, Pawn("black", (0, 4)), 0, Pawn("black", (0, 6)), 0],
                      [0, Pawn("black", (1, 1)), 0, Pawn("black", (1, 3)), 0, Pawn("black", (1, 5)), 0, Pawn("black", (1, 7))],
                      [Pawn("black", (2, 0)), 0, Pawn("black", (2, 2)), 0, Pawn("black", (2, 4)), 0, Pawn("black", (2, 6)), 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, Pawn("white", (5, 1)), 0, Pawn("white", (5, 3)), 0, Pawn("white", (5, 5)), 0, Pawn("white", (5, 7))],
                      [Pawn("white", (6, 0)), 0, Pawn("white", (6, 2)), 0, Pawn("white", (6, 4)), 0, Pawn("white", (6, 6)), 0],
                      [0, Pawn("white", (7, 1)), 0, Pawn("white", (7, 3)), 0, Pawn("white", (7, 5)), 0, Pawn("white", (7, 7))]]

    def check_movability(self, possible_moves, total_moves):
        """For checkers, if there are still jumps on the board, you cannot make a simple move."""
        if isinstance(possible_moves[0], Simple) and True in [isinstance(move, Jump) for move in total_moves]:
            return False
        return True

    def return_greedy_moves(self, total_moves):
        greedy_move_length = -1
        greedy_move_choices = []
        for move in total_moves:
            if len(move.eliminated) > greedy_move_length:   # if more elims than previously, reset list
                greedy_move_length = len(move.eliminated)
                greedy_move_choices = [move]
            elif len(move.eliminated) == greedy_move_length:
                greedy_move_choices.append(move)            # otherwise append to list
        return greedy_move_choices

    def calculate_moves(self, position, already_coords=False):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_to_coord(position) if already_coords == False else position
        piece = self.board[row][col]
        moves = piece.calculate_jump_moves(self.board)                      # If there are jump moves, we must do them!
        if not moves:
            return piece.calculate_simple_moves(self.board)                 # if no jump moves, then return simple moves
        return moves

    def execute_move(self, move):
        """Given the user's selected move, executes it and updates piece position."""
        b = move.beginning
        e = move.end
        self.board[e[0]][e[1]] = self.board[b[0]][b[1]]     # new territory, conquered!!
        self.board[b[0]][b[1]] = 1                          # deserted land left in the wake of battle
        self.board[e[0]][e[1]].location = e                 # update the piece instance's location attribute

        if isinstance(move, Jump):
            for piece in move.eliminated:                   # removed jumped pieces
                row, col = piece.location
                self.board[row][col] = 1
            self.draw_counter = 0
        else:
            self.draw_counter += 1

        self._check_king(self.board[e[0]][e[1]])

    def _check_king(self, piece):
        """If a pawn has reached the end of the board, promote it to king."""
        if (piece.location[0] == 0 and piece.color == "white") or (piece.location[0] == 7 and piece.color == "black"):
            self.board[piece.location[0]][piece.location[1]] = King(piece.color, piece.location)

    def check_win(self, player_state):
        # checks whole board for piece matching player's color
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if isinstance(self.board[row][col], CheckersPiece) and self.board[row][col].color == player_state.color:
                    return False
        return True