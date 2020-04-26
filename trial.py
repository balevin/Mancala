from Player import Player
from util import evaluate_players
from RandomPlayer import RandomPlayer
from discreetPlayer import DiscreetQValuesPlayer
# import tensorflow as tf
from game import Board
from smartPlayer import SmartPlayer
import pickle
import os
import random
print('start')
pickle_in = open('player1.pickle', 'rb')
qvals = pickle.load(pickle_in)
print(os.stat('player1.pickle').st_size/(1024*1024))
print(qvals[(4,4,4,4,4,4,4,4,4,4,4,4)])
total = 0
for key in qvals.keys():
    total+=qvals[key].count(0)
print(total/len(qvals))


discreetPlayer = DiscreetQValuesPlayer(training=False, qValues=qvals)
# discreetPlayer = DiscreetQValuesPlayer(training=True, qValues=qvals)
# discreetPlayer = DiscreetQValuesPlayer(training=False, qValues=qvals)
rndplayer = RandomPlayer()
smrtplayer = SmartPlayer()
# game_number, p1_wins, p2_wins, draws = evaluate_players(discreetPlayer, smrtplayer, games_per_battle=100000, num_battles=1)
game_number, p1_wins, p2_wins, draws, allPos = evaluate_players(discreetPlayer, rndplayer, games_per_battle=100000, num_battles=1)
# game_number, p1_wins, p2_wins, draws = evaluate_players(smrtplayer, rndplayer, games_per_battle=100000, num_battles=1)
total = 0
numSeen = 0
numNotSeen = 0
for key in allPos:
    if key in qvals:
        total += qvals[key].count(0)
        numSeen+=1
    else:
        numNotSeen += 1
print(total/numSeen)
print(numSeen)
print(numNotSeen)
print(numSeen/(numNotSeen+numSeen))
for i in range(3):
    print(random.choice(tuple(allPos)))


# game_number, p1_wins, p2_wins, draws = evaluate_players(rndplayer, discreetPlayer, games_per_battle=100000, num_battles=1)
# discreetPlayer.saveQValues()
#p = plt.plot(game_numbe, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')
#plt.show()
# board = Board()
# # print(board)
# while not board.isOver():
#    if board.myTurn:
    #    move = input('bottom: input which pile you would like to move: \n')
        # discreetPlayer.move(board)
    #    board.makeMove(move)
    # move = board.makeSmartMove()
    # board.makeMove(move)
#    else:
    #    move = board.makeSmartMove()
    #    board.makeMove(move)
       # rndplayer.move(board)
       # print(board)
        # move = input('Top: input which pile you would like to move: \n')
        # board.makeMove(move)
