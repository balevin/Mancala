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
rndplayer = RandomPlayer()
game_number, p1_wins, p2_wins, draws, allPos = evaluate_players(discreetPlayer, rndplayer, games_per_battle=100000, num_battles=1)
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

pickle_in = open('p1PlusSelfTraining.pickle', 'rb')
qvals = pickle.load(pickle_in)
print(os.stat('p1PlusSelfTraining.pickle').st_size/(1024*1024))
print(qvals[(4,4,4,4,4,4,4,4,4,4,4,4)])
total = 0
for key in qvals.keys():
    total+=qvals[key].count(0)
print(total/len(qvals))


discreetPlayer = DiscreetQValuesPlayer(training=False, qValues=qvals)
rndplayer = RandomPlayer()
game_number, p1_wins, p2_wins, draws, allPos = evaluate_players(discreetPlayer, rndplayer, games_per_battle=100000, num_battles=1)
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


