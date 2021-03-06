# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

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

    def _get_adjacent(self, board, start: tuple, direction: tuple, return_coord=False):
        """Fetches obj or value at location in a given starting point and direction (if it exists)"""
        return self._get_board(board, (start[0] + direction[0], start[1] + direction[1]), return_coord)