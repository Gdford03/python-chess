from player import Player
from move import Move
from chess_piece import ChessPiece
from enum import Enum
from pawn import Pawn
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from knight import Knight


class MoveValidity(Enum):
    VALID = 0
    INVALID = 1
    INTO_CHECK = 2

class ChessModel:
    def __init__(self):
        
        #initialize size of the board which 8x8
        self.__nrows = 8
        self.__ncols = 8
        self.__board = [[None] * self.__ncols for _ in range(self.__nrows)]
        self.__player = Player.WHITE
        #first move is white so the player should be set to white
        self.__message_code = MoveValidity.VALID
        #sets the inital code to a valid move
        self.__initialize_board()
        #runs the initialize board method
        self.__moves = []
        #This list stores all moves in it


    def __initialize_board(self):
        #this function sets all the pieces where they need to be
        for col in range(self.__ncols):
            #places pawns in the correct rows and columns
            self.__board[6][col] = Pawn(Player.WHITE)
            self.__board[1][col] = Pawn(Player.BLACK)

        #sets the order of the pieces in the correct order
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_type in enumerate(piece_order):
            #enumerates the order of the pieces for black and white
            self.__board[7][col] = piece_type(Player.WHITE)
            self.__board[0][col] = piece_type(Player.BLACK)

    @property
    def nrows(self) -> int:
        #returns number of rows
        return self.__nrows

    @property
    def ncols(self) -> int:
        #returns number of columns
        return self.__ncols

    @property
    def current_player(self) -> Player:
        #returns the current player
        return self.__player

    @property
    def messageCode(self) -> MoveValidity:
        #return the message code indicating the validity of the move
        return self.__message_code

    def is_valid_move(self, move: Move) -> bool:
        #check if the move is valid
        start_row, start_col = move.from_row, move.from_col #sets rows and columns
        end_row, end_col = move.to_row, move.to_col
        # Check if the move is within the bounds of the board
        if not (0 <= start_row < self.__nrows and 0 <= start_col < self.__ncols and
                0 <= end_row < self.__nrows and 0 <= end_col < self.__ncols):
            self.__message_code = MoveValidity.INVALID
            return False
        # Check if there is a piece at the starting position and if it belongs to the current player
        piece = self.__board[start_row][start_col]
        if piece is None or piece.player != self.__player:
            self.__message_code = MoveValidity.INVALID
            return False
        # Check if the move is valid according to the piece's rules
        if not piece.is_valid_move(move, self.__board):
            self.__message_code = MoveValidity.INVALID
            return False
        # Check if the path between the start and end positions is clear of other pieces
        if not self.is_path_clear(move):
            self.__message_code = MoveValidity.INVALID
            return False
        # Simulate the move and check if it puts the current player's king in check
        original_piece = self.__board[end_row][end_col]
        self.__board[end_row][end_col] = self.__board[start_row][start_col]
        self.__board[start_row][start_col] = None

        if self.in_check(self.__player):
            self.__board[start_row][start_col] = self.__board[end_row][end_col]
            self.__board[end_row][end_col] = original_piece
            self.__message_code = MoveValidity.INTO_CHECK
            return False
        # Undo Undo Undo Undo
        self.__board[start_row][start_col] = self.__board[end_row][end_col]
        self.__board[end_row][end_col] = original_piece
        self.__message_code = MoveValidity.VALID
        return True


    def is_path_clear(self, move: Move) -> bool:
        # Check if the path between the start and end positions of a move is clear of other pieces
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        if start_row == end_row:
            # Check if the path is clear horizontally
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if self.__board[start_row][col] is not None:
                    return False
        elif start_col == end_col:
            # Check if the path is clear vertically
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if self.__board[row][start_col] is not None:
                    return False
        else:
            # Check if the path is clear diagonally
            row_direction = 1 if end_row > start_row else -1
            col_direction = 1 if end_col > start_col else -1
            current_row, current_col = start_row + row_direction, start_col + col_direction
            while current_row != end_row and current_col != end_col:
                if self.__board[current_row][current_col] is not None:
                    return False
                current_row += row_direction
                current_col += col_direction

        return True
            
        
    def in_check(self, p: Player) -> bool:
        # Check if a player's king is in check
        king_position = self.find_king_position(p)
        #Using the helper function find_king_positions this finds the kings position
        if not king_position:
            return False

        opponent = Player.BLACK if p == Player.WHITE else Player.WHITE
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.__board[row][col]
                if piece and piece.player == opponent:
                    # Check if any opponent piece can capture the king
                    if piece.is_valid_move(Move(row, col, *king_position), self.__board):
                        return True
        return False
    def find_king_position(self, p: Player) -> tuple[int, int]:
        # Find the position of a player's king on the board
        #This checks through all the rows and columns and looks for the king piece
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.__board[row][col]
                if isinstance(piece, King) and piece.player == p:
                    return row, col
        return None

    def piece_at(self, row: int, col: int) -> ChessPiece:
        # Get the piece at a given position on the board
        if 0 <= row < self.__nrows and 0 <= col < self.__ncols:
            return self.__board[row][col]
        else:
            return None

    def set_next_player(self) -> None:
        # Set the next player after a move
        self.__player = Player.BLACK if self.__player == Player.WHITE else Player.WHITE

    def set_piece(self, row: int, col: int, piece: ChessPiece) -> None:
        # Set a piece at a given position on the board
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise ValueError("Value Error")
        if piece is not None and not isinstance(piece, ChessPiece):
            raise TypeError("Type Error")
        self.__board[row][col] = piece

    def is_complete(self) -> bool:
        # Check if the game is complete (checkmate or stalemate)
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.__board[row][col]
                if piece and piece.player == self.__player:
                    for new_row in range(self.__nrows):
                        for new_col in range(self.__ncols):
                            if self.is_valid_move(Move(row, col, new_row, new_col)):
                                return False
        return True


    #This does not work :\
    def prompt_promotion(self, player: Player) -> ChessPiece:
        # Prompt the player to choose a piece for pawn promotion

        print(f"Your pawn reached the back rank and can be promoted.")
        print(f"Choose a piece to promote to for {player.name}:")
        print("1. Queen")
        print("2. Rook")
        print("3. Bishop")
        print("4. Knight")

        while True:
            choice = input("1 = Queen, 2 = Rook, 3 = Bishop, 4 = Knight")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= 4:
                    if choice == 1:
                        return Queen(player)
                    elif choice == 2:
                        return Rook(player)
                    elif choice == 3:
                        return Bishop(player)
                    elif choice == 4:
                        return Knight(player)
                else:
                    print("Please enter a number between 1 and 4.")
            else:
                print("Please enter a number.")

    def move(self, move: Move) -> None:
        # Make a move on the chess board
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check if the move is valid
        if not self.is_valid_move(move):
            return
        # Store the original piece before making the move
        original_piece = self.__board[start_row][start_col]  # Store the original piece before the move

        self.__moves.append((start_row, start_col, end_row, end_col, original_piece, self.__board[end_row][end_col]))
        # Make the move
        self.__board[end_row][end_col] = original_piece
        self.__board[start_row][start_col] = None
        # Switch to the next player
        self.set_next_player()
        # Promote pawn if it reaches the last rank
        if isinstance(self.__board[end_row][end_col], Pawn) and (end_row == 0 or end_row == 7):
            pawn_color = self.__board[end_row][end_col].player
            self.__board[end_row][end_col] = Queen(pawn_color)

    def undo(self):
        # Undo the last move
        if not self.__moves:
            raise UndoException("No moves left to undo")
        #Checks through the list of moves and pops that one
        last_move = self.__moves.pop()

        if len(last_move) < 4:
            raise ValueError("Invalid move format")
        # Retrieve the details of the last move
        start_row, start_col, end_row, end_col = last_move[:4]
        original_piece = last_move[4]
        captured_piece = last_move[5]
        # Restore the original positions of the pieces
        self.__board[start_row][start_col] = original_piece
        self.__board[end_row][end_col] = captured_piece
        # Switch back to the previous player
        self.set_next_player()

class UndoException(Exception):
    pass