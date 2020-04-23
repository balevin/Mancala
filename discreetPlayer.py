import numpy as np
import tensorflow as tf
from game import Board
from Player import Player
from RandomPlayer import RandomPlayer
from util import evaluate_players
from TFSessionManager import TFSessionManager as TFSN
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
        super().__init__()

    
    def new_game(self, me):
        self.me = me
        self.currentPosition = []
        self.action_log = []
        self.values_log = []

    def updateQValues(self, gameReward):
        game_length = len(self.action_log)
        for i in range(game_length-1):
            state = tuple(self.currentPosition[i])
            if state in self.qValues:
                thisStateActions = self.qValues[state]
            else:
                thisStateActions = [0,0,0,0,0,0]
            nextState = tuple(self.currentPosition[i+1])
            if nextState in self.qValues:
                nextQValues = self.qValues[nextState]
            else:
                nextQValues = [0,0,0,0,0,0]
                self.qValues[nextState] = nextQValues
            thisStateActions[self.action_log[i]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[i]+(gameReward*self.end_discount**(game_length-1-i)) + self.gamma*max(nextQValues))
            self.qValues[state] = thisStateActions
        state = tuple(self.currentPosition[game_length-1])
        if state in self.qValues:
            thisStateActions = self.qValues[state]
        else:
            thisStateActions = [0,0,0,0,0,0]
        thisStateActions[self.action_log[game_length-1]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[game_length-1]+gameReward + self.gamma*max(nextQValues))
        self.qValues[state] = thisStateActions 

    def move(self, board):
        self.currentPosition.append(board.myMarbles+board.opMarbles)
        if (self.training) and (random.random() < self.random_move_prob):
            move = board.randomPossibleMove()
        else:
            
            if tuple(board.myMarbles+board.opMarbles) in self.qValues:
                values = self.qValues[tuple(board.myMarbles+board.opMarbles)]
                move = values.index(max(values))
                available = board.getMyAvailabele()
                ind = 1
                while move not in available:
                    move  = values.index(sorted(values)[ind])
                    ind += 1
            else:
                move = board.randomPossibleMove()
        self.action_log.append(move)
        if self.training:
            extra = board.makeMove(move)
            self.extra_reward_log.append(extra)
        else:
            board.makeMove(move)
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
        pickle_out = open("pickles/dict.pickle","wb")
        pickle.dump(self.qValues, pickle_out)
        pickle_out.close()