import numpy as np
import tensorflow as tf
from game import Board
from Player import Player
from RandomPlayer import RandomPlayer
from util import evaluate_players
from TFSessionManager import TFSessionManager as TFSN
import matplotlib.pyplot as plt
import random

class QNetwork:
    def __init__(self, name, learning_rate=0.01):
        self.learning_rate = learning_rate
        self.name = name
        self.input_positions = None
        self.target_input = None
        self.q_values = None
        self.probabilities = None
        self.train_step = None
        self.build_graph(name)

    def add_dense_layer(self, input_tensor, output_size, activation_fn=None, name=None):
        return tf.layers.dense(input_tensor, output_size, activation=activation_fn, kernel_initializer=tf.contrib.layers.variance_scaling_initializer(), name=name)
        
    
    def build_graph(self, name):
        with tf.compat.v1.variable_scope(name):
            # Try this as just 12 with number representing each thing
            # Try this as dim 48*12. Each 48 bits represents a bucket, the first x are 1s if that bucket contains x marbles
            self.input_positions = tf.placeholder(tf.float32, shape=(None,12*48), name='inputs')
            # self.input_positions = tf.placeholder(tf.float32, shape=(None, 12*48), name='inputs')
            
            # Try with output of 6, one for each of 6 options, have to somehow specify first 6 for one, second 6 for other
            # Try with output of 12, one for each 12, somehow make first/last 6 0 depending on turn
            self.target_input = tf.placeholder(tf.float32, shape=(None, 12), name='targets')
            # self.target_input = tf.placeholder(tf.float32, shape=(None, 6), name='targets')
            net = self.input_positions
            # Would change to 12*12*48 if do other way
            net = self.add_dense_layer(net, 12*12, tf.nn.relu)
            net = self.add_dense_layer(net, 4*12, tf.nn.relu)
            # Would change 12 to 6 if do other way
            self.q_values = self.add_dense_layer(net, 12, name='q_values')
            self.probabilities = tf.nn.softmax(self.q_values, name='probabilities')
            mse = tf.losses.mean_squared_error(predictions=self.q_values, labels=self.target_input)
            self.train_step = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(mse,name='train')
    def save(self):
        tf.saved_model.save(self, 'models/')

class EGreedyNNQPlayer(Player):
    def board_state_to_nn_input(self, state):
        # For first way:
        # state = np.array(state)
        # return state

        # For second way:
        endList = []
        for number in state:
            for i in range(number):
                endList.append(1)
            for i in range(48-number):
                endList.append(0)
        state = np.array(endList)
        return state

    def __init__(self, name, reward_discount = 0.95, win_value = 1.0, draw_value = 0.0,
        loss_value = -1.0, learning_rate = 0.01, training = True,
        random_move_prob = 0.95, random_move_decrease = 0.95):
        self.reward_discount = reward_discount
        self.win_value = win_value
        self.draw_value = draw_value
        self.loss_value = loss_value
        self.me = None
        self.board_position_log = []
        self.action_log = []
        self.next_max_log = []
        self.values_log = []
        self.name = name
        self.nn = QNetwork(name, learning_rate)
        self.training = training
        self.random_move_prob = random_move_prob
        self.random_move_decrease = random_move_decrease
        self.init = tf.global_variables_initializer()
        self.extra_reward_log = []

        super().__init__()

    
    def new_game(self, me):
        self.me = me
        self.board_position_log = []
        self.action_log = []
        self.next_max_log = []
        self.values_log = []

    def calculate_targets(self):
        game_length = len(self.action_log)
        targets = []
        for i in range(game_length):
            target = np.copy(self.values_log[i])
            target[self.action_log[i]] = self.reward_discount*(self.next_max_log[i] + self.extra_reward_log[i])
            targets.append(target)
        return targets

    def get_probs(self, input_pos):
        probs, qvalues = TFSN.get_session().run([self.nn.probabilities, self.nn.q_values],
        {self.nn.input_positions:[input_pos]})
        return probs[0], qvalues[0]

    def move(self, board):
        # print('making nn move')
        # has to decide which move to take
        self.board_position_log.append(board.myMarbles+board.opMarbles)
        nn_input = self.board_state_to_nn_input(board.myMarbles+board.opMarbles)
        probs, qvalues = self.get_probs(nn_input)
        qvalues=np.copy(qvalues)
        for index, p in enumerate(qvalues):
            if not board.is_valid(index):
                probs[index] = -1
            elif probs[index] < 0:
                probs[index] = 0

        if (self.training) and (random.random() < self.random_move_prob):
            # print('random')
            move = board.randomPossibleMove()
        else:
            # print('max')
            move = np.argmax(probs)
        
        if len(self.action_log)>0:
            self.next_max_log.append(qvalues[np.argmax(probs)])
        self.action_log.append(move)
        self.values_log.append(qvalues)
        # print(msove)
        extra = board.makeMove(move)
        self.extra_reward_log.append(extra)
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
        
        self.next_max_log.append(reward)
        if self.training:
            targets = self.calculate_targets()
            # print('targets: ', targets)
            nn_input=[self.board_state_to_nn_input(x) for x in self.board_position_log]
            TFSN.get_session().run([self.nn.train_step], 
            feed_dict={self.nn.input_positions:nn_input,
            self.nn.target_input:targets})
            print(self.nn)
            print(type(self.nn))
            if self.random_move_prob>= 0.05:
                self.random_move_prob*=self.random_move_decrease
            # self.nn.save()
            # input()