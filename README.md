Implementation of chess for CPSC 327 (Object Oriented Programming) at Yale by Christie Yu and Matt Udry.

## Project Description

In this project, we implemented checkers and chess in Python using object-oriented strategies. We used [usual English draught rules](https://en.wikipedia.org/wiki/English_draughts) except jumping is mandatory: if the player or bot can jump, they must. We also used [usual chess rules](https://www.chess.com/learn-how-to-play-chess). The checkers and chess boards are represented thus:

         Checkers                          Chess
    1 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼                1 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
    2 ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈                2 ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ 
    3 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼                3 ◻ ◼ ◻ ◼ ◻ ◼ ◻ ◼ 
    4 ◼ ◻ ◼ ◻ ◼ ◻ ◼ ◻                4 ◼ ◻ ◼ ◻ ◼ ◻ ◼ ◻ 
    5 ◻ ◼ ◻ ◼ ◻ ◼ ◻ ◼                5 ◻ ◼ ◻ ◼ ◻ ◼ ◻ ◼ 
    6 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆                6 ◼ ◻ ◼ ◻ ◼ ◻ ◼ ◻ 
    7 ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼                7 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 
    8 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆                8 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 
      a b c d e f g h                  a b c d e f g h
      
Where a '⚆' = pawn and a '⚇' = king in checkers; ♜ = rook, ♞ = knight, ♝ = bishop, ♛ = queen, ♚ = king, and ♟︎ = pawn in chess.

Once a user selects a piece to move by calling its coordinate (e.g: 'c3'), the program returns a list of moves that the user must choose from.

There are four kinds of players in the game: human (player submits moves), random (computer chooses a random move from the moveset, prioritizing jumps), greedy (computer chooses the move from the moveset with the most jumps, breaking ties randomly), and minimax# (where # is a number representing the depth) that plays with fixed-depth [minimax](https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm) without Alpha-Beta pruning.

The program also has move undo/redo functionality.

## Running the program

To run the program, write to the command line:

`python3 main.py [arg1] [arg2] [arg3] [arg4]`

* `arg1` should be `checkers` or `chess`; is `chess` by default; and represents whether the game played is checkers or chess.
* `arg2` should be `human`, `random` or `greedy`; is `human` by default; and represents the type of player that plays white.
* `arg3` should be `human`, `random` or `greedy`; is `human` by default; and represents the type of player that plays black.
* `arg4` should be `on` or `off`; is `off` by default; and represents whether the game offers undo/redo functionality.

For example, the input `python3 main.py` represents a chess game played by two humans without undo/redo functionality.

Meanwhile, the input `python3 main.py checkers greedy minimax3 on` represents a checkers game played by a random bot on white, a minimax bot with fixed-depth 3 on black, and undo/redo functionality.
