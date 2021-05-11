# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

class Move:
    def __init__(self, beginning, end, elim=None):
        """Initializes move and checks that its ending location is within bounds."""
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7:
            self.end = None
        else:
            self.beginning = beginning
            self.end = end

    def _convert_to_letter(self, coord):
        """Given numerical coordinates (e.g: (4, 1)), returns coord (e.g: 'b4')."""
        row, col = coord
        return chr(col + 96 + 1) + str(row + 1)