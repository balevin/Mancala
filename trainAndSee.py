from Player import Player
from util import evaluate_players
from TFSessionManager import TFSessionManager as TFSN
import matplotlib.pyplot as plt
from RandomPlayer import RandomPlayer
from nnPlayer import EGreedyNNQPlayer
import tensorflow as tf
from game import Board
tf.compat.v1.reset_default_graph()  

nnplayer = EGreedyNNQPlayer("QLearner1", training=True)
# nnplayer.new_game(True)
rndplayer = RandomPlayer()

game_number, p1_wins, p2_wins, draws = evaluate_players(nnplayer, rndplayer, num_battles=2)

p = plt.plot(game_number, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')
# plt.show()
# board = Board()
# while not board.isOver():
#     if board.myTurn:
#         nnplayer.move(board)
#     else:
#         move = input('Brad: input which pile you would like to move: \n')
#         board.makeMove(move)