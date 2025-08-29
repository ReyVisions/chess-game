import tkinter as tk
import numpy as np
from abc import ABC,abstractmethod
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MoveError(Exception):
    """Exception dans le cas ou le joueur effectue un mouvement impossible"""
    def __init__(self,position,message="The move is impossible"):
        self.position=position
        self.message=message
        super().__init__(self.message)

class ColorException(Exception):
    """Exception dans la couleur des pieces lors de leur creation"""
    def __init__(self,color,message="The color needs to be black or white"):
        self.color=color
        self.message=message
        super().__init__(self.message)


class Piece(ABC):
    def __init__(self,color):
        self.color=color
        self.position=0
    
    @property
    def getColor(self):
        return(self.color)
    
    def getPosition(self):
        return(self.position)
    
    def printColor(self):
        print(self.color)

    def printPosition(self):
        print(self.position)
    
    def getName(self):
        return(f"Nothing")
    
    @abstractmethod
    def move(self,positionBefore,positionNext):
        pass

    @abstractmethod
    def capture(self, position_before, position_next):
        pass

class Pawn(Piece):
    def __init__(self, color ):
        if color!="black" and color!="white":
            raise ColorException("The color should be black or white")
        else:
            super().__init__(color)

    def getName(self):
        return(f"{self.color} pawn")
    
    def move(self,positionBefore,positionNext):
        piece=self.board[positionBefore]
        if self.board[positionNext]==0:
            
            self.board[positionBefore]=0
            self.board[positionNext]=piece
        else:
            raise MoveError("You can't move piece to there!")

    def capture(self, position_before, position_next):
        piece = self.board[position_before]
        target_piece = self.board[position_next]
        if target_piece != 0 and target_piece.get_color() != piece.get_color():
            self.board[position_before] = 0
            self.board[position_next] = piece
            piece.position = position_next
        elif target_piece != 0 and target_piece.get_color() == piece.get_color():
            raise MoveError("You can't capture your own piece!")
        else:
            raise MoveError("There is nothing to capture!")        


class Board:
    def __init__(self):
        self.board=np.zeros((8,8),dtype=object)
        for j in range(8):
            for i in range(8):
                self.board[i][j]=0

    def addPiece(self,position,piece):
        self.board[position]=piece

    def deletePiece(self,position):
        self.board[position]=0

    def move(self,positionBefore,positionNext):
        piece=self.board[positionBefore]
        if self.board[positionNext]==0:
            
            self.board[positionBefore]=0
            self.board[positionNext]=piece
        else:
            raise MoveError("You can't move piece to there!")

    def capture(self, position_before, position_next):
        piece = self.board[position_before]
        target_piece = self.board[position_next]
        if target_piece != 0 and target_piece.get_color() != piece.get_color():
            self.board[position_before] = 0
            self.board[position_next] = piece
            piece.position = position_next
        elif target_piece != 0 and target_piece.get_color() == piece.get_color():
            raise MoveError("You can't capture your own piece!")
        else:
            raise MoveError("There is nothing to capture!")

    def printBoard(self):
        letters=["A","B","C","D","E","F","G","H"]
        for i in range(8):
            for j in range(8):
                
                print(f"Position: {letters[j]}{i}, piece= {self.board[i][j].getName()}")
    
class Game:
    def __init__(self):
        self.turn=1
        self.board=Board()
        try:
            blackpawn=Pawn("black")
            whitepawn=Pawn("white")
        except ColorException as e:
            logger.error(f"Erreur sur la création de la piece : {e}")
        else:
            print(f"Creation des pieces {blackpawn.getName()} et {whitepawn.getName} réussie")
        finally:
            print("Fin de gestion d'erreur")

        for i in range(8):
            self.board.addPiece((1,i),whitepawn)
            self.board.addPiece((6,i),blackpawn)
        self.board.printBoard()

def main():
    Game()

if __name__=="__main__":
    main()
    
