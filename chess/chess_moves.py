# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from shared.moves import Move

class ChessMove(Move):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured = None

    def __str__(self):
        beginning = self._convert_to_letter(self.beginning)
        end = self._convert_to_letter(self.end)
        return f"move: {beginning}->{end}"