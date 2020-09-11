from Player import Player
from util import evaluate_players
import matplotlib.pyplot as plt
from RandomPlayer import RandomPlayer
from discreetPlayer import DiscreetQValuesPlayer
from game import Board
from smartPlayer import SmartPlayer
try:
   import cPickle as pickle
except:
   import pickle
print('starting')
# pickle_in = open('p1PlusSelfTraining.pickle', 'rb')
# qvals1 = pickle.load(pickle_in)
# player1 = DiscreetQValuesPlayer(training=False, qValues=qvals1)
rndplayer = RandomPlayer()
smartPlayer = SmartPlayer()
pickle_in = open('thisGuysPrettyGood.pickle', 'rb')
qvals = pickle.load(pickle_in)
player1 = DiscreetQValuesPlayer(training=False, qValues=qvals)
player1.setPerson(True)
pickle_in = open('player2.pickle', 'rb')
qvals2 = pickle.load(pickle_in)
player2 = DiscreetQValuesPlayer(training=False, qValues=qvals2)
player2.setPerson(False)

# game_number, p1_wins, p2_wins, draws = evaluate_players(player1, player2, games_per_battle=100000, num_battles=50)
# player1.saveStateCounts()
# player2.saveStateCounts()
# player2.saveQValues()
# player2.setTraining(False)
# game_number, p1_wins, p2_wins, draws = evaluate_players(player1, rndplayer, games_per_battle=1000, num_battles=25)
# game_number, p1_wins, p2_wins, draws = evaluate_players(player1, smartPlayer, games_per_battle=1000, num_battles=25)
# player1.saveStateCounts()
# player2.setTraining(True)
# game_number, p1_wins, p2_wins, draws = evaluate_players(rndplayer, player2, games_per_battle=1000, num_battles=25)
# game_number, p1_wins, p2_wins, draws = evaluate_players(smartPlayer, player2, games_per_battle=1000, num_battles=25)
# player2.saveStateCounts()
# player2.saveQValues()
# player2.setTraining(False)

board2 = Board()
print(board2)
while not board2.isOver():
    if board2.myTurn:
        player1.move(board2)
        # print(board2)
        print(board2)
    else:
   ##    player2.move(board2)
        move = input('top: input which pile you would like to move: \n')
        board2.makeMove(move)
        print(board2)

board = Board()
print(board)
while not board.isOver():
    if board.myTurn:
        move = input('bottom: input which pile you would like to move: \n')
        # player1.move(board2)
        board.makeMove(move)
        print(board)
    else:
        player2.move(board)
        # move = input('top: input which pile you would like to move: \n')
        # board.makeMove(move)
        print(board)

print(board)
       
board2 = Board()
print(board2)
while not board2.isOver():
    if board2.myTurn:
        # move = input('bottom: input which pile you would like to move: \n')
        player1.move(board2)
        print(board2)
        # board2.makeMove(1move)
    else:
   ##    player2.move(board2)
        move = input('top: input which pile you would like to move: \n')
        board2.makeMove(move)
        print(board2)

print(board2)


board2 = Board()
print(board2)
while not board2.isOver():
    if board2.myTurn:
        # move = input('bottom: input which pile you would like to move: \n')
        player1.move(board2)
        print(board2)
        # board2.makeMove(1move)
    else:
   ##    player2.move(board2)
        move = input('top: input which pile you would like to move: \n')
        board2.makeMove(move)
        print(board2)

print(board2)
# 2
# 5 
# 4 
# 5 
# 1 
# 0 
# 5 
# 1 
# 1 
# 0 
# 5 
# 3

# POSSIBLE idea is to play a bunch of games keping track of how many times each state is reached and find a valuable cutoff of how many times a state is reached and decide to delete all states under that cutoff. 



