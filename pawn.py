from player import Player
from move import Move
from chess_piece import ChessPiece


class Pawn(ChessPiece):
    def __str__(self) -> str:
        return f"{self.player.name} Pawn"

    def type(self) -> str:
        return "Pawn"

    def is_valid_move(self, move: Move, board: list[list[ChessPiece]]) -> bool:
       # assigns start row and start col to the corresponding move from
        start_row, start_col = move.from_row, move.from_col
        
        # assigns end row and end col to the corresponding move to
        end_row, end_col = move.to_row, move.to_col 

        # checks if peice at start postion is a pawn
        if not isinstance(board[start_row][start_col], Pawn):
            return False

        # checks parent class
        if not super().is_valid_move(move, board):
            return False

        # determines what direction the pawn can move
        direction = -1 if self.player == Player.WHITE else 1
        
        # determines what the first row of the pawn should be
        first_row = 6 if self.player == Player.WHITE else 1
        

        # checks if the move is in the same col
        if end_col == start_col:
            
            # checks if the end row is forward one
            if end_row == start_row + direction:
                if board[end_row][end_col] is None:
                    return True
                
            # checks if end row is the start row + direction * 2 to see if it moved twice
            elif end_row == start_row + (direction + direction):
                
                # checks if pawn was in the starting row
                if start_row == first_row:
                    
                    # checks if there are any peices in the way 
                    if board[end_row - direction][end_col] is None and board[end_row][end_col] is None:
                        return True
                else:
                    return False
            else:
                return False
        
        # checks if pawn is taking a peice
        elif end_col == start_col - 1 or end_col == start_col + 1:
            
            # checks if pawn is moving it right direction
            if end_row == start_row + direction:
                
                # makes sure the peice that its taking isnt self
                if board[end_row][end_col] is not None and board[end_row][end_col].player != self.player:
                    return True
            else:
                return False
            
        # if none of these moves pass then its not a vaild move
        return False