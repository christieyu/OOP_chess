# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 5

import sys
import random
import copy
from checkers.checkers_board import CheckersBoard
from chess.chess_board import ChessBoard
from players import WhiteState, BlackState, PlayerMove
from shared.pieces import Piece

class CLI:
    def __init__(self):
        # state pattern setup
        self.white_state = WhiteState(self, sys.argv[2] if len(sys.argv) > 2 else "human")
        self.black_state = BlackState(self, sys.argv[3] if len(sys.argv) > 3 else "human")
        self.player_state = self.white_state
        # undo-redo setup
        self.history = True if len(sys.argv) > 4 and sys.argv[4] == "on" else False
        self.move_history = []
        # board setup
        self.turn = 1
        self.board = CheckersBoard() if len(sys.argv) > 1 and sys.argv[1] == "checkers" else ChessBoard()
        self._update_moveset()
        # strategy pattern setup
        self._choices = {
            "human": self._human_moves,
            "random": self._random_moves,
            "greedy": self._greedy_moves,
            "minimax": self._minimax_moves
        }
        # get randomized seed
        with open('seed.txt', 'r') as seed_f:
            seed_value = seed_f.read()
        random.seed(seed_value)

    def toggle_color(self):
        """Utilizes the player_state state machine to toggle between white and black player objects."""
        self.player_state.toggle_color()

    def _human_moves(self):
        """If player is human, prints a piece's possible moves and requests selection."""
        while True:
            position = input("Select a piece to move\n")
            row, col = self.board._convert_to_coord(position)
            # check if no piece at position
            if isinstance(self.board.board[row][col], Piece) == False:
                print("No piece at that location")
                continue
            # check if player's piece
            if self.board.board[row][col].color != self.player_state.color:
                print("That is not your piece")
                continue
            # check if no possible moves or possible jumps not selected
            possible_moves = [move for move in self.player_state.moves if move.beginning == (row, col)]
            if len(possible_moves) == 0 or self.board.check_movability(possible_moves, self.player_state.moves) == False:
                print("That piece cannot move")
                continue
            # otherwise move is valid
            else:
                break
        for i, move in enumerate(possible_moves):
            print(f"{i}: {move}")
        choice = input("Select a move by entering the corresponding index\n")
        # move_obj = possible_moves[int(choice)]
        move = PlayerMove(self.turn, self.player_state, possible_moves[int(choice)], copy.deepcopy(self.board))
        self.move_history.append(move)
        return move

    def _random_moves(self):
        """Uses the player's moveset to select a random move, prioritizing jumps."""
        # choose a random move from moveset and prioritizes jumps
        move = None
        while True:
            move = random.choice(self.player_state.moves)
            if self.board.check_movability([move], self.player_state.moves) == True:
                break
        print(move)
        move = PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board))
        self.move_history.append(move)
        return move

    def _greedy_moves(self):
        """Goes through possible moves and chooses randomly from the greediest moveset."""
        greedy_move_choices = self.board.return_greedy_moves(self.player_state.moves)
        # choose a random move from list
        move = random.choice(greedy_move_choices)
        print(move)
        move = PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board))
        self.move_history.append(move)
        return move

    def _minimax_moves(self):
        # return a move given the player state!
        move = self._minimax_search(self.board, self.player_state.depth, float('-inf'), float('inf'), True)[0]
        move = PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board))
        self.move_history.append(move)
        return move

    # inspired by https://stackoverflow.com/questions/64644532/minimax-algorithm-in-python-using-tic-tac-toe
    def _minimax_search(self, board, depth, alpha, beta, maximizing_player):
        """Does recursive search for minimax. Node is a board, minmax is a bool where True=calculate max for this node, 
        False=calculate min. Returns a tuple of (Move, score) where score is an int."""
        if depth == 0 or board.check_win(self.player_state):
            return None, self._minimax_evaluate(self.player_state, board)

        children = self.player_state.moves
        best_move = children[0]
        
        if maximizing_player:
            max_eval = float('-inf')       
            for child in children:
                board_copy = copy.deepcopy(board)
                board_copy.player_state = self.black_state
                current_eval = self._minimax_search(board_copy, int(depth) - 1, alpha, beta, False)[1]
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = child
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = float('inf')
            for child in children:
                board_copy = copy.deepcopy(board)
                board_copy.player_state = self.white_state
                current_eval = self._minimax_search(board_copy, int(depth) - 1, alpha, beta, True)[1]
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = child
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def _minimax_evaluate(self, player_state, board):
        """Evaluates score of given board for given player_state. Returns an int or +inf/-inf.
        Note: All of player_state and board's attributes must be updated before using."""
        # check if this board has a winner
        black_win = board.check_win(self.black_state)
        white_win = board.check_win(self.white_state)
        if white_win or black_win:
            if (player_state.color == "white" and white_win) or (player_state.color == "black" and black_win):
                return float('inf')                     # winning board for this player_state
            return float('-inf')                        # losing board for this player_state
        # check if this board has a draw
        if len(player_state.moves) == 0 or board.draw_counter >= 50:
            return 0
        # if neither, calculate the score for this player_state
        black_total = 0
        white_total = 0
        for row in self.board.board:
            for tile in row:
                if isinstance(tile, Piece):
                    if tile.color == "white":
                        white_total += tile.value
                    else:
                        black_total += tile.value
        if player_state.color == "white":
            return white_total - black_total
        else:
            return black_total - white_total

    def _update_moveset(self):
        """Collects all possible moves of the current player."""
        total_moves = []
        # checks whether win conditions are met
        self.player_state.win_met = self.board.check_win(self.player_state)
        # checks whole board for piece matching player's color
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                if isinstance(self.board.board[row][col], Piece) and self.board.board[row][col].color == self.player_state.color:
                    # update moveset
                    possible_moves = self.board.calculate_moves((row, col), True)
                    if len(possible_moves) > 0:
                        for move in possible_moves:
                            total_moves.append(move)
        self.player_state.moves = total_moves

    def _new_turn(self):
        """Updates player info each turn."""
        self.turn += 1
        self.player_state.toggle_color()
        self._update_moveset()

    def _do_history(self):
        """Presents undo/redo/next options at beginning of turn. Returns False if history is disable or "next"
        is selected, otherwise returns True (skipping usual move operations for undo/redo)"""
        if not self.history:
            return False
        op = input("undo, redo, or next\n")
        try:
            if op == "undo":
                self.turn -= 1
                last_move = self.move_history[self.turn - 1]
                self.board = copy.deepcopy(last_move.board_state)
                self.player_state = last_move.player_state
                return True
            elif op == "redo":
                next_move = self.move_history[self.turn - 1]
                next_move.execute(self.board)
                self.turn += 1
                self.player_state.toggle_color()
                return True
        except IndexError:
            return True                                                   # if undo/redo unavailable, don't do anything
        self.move_history = self.move_history[:self.turn-1]               # if new history branch, cut off old paths
        return False

    def _check_victory_draw(self):
        """Checks win conditions and changes current player's turn."""
        # victory conditions (no pieces left for checkers or no king left for chess)
        if self.player_state.win_met == True:
            self.player_state.toggle_color()
            print(f"{self.player_state} has won")
            sys.exit(0)
        # draw conditions (no moves left or 50 turns without capturing)
        elif len(self.player_state.moves) == 0:
            print("draw")
            sys.exit(0)
        if self.board.draw_counter >= 50:
            print("draw")
            sys.exit(0)

    def run(self):
        """Prints board, displays moves, asks player for move, executes move, updates the board after each turn, and checks for victory conditions."""
        while True:
            self.board.print_board()
            print(f"Turn: {self.turn}, {self.player_state}")
            self._check_victory_draw()
            if self._do_history():
                continue
            move = self._choices.get(self.player_state.player)()        # strategy pattern caller
            move.execute(self.board)
            self._new_turn()