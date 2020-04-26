from Player import Player
from util import evaluate_players
# from TFSessionManager import TFSessionManager as TFSN
import matplotlib.pyplot as plt
from RandomPlayer import RandomPlayer
# from nnPlayer import EGreedyNNQPlayer
from discreetPlayer import DiscreetQValuesPlayer
# import tensorflow as tf
from game import Board
from smartPlayer import SmartPlayer
import pickle
#tf.compat.v1.reset_default_graph()  

# nnplayer = EGreedyNNQPlayer("QLearner1", training=True)
# nnplayer.new_game(True)e
print('starting')
pickle_in = open('prettyGood.pickle', 'rb')
qvals = pickle.load(pickle_in)
# discreetPlayer = DiscreetQValuesPlayer(training=True, qValues=qvals)
# discreetPlayer = DiscreetQValuesPlayer(training=True, qValues=qvals)
discreetPlayer = DiscreetQValuesPlayer(training=False, qValues=qvals)
rndplayer = RandomPlayer()
smrtplayer = SmartPlayer()
game_number, p1_wins, p2_wins, draws, __ = evaluate_players(discreetPlayer, rndplayer, games_per_battle=100000, num_battles=1)
game_number, p1_wins, p2_wins, draws, __ = evaluate_players(discreetPlayer, smrtplayer, games_per_battle=100000, num_battles=1)
# game_number, p1_wins, p2_wins, draws = evaluate_players(smrtplayer, rndplayer, games_per_battle=100000, num_battles=1)


# game_number, p1_wins, p2_wins, draws = evaluate_players(rndplayer, discreetPlayer, games_per_battle=100000, num_battles=1)
#discreetPlayer.saveQValues()
#p = plt.plot(game_numbe, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')
#plt.show()
# board = Board()
# # print(board)
# while not board.isOver():
    # if board.myTurn:
    #    move = input('bottom: input which pile you would like to move: \n')
        # discreetPlayer.move(board)
    #    board.makeMove(move)
    # move = board.makeSmartMove()
    # board.makeMove(move)
    # else:
    #    move = board.makeSmartMove()
    #    board.makeMove(move)
       # rndplayer.move(board)
       # print(board)
        # move = input('Top: input which pile you would like to move: \n')
        # board.makeMove(move)
