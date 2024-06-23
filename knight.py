from player import Player
from move import Move
from chess_piece import ChessPiece


class Knight(ChessPiece):
    def __init__(self, player: Player) -> None:
        super().__init__(player)

    def __str__(self) -> str:
        return f"{self.player.name} Knight"

    def type(self) -> str:
        return "Knight"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
       # assigns start row and start col to the corresponding move from
        start_row, start_col = move.from_row, move.from_col
        
        # assigns end row and end col to the corresponding move to
        end_row, end_col = move.to_row, move.to_col 

        # checks if the move is inside the board and does edge moves
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # does the absoulte value if the row diffrence and the col diffrence
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)

        # checks if the move is L shaped
        if (row_diff, col_diff) in [(1, 2), (2, 1)]:
            
            # checks if the end location has a opponents peice and or if its empty
            if board[end_row][end_col] is None or board[end_row][end_col].player != self.player:
                return True

        # if it isnt in a L shape move then its false 
        return False