from game import Board
from Player import Player
import random

class RandomPlayer(Player):
    """
    This player can play a game of Tic Tac Toe by randomly choosing a free spot on the board.
    It does not learn or get better.
    """

    def __init__(self):
        """
        Getting ready for playing tic tac toe.
        """
        self.me = None
        super().__init__()

    def move(self, board):
        """
        Making a random move
        :param board: The board to make a move on
        :return: The result of the move
        """
        # 
        # print('making random move')
        # if board.myTurn:
        #     options = board.getMyAvailable()
        # else:
        #     options = board.getOpAvailable()
        # foundOne = False
        # while not foundOne:
        #     trial = random.randint(0,5)
        #     if trial in options:
        #         foundOne = True
        # board.makeMove(trial)
        # return board.getState(), board.isOver()
        if board.myMarbles == [4,4,4,4,4,4]:
            board.makeMove(2)
            return
        if board.myMarbles == [4,4,0,5,5,5]:
            board.makeMove(5)
            return
        move = board.randomPossibleMove()
        board.makeMove(move)

    def final_result(self, result):
        """
        Does nothing.
        :param result: The result of the game that i finished
        :return:
        """

        pass

    def new_game(self, me):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        self.me = me

    def typeRep(self):
        return ' random '