from player import Player
from move import Move
from chess_piece import ChessPiece

class King(ChessPiece):
    def __str__(self) -> str:
        return f"{self.player.name} King"

    def type(self):
        return "King"


    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        # assigns start row and start col to the corresponding move from
        start_row, start_col = move.from_row, move.from_col
        
        # assigns end row and end col to the corresponding move to
        end_row, end_col = move.to_row, move.to_col 

        # checsks if is vaild passes from parent class
        if not super().is_valid_move(move, board):
            return False

        # gives absoulte value of rows
        row_diff = abs(end_row - start_row)
        
        # gives absoulte value of cols
        col_diff = abs(end_col - start_col)

        # checks if both row and col diffs are less than or equal to one
        if max(row_diff, col_diff) <= 1:
            return True
        
        # if not returns false
        return False