# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import random
import copy
import tkinter as tk
from tkinter import Frame, Button, OptionMenu

from checkers.checkers_board import CheckersBoard
from chess.chess_board import ChessBoard
from players import WhiteState, BlackState, PlayerMove
from shared.pieces import Piece

class GUI(Frame):
    def __init__(self):
        # undo-redo setup
        self.history = True
        self.move_history = []
        # board setup
        self.turn = 1
        self.board = ChessBoard()
        # strategy pattern setup
        self._choices = {
            "random": self._random_moves,
            "greedy": self._greedy_moves,
            "minimax": self._minimax_moves
        }
        # get randomized seed
        with open('seed.txt', 'r') as seed_f:
            seed_value = seed_f.read()
        random.seed(seed_value)
        # GUI ----- frames
        self._window = tk.Tk()
        self._top_frame = tk.Frame(self._window)
        self._top_frame.grid(row=0, column=0)
        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=1, column=0)
        self._controls_frame = tk.Frame(self._window)
        self._controls_frame.grid(row=1, column=1)
        self._window.title("Chess with Matt and Christie!!")
        label = tk.Label(self._top_frame, text="Welcome to chess with Matt and Christie!!")
        label.grid(row=0, column=0)
        # GUI ----- variables for widget storage
        self._button_list = {}
        self._selected_piece = None
        self._movepool = []
        self._move = None
        # GUI ----- labels
        self._instruction_label = tk.Label(self._controls_frame, text="")
        self._instruction_label.grid(row=0, column=0)
        self._move_label = tk.Label(self._controls_frame, text="", fg="green")
        self._move_label.grid(row=1, column=0)
        self._error_label = tk.Label(self._controls_frame, text="", fg="red")
        self._error_label.grid(row=2, column=0)
        self._turn_label = tk.Label(self._top_frame, text="Select players.", fg="blue")
        self._turn_label.grid(row=1, column=0)
        self._ask_players()

    def toggle_color(self):
        """Utilizes the player_state state machine to toggle between white and black player objects."""
        self.player_state.toggle_color()

    def _ask_players(self):
        """Presents opening screen asking for p1 and p2 player types."""
        def players_chosen():
            """Once "OK" button has been pressed, submit p1 and p2 player types and destroy interface."""
            self.white_state = WhiteState(self, p1.get())
            self.black_state = BlackState(self, p2.get())
            self.player_state = self.white_state
            self._update_moveset()
            p1_label.destroy()
            p1_menu.destroy()
            p2_label.destroy()
            p2_menu.destroy()
            button.destroy()
            self._initGUI()

        p1 = tk.StringVar()
        p1.set("human")
        p1_label = tk.Label(self._top_frame, text="Player on white", fg="green")
        p1_label.grid(row=2, column=0)
        p1_menu = OptionMenu(self._top_frame, p1, "human", "random", "greedy", "minimax")
        p1_menu.grid(row=3, column=0)
        p2 = tk.StringVar()
        p2.set("human")
        p2_label = tk.Label(self._top_frame, text="Player on black", fg="green")
        p2_label.grid(row=2, column=1)
        p2_menu = OptionMenu(self._top_frame, p2, "human", "random", "greedy", "minimax")
        p2_menu.grid(row=3, column=1)
        button = Button(self._top_frame, text="OK", command=players_chosen)
        button.grid(row=4, column=0)

    def _initGUI(self):
        """Create 64 board button widgets."""
        # populate labels
        turn_text = f"TURN " + str(self.turn) + ", CURRENT PLAYER: " + str(self.player_state).upper()
        self._turn_label.config(text=turn_text)
        self._instruction_label.config(text="Select a piece to move.")
        # create board
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "gray"
                text = self.board.board[i][j] if not isinstance(self.board.board[i][j], int) else ""
                coord = (i, j)
                # buttons call "piece_selected" function when clicked
                self._button_list[(i, j)] = Button(self._board_frame, text=text, height=3, width=6, highlightbackground=color, command=lambda coord=coord: self._piece_selected(coord))
                self._button_list[(i, j)].grid(row=i, column=j)
        # AI players
        if self.player_state.player == "random":
            move = self._random_moves()
            self._move_selected(move=move)
        elif self.player_state.player == "greedy":
            move = self._greedy_moves()
            self._move_selected(move=move)
        elif self.player_state.player == "minimax":
            pass

    def _new_turn(self):
        """Updates player info each turn."""
        # check victory conditions
        if self._check_victory_draw() == True:
            for coord in self._button_list:
                self._button_list[coord].destroy()
        else:
            # update game state
            self.turn += 1
            self.player_state.toggle_color()
            self._update_moveset()
            # update turn text
            turn_text = f"TURN " + str(self.turn) + ", CURRENT PLAYER: " + str(self.player_state).upper()
            self._turn_label.config(text=turn_text)
            # reset board colors
            for coord in self._button_list:
                row, col = coord
                color = "white" if (row + col) % 2 == 0 else "gray"
                text = str(self.board.board[row][col]) if not isinstance(self.board.board[row][col], int) else ""
                # set buttons to call "piece_selected" function again
                self._button_list[(row, col)].config(text=text, height=3, width=6, highlightbackground=color, command=lambda coord=coord: self._piece_selected(coord))
            # AI players
            if self.player_state.player == "random":
                move = self._random_moves()
                self._move_selected(move=move)
            elif self.player_state.player == "greedy":
                move = self._greedy_moves()
                self._move_selected(move=move)
            elif self.player_state.player == "minimax":
                pass

    def _piece_selected(self, coords):
        """Once a piece has been selected by a human player, highlight possible moves and make buttons re-clickable for move selection."""
        self._selected_piece = coords
        row, col = coords
        # error checking once player has clicked a piece
        if isinstance(self.board.board[row][col], Piece) == False:
            self._error_label.config(text="No piece at that location")
        if self.board.board[row][col].color != self.player_state.color:
            self._error_label.config(text="That is not your piece")
        possible_moves = [move for move in self.player_state.moves if move.beginning == (row, col)]
        if len(possible_moves) == 0 or self.board.check_movability(possible_moves, self.player_state.moves) == False:
            self._error_label.config(text="That piece cannot move")
        else:
            # highlight selected piece and show possible moves
            self._button_list[(row, col)].config(highlightbackground="blue")
            for move in possible_moves:
                self._button_list[(move.end[0], move.end[1])].config(highlightbackground="yellow")
            self._instruction_label.config(text="Select a move.")
            self._movepool = possible_moves
            # set buttons to call "move_selected" function
            for coord in self._button_list:
                self._button_list.get(coord).config(command=lambda coord=coord: self._move_selected(coord))
    
    def _move_selected(self, coords=None, move=None):
        """Once human player has selected move, execute it and reset to a new turn."""
        # execute move
        if move:
            self._move = move
        else:
            for move in self._movepool:
                if move.beginning == self._selected_piece and move.end == coords:
                    self._move = move
        text = str(self._move) + " was selected."
        self._move_label.config(text=text)
        self.board.execute_move(self._move)
        # for undo-redo
        self.move_history.append(PlayerMove(self.turn, self.player_state, self._move, copy.deepcopy(self.board)))
        self.board.print_board()
        # new turn
        self._new_turn()

    def _random_moves(self):
        """Uses the player's moveset to select a random move, prioritizing jumps."""
        # choose a random move from moveset and prioritizes jumps
        move = None
        while True:
            move = random.choice(self.player_state.moves)
            if self.board.check_movability([move], self.player_state.moves) == True:
                break
        self.move_history.append(PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board)))
        return move

    def _greedy_moves(self):
        """Goes through possible moves and chooses randomly from the greediest moveset."""
        greedy_move_choices = self.board.return_greedy_moves(self.player_state.moves)
        # choose a random move from list
        move = random.choice(greedy_move_choices)
        self.move_history.append(PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board)))
        return move

    def _minimax_moves(self):
        pass

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
            text = f"{self.player_state} has won"
            self._error_label.config(text=text, highlightbackground="yellow")
            return True
        # draw conditions (no moves left or 50 turns without capturing)
        elif len(self.player_state.moves) == 0:
            self._error_label.config(text="draw", highlightbackground="yellow")
            return True
        if self.board.draw_counter >= 50:
            self._error_label.config(text="draw", highlightbackground="yellow")
            return True
        return False

    def run(self):
        """Prints board, displays moves, asks player for move, executes move, updates the board after each turn, and checks for victory conditions."""
        self._window.mainloop()

if __name__ == "__main__":
    GUI().run()