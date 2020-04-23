import numpy as np
from game import Board
from Player import Player
from RandomPlayer import RandomPlayer
from util import evaluate_players
import matplotlib.pyplot as plt
import random
import pickle


class DiscreetQValuesPlayer(Player):
    def __init__(self, qValues={}, training = True,random_move_prob = 0.95, random_move_decrease = 0.95, alpha = 0.95, gamma = 0.98, end_discount = 0.99):
        self.alpha = alpha
        self.gamma = gamma
        self.end_discount = end_discount
        self.me = None
        self.currentPosition = []
        self.action_log = []
        self.values_log = []
        self.training = training
        self.random_move_prob = random_move_prob
        self.random_move_decrease = random_move_decrease
        self.extra_reward_log = []
        if len(qValues.keys()) == 0:
            self.qValues = qValues
        else:
            pickle_in = open("dict.pickle","rb")
            self.qValues = pickle.load(pickle_in)
            print('loaded it')
        super().__init__()

    
    def new_game(self, me):
        self.me = me
        self.currentPosition = []
        self.action_log = []
        self.values_log = []

    def updateQValues(self, gameReward):
        totalMoves = 1
        hadMoves = 0
        game_length = len(self.action_log)
        for i in range(game_length-1):
            state = tuple(self.currentPosition[i])
            totalMoves += 1
            if state in self.qValues:
                hadMoves += 1
                thisStateActions = self.qValues[state]
            else:
                thisStateActions = [0,0,0,0,0,0]
            nextState = tuple(self.currentPosition[i+1])
            if nextState in self.qValues:
                nextQValues = self.qValues[nextState]
            else:
                nextQValues = [0,0,0,0,0,0]
                self.qValues[nextState] = nextQValues
            try:
                thisStateActions[self.action_log[i]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[i]+(gameReward*self.end_discount**(game_length-1-i)) + self.gamma*max(nextQValues))
            except:
                print(thisStateActions[self.action_log[i]])
                print(self.extra_reward_log[i])
                print(max(nextQValues))
                input()
            self.qValues[state] = thisStateActions
        state = tuple(self.currentPosition[game_length-1])
        if state in self.qValues:
            thisStateActions = self.qValues[state]
            hadMoves += 1
        else:
            thisStateActions = [0,0,0,0,0,0]
        thisStateActions[self.action_log[game_length-1]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[game_length-1]+gameReward + self.gamma*max(nextQValues))
        self.qValues[state] = thisStateActions 
        return totalMoves, hadMoves
    def move(self, board):
        self.currentPosition.append(board.myMarbles+board.opMarbles)
        if (self.training) and (random.random() < self.random_move_prob):
            move = board.randomPossibleMove()
        else:
            if tuple(board.myMarbles+board.opMarbles) in self.qValues:
                available = board.getMyAvailable()
                values = self.qValues[tuple(board.myMarbles+board.opMarbles)]
                sortedValues = sorted(values, reverse=True)
                if float(sum(values)) == 0.0:
                    move = board.makeSmartMove()

                for i in range(len(values)):
                    if values.index(sortedValues[i]) in available:
                        move = values.index(sortedValues[i])
                        break
                had = True
            else:
                move = board.makeSmartMove()
                had = False
        if not move and move!=0:
            move = board.makeSmartMove()
        if not move and move !=0:
            move = board.randomPossibleMove()
        try:
            move
        except:
            move = board.randomPossibleMove()
        self.action_log.append(move)
        if self.training:
            extra = board.makeMove(move)
            self.extra_reward_log.append(extra)
        else:
            board.makeMove(move)
        if not self.training:
            return had
        # input()
    def final_result(self, board):
        if board.myMarbles>board.opMarbles:
            if self.me:
                reward = 10+board.myMarbles-board.opMarbles
            else:
                reward=-10+board.opMarbles-board.myMarbles

        if board.opMarbles>board.myMarbles:
            if self.me:
                reward = -10+board.myMarbles-board.opMarbles
            else:
                reward = 10+board.opMarbles-board.myMarbles
        else:
            reward = 0

        if self.training:
            self.updateQValues(reward)
            if self.random_move_prob>= 0.05:
                self.random_move_prob*=self.random_move_decrease
    
    def saveQValues(self):
        pickle_out = open("dict.pickle","wb")
        pickle.dump(self.qValues, pickle_out)
        pickle_out.close()
