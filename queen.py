from move import Move
from player import Player
from chess_piece import ChessPiece


class Queen(ChessPiece):
    
    #Queen constructor
    def __init__(self, player: Player) -> None:
        super().__init__(player)
        
    #returns the name of the piece which is "Queen"
    def __str__(self) -> str:
        return f"{self.player.name} Queen"
    
    #returns the type of the Queen piece which is Queen
    def type(self) -> str:
        return "Queen"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        
        #Checks the many moves that a queen can do and if they are valid
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col
        
        #Checks within the boundaries
        if not super().is_valid_move(move, board):
            return False
        
        #Checks on the straight line
        if start_row == end_row or start_col == end_col:
            
            # Moving in a straight line
            if self._is_valid_straight_move(move, board):
                return True
        elif abs(start_row - end_row) == abs(start_col - end_col):
            
            # Moving diagonally
            if self._is_valid_diagonal_move(move, board):
                return True

        return False

    def _is_valid_straight_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        
        #I was thingking of using this for rook but it only worked for queen
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        if start_row == end_row:
            
            # Moving horizontally
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
            return True
        elif start_col == end_col:
            
            # Moving vertically
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False
            return True
        else:
            return False

    def _is_valid_diagonal_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        
        #Same that was used for bishop
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col
        
        #checks movement for diagonal moves
        row_direction = 1 if end_row > start_row else -1
        col_direction = 1 if end_col > start_col else -1

        current_row, current_col = start_row + row_direction, start_col + col_direction
        
        #Is slightly different than bishop but same logic
        while current_row != end_row and current_col != end_col:
            if board[current_row][current_col] is not None:
                return False
            current_row += row_direction
            current_col += col_direction

        return True
        