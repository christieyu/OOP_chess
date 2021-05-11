# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import enum
from .moves import Move

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.location = location

    def _get_board(self, board, coords, return_coord=False):
        """Fetches obj or value at a given board location (if it exists)"""
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return None
        if return_coord:
            return (coords[0], coords[1])               # return the coordinates at board location
        return board[coords[0]][coords[1]]              # return the value at board location    