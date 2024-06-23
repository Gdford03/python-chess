from player import Player
from move import Move
from chess_piece import ChessPiece

class Bishop(ChessPiece):
    
    #initalize the super as player
    def __init__(self, player: Player) -> None:
        super().__init__(player)
        
    #returns the string of the piece name "Bishop"
    def __str__(self) -> str:
        return f"{self.player.name} Bishop"
    
    #returns the type of the bishop class
    def type(self) -> str:
        return "Bishop"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        
        #checks that the move the bishop is trying to make is a valid move
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col
        
        #check is the destination is within the boundaries of the board
        if not (0 <= end_row < len(board) and 0 <= end_col < len(board[0])):
            return False

        if not super().is_valid_move(move, board):
            return False
        
        #check if the move is along a diagonal path
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
        
        #Check if the diagonal path is clear
        return self._is_valid_diagonal_move(move, board)

    def _is_valid_diagonal_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
        
        #I use this for both the bishop and Queen
        #This checks if a diagonal move is possible
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col
        
        #determines the direction of movement that is diagonally possible
        row_direction = 1 if end_row > start_row else -1
        col_direction = 1 if end_col > start_col else -1
        
        #Check each square that is diagonal
        current_row, current_col = start_row + row_direction, start_col + col_direction

        while current_row != end_row and current_col != end_col:
            if board[current_row][current_col] is not None:
                return False
            current_row += row_direction
            current_col += col_direction
            
        #If occupied with another piece return True
        if board[end_row][end_col] is None or board[end_row][end_col].player != self.player:
            return True

        return False