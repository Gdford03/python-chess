from player import Player
from move import Move
from chess_piece import ChessPiece


class Rook(ChessPiece):
    def __str__(self) -> str:
        return f"{self.player.name} Rook"

    def type(self):
        return "Rook"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        # assigns start row and start col to the corresponding move from
        start_row, start_col = move.from_row, move.from_col
        
        # assigns end row and end col to the corresponding move to
        end_row, end_col = move.to_row, move.to_col 

        # checks if the last move is out of bounds
        if end_row < 0 or end_col < 0 or end_row > 7 or end_col > 7:
            return False

        # checks if parent class
        if not super().is_valid_move(move, board):
            return False

        # checks if the row changed
        if start_row == end_row:
            
            step = 1 if start_col < end_col else -1
            
            # checks if there is a pice in between the start col and end col
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
            return True


        # chcks if the col changed
        elif start_col == end_col:
            
            step = 1 if start_row < end_row else -1
            
            # checks if there is a pice in between the start row and end row
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False
            return True
        
        # if any if these moves arent played then its returns false
        return False