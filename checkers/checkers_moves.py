# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.moves import Move

class CheckersMove(Move):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Simple(CheckersMove):
    def __init__(self, *args, **kwargs):
        """Initializes simple move."""
        super().__init__(*args, **kwargs)
        self.type = "simple"
        self.eliminated = []

    def __str__(self):
        beginning = self._convert_to_letter(self.beginning)
        end = self._convert_to_letter(self.end)
        return f"basic move: {beginning}->{end}"

class Jump(CheckersMove):
    def __init__(self, beginning, end, elim):
        """Initializes jump move and creates location archive."""
        super().__init__(beginning, end)
        self.type = "jump"
        self.eliminated = elim if isinstance(elim, list) else [elim]        # contains list of eliminated enemy piece objects

    def __str__(self):
        beginning = self._convert_to_letter(self.beginning)
        end = self._convert_to_letter(self.end)
        captured = ", ".join([self._convert_to_letter(piece.location) for piece in self.eliminated])
        return f"jump move: {beginning}->{end}, capturing [{captured}]"
