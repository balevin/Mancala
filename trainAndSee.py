from Player import Player
from util import evaluate_players
from TFSessionManager import TFSessionManager as TFSN
import matplotlib.pyplot as plt
from RandomPlayer import RandomPlayer
from nnPlayer import EGreedyNNQPlayer
from discreetPlayer import DiscreetQValuesPlayer
import tensorflow as tf
from game import Board
tf.compat.v1.reset_default_graph()  

nnplayer = EGreedyNNQPlayer("QLearner1", training=True)
# nnplayer.new_game(True)
discreetPlayer = DiscreetQValuesPlayer()
rndplayer = RandomPlayer()

game_number, p1_wins, p2_wins, draws = evaluate_players(discreetPlayer, nnplayer, games_per_battle=10, num_battles=100)
discreetPlayer.saveQValues()
p = plt.plot(game_number, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')
plt.show()
# board = Board()
# while not board.isOver():
#     if board.myTurn:
#         nnplayer.move(board)
#     else:
#         move = input('Brad: input which pile you would like to move: \n')
# #         board.makeMove(move)
# board = Board()
# while not board.isOver():
#     if board.myTurn:
#         move = input('Brad: input which pile you would like to move: \n')
#     else:
#         move = input('Other: input which pile you would like to move: \n')
#     board.makeMove(move)