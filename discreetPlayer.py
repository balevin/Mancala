import numpy as np
from game import Board
from Player import Player
from RandomPlayer import RandomPlayer
from util import evaluate_players
import matplotlib.pyplot as plt
import random
import pickle


class DiscreetQValuesPlayer(Player):
    def __init__(self, qValues=None, training = True,random_move_prob = 0.99, random_move_decrease = 0.99, alpha = 0.25, gamma = 0.9, end_discount = 0.99):
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
        self.extra_reward_log = []

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
                continue
                # thisStateActions = [0,0,0,0,0,0]
            
            nextState = tuple(self.currentPosition[i+1])
            # print('next state: ', nextState)
            if nextState in self.qValues:
                # print('had next')
                nextQValues = self.qValues[nextState]
            else:
                # print("didn't have next")
                nextQValues = [0,0,0,0,0,0]
                # self.qValues[nextState] = nextQValues
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
            return totalMoves, hadMoves
            # thisStateActions = [0,0,0,0,0,0]
        thisStateActions[self.action_log[game_length-1]] = (1-self.alpha)*thisStateActions[self.action_log[i]] + self.alpha*(self.extra_reward_log[game_length-1]+gameReward + self.gamma*max(nextQValues))
        self.qValues[state] = thisStateActions 
        return totalMoves, hadMoves
    def move(self, board):
        # if self.me:
        #     boardRep = tuple(board.myMarbles+board.opMarbles)
        # else:
        #     boardRep = tuple(board.opMarbles[::-1]+board.myMarbles[::-1])
        # print(board)
        # print(board.getMyAvailable())
        # input()
        boardRep = tuple(board.myMarbles + board.opMarbles)
        self.currentPosition.append(boardRep)
        # hi = False
        if (self.training) and (random.random() < self.random_move_prob):
        # if hi:
            move = board.randomPossibleMove()
        else:
            if boardRep in self.qValues:
                # print(sum([x for x in self.qValues[boardRep] if x==0])
                if (self.training) and (random.random()<0.5) and (0 in self.qValues[boardRep]):
                    possible = 0
                    available = board.getMyAvailable()
                    zeroInds = [i for i in range(6) if self.qValues[boardRep][i] == 0]
                    possible = [x for x in zeroInds if x in available]
                    if len(possible) == 0:
                        move = board.randomPossibleMove()
                    else:
                        randInt = random.randint(0,len(possible)-1)
                        move = possible[randInt]
                else:
                    available = board.getMyAvailable()
                    values = self.qValues[boardRep]
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
        try:
            if not move and move!=0:
                move = board.makeSmartMove()
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
