from abc import ABC, abstractmethod
from enum import Enum
from move import Move
from player import Player
'''
This is the main piece class and is the parent class to all the chess peices 

'''
class ChessPiece(ABC):
    
    # sets the current player from the player class
    def __init__(self, player: Player) -> None:
        self.__player = player


    # returns the color of the player in each peice
    @property
    def player(self) -> Player:
        return self.__player

    # method for chess peices to print the string of what they are and who they are
    @abstractmethod
    def __str__(self) -> str:
        pass

    # method for chess peices to print the string of what they are
    @abstractmethod
    def type(self) -> str:
        pass


    # basic invaild moves for each peice 
    @abstractmethod
    def is_valid_move(self, move: Move, board: list[list['ChessPiece']]) -> bool:
        start_row, start_col = move.from_row, move.from_col

        end_row, end_col = move.to_row, move.to_col

        # checks if starting location is in the board 
        if not (0 <= start_row < len(board) and 0 <= start_col < len(board[0])):
            return False
        
        # checks if ending location is in the board
        if not (0 <= end_row < len(board) and 0 <= end_col < len(board[0])):
            return False

        # checks if starting location isnt the same as the end location 
        if (move.from_row, move.from_col) == (move.to_row, move.to_col):
            return False

        # checks if the peice thats trying to move is the corect players peice
        if board[move.from_row][move.from_col] != self:
            return False

        # checks if the ending location doesnt already have the same players peice
        if board[move.to_row][move.to_col] is not None and board[move.to_row][move.to_col].player == self.player:
            return False
        
        # if everything checks then it returns true 
        return True