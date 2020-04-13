from abc import ABC, abstractmethod

from game import Board 


class Player(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def move(self, board):
        pass

    @abstractmethod
    def final_result(self, board):
        pass

    @abstractmethod
    def new_game(self):
        pass