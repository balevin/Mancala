import numpy as np
from game import Board
from Player import Player
from RandomPlayer import RandomPlayer
from util import evaluate_players
import matplotlib.pyplot as plt
import random
import pickle


class DiscreetQValuesPlayer(Player):
    def __init__(self, qValues=None, training = True,random_move_prob = 0.99, random_move_decrease = 0.99, alpha = 0.4, gamma = 0.9, end_discount = 0.99, tryUntriedProb=0.5):
        self.tryUntriedProb = tryUntriedProb
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
        if qValues:
            self.qValues = qValues

        else:
            self.qValues = {}
        super().__init__()

    
    def new_game(self, me):
        self.me = me
        self.currentPosition = []
        self.action_log = []
        self.values_log = []

    def updateQValues(self, gameReward):
        # print(self.action_log)
        # print(self.extra_reward_log)
        # print(self.currentPosition)
        # input()
        totalMoves = 1
        hadMoves = 0
        game_length = len(self.action_log)
        for i in range(game_length-1):
            state = tuple(self.currentPosition[i])
            # print('current state: ', state)
            totalMoves += 1
            if state in self.qValues:
                # print('had it')
                hadMoves += 1
                thisStateActions = self.qValues[state]
            else:
                # print('didnt have it')
                # continue
                thisStateActions = [0,0,0,0,0,0]
            
            nextState = tuple(self.currentPosition[i+1])
            # print('next state: ', nextState)
            if nextState in self.qValues:
                # print('had next')
                nextQValues = self.qValues[nextState]
            else:
                # print("didn't have next")
                nextQValues = [0,0,0,0,0,0]
                self.qValues[nextState] = nextQValues
            # print('qValues before: ', thisStateActions)
            thisStateActions[self.action_log[i]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[i]+(gameReward*self.end_discount**(game_length-1-i)) + self.gamma*max(nextQValues))
            # print('qValues after: ', thisStateActions)
            self.qValues[state] = thisStateActions
            # input()
        state = tuple(self.currentPosition[game_length-1])
        if state in self.qValues:
            thisStateActions = self.qValues[state]
            hadMoves += 1
        else:
            # return totalMoves, hadMoves
            thisStateActions = [0,0,0,0,0,0]
        thisStateActions[self.action_log[game_length-1]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[game_length-1]+gameReward + self.gamma*max(nextQValues))
        self.qValues[state] = thisStateActions 
        return totalMoves, hadMoves
    def move(self, board):
        # if self.me:
        #     boardRep = tuple(board.myMarbles+board.opMarbles)
        # else:
        #     boardRep = tuple(board.opMarbles[::-1]+board.myMarbles[::-1])
        boardRep = tuple(board.myMarbles + board.opMarbles)
        self.currentPosition.append(boardRep)
        if (self.training) and (random.random() < self.random_move_prob):
            move = board.randomPossibleMove()
        else:
            if boardRep in self.qValues:
                available = board.getMyAvailable()
                # if not self.me:
                #     available = [5-x for x in available]
                values = self.qValues[boardRep]
                if (self.training) and (0 in values) and (random.random()<self.tryUntriedProb):
                    print('getting untried')
                    zeroPlace = values.index(0)
                    move = zeroPlace
                    extra = board.makeMove(move)
                    self.extra_reward_log.append(extra)
                    return
                sortedValues = sorted(values, reverse=True)
                if float(sum(values)) == 0.0:
                    move = board.makeSmartMove()
                    had = False 
                for i in range(len(values)):
                    if values.index(sortedValues[i]) in available:
                        # if self.me:
                        #     move = values.index(sortedValues[i])
                        # else:
                        #     move = 5-values.index(sortedValues[i]) 
                        # break
                        move = values.index(sortedValues[i])
                had=True
            else:
                if self.training:
                    move = board.randomPossibleMove()
                else:
                    move = board.makeSmartMove()
                    had = False
        # print('available: ', board.getMyAvailable())
        try:
            move
        except:
            move = board.makeSmartMove()
        if not move and move !=0:
            move = board.randomPossibleMove()
        self.action_log.append(move)
        if self.training:
            extra = board.makeMove(move)
            self.extra_reward_log.append(extra)
        else:
            board.makeMove(move)
        if not self.training:
            return had
        # print('action log: ', self.action_log)
        # print('extra reward: ', self.extra_reward_log)
        # print('position log: ', self.currentPosition)
        # input()
        # input()
    def final_result(self, board):
        if board.myScore>board.opScore:
            if self.me:
                # reward = 10+board.myScore-board.opScore
                reward = 10
            else:
                # reward=-10+board.opScore-board.myScore
                reward = -10

        elif board.opScore>board.myScore:
            if self.me:
                # reward = -10+board.myScore-board.opScore
                reward = -10
            else:
                # reward = 10+board.opScore-board.myScore
                reward = 10
        else:
            reward = 0
        if self.training:
            self.updateQValues(reward)
            if self.random_move_prob>= 0.33:
                self.random_move_prob*=self.random_move_decrease
    
    def saveQValues(self):
        if self.me:
            pickle_out = open("player1.pickle","wb")
            pickle.dump(self.qValues, pickle_out)
            pickle_out.close()
        else:
            pickle_out = open("player2.pickle","wb")
            pickle.dump(self.qValues, pickle_out)
            pickle_out.close()
