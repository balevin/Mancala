import numpy as np
import random
import tensorflow as tf
from Player import Player
from RandomPlayer import RandomPlayer
import os
from util import evaluate_players
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from TFSessionManager import TFSessionManager as TFSN
import matplotlib.pyplot as plt
from game import Board
class QNetwork:
    """
    Contains a TensorFlow graph which is suitable for learning the mancala Q function
    """

    def __init__(self, name, learning_rate, beta = 0.00001):
        """
        Constructor for QNetwork. Takes a name and a learning rate for the GradientDescentOptimizer
        :param name: Name of the network
        :param learning_rate: Learning rate for the GradientDescentOptimizer
        """
        self.learningRate = learning_rate
        self.beta = beta
        self.name = name


        self.input_positions = None
        self.target_q = None
        self.actions = None

        # Internal tensors
        self.actions_onehot = None
        self.value = None
        self.advantage = None

        self.td_error = None
        self.q = None
        self.loss = None
        self.total_loss = None
        self.reg_losses = None

        # Externally useful tensors

        self.q_values = None
        self.probabilities = None
        self.train_step = None

        # For TensorBoard

        self.merge = None
        self.build_graph(name)

    def add_dense_layer(self, input_tensor, output_size, activation_fn=None,
                        name = None):
        """
        Adds a dense Neural Net layer to network input_tensor
        :param input_tensor: The layer to which we should add the new layer
        :param output_size: The output size of the new layer
        :param activation_fn: The activation function for the new layer, or None if no activation function
        should be used
        :param name: The optional name of the layer. Useful for saving a loading a TensorFlow graph
        :return: A new dense layer attached to the `input_tensor`
        """
        return tf.layers.dense(input_tensor, output_size, activation=activation_fn,
                               kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                               kernel_regularizer=tf.contrib.layers.l1_l2_regularizer(),
                               name=name)

    def build_graph(self, name):
        """
        Builds a new TensorFlow graph with scope `name`
        :param name: The scope for the graph. Needs to be unique for the session.
        """
        with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
            # change shape of input for when adding score
            self.input_positions = tf.placeholder(tf.float32, shape=(None, 1, 2,6), name='inputs')
            self.target_q = tf.placeholder(shape=[None], dtype=tf.float32, name='target')
            net = self.input_positions

            net = tf.layers.conv2d(inputs=net, filters=128, kernel_size=6,
                                   kernel_regularizer=tf.contrib.layers.l1_l2_regularizer(),
                                   data_format="channels_last", padding='SAME', activation=tf.nn.relu)
            net = tf.layers.conv2d(inputs=net, filters=128, kernel_size=6,
                                   kernel_regularizer=tf.contrib.layers.l1_l2_regularizer(),
                                   data_format="channels_last", padding='SAME', activation=tf.nn.relu)
            net = tf.layers.conv2d(inputs=net, filters=64, kernel_size=6,
                                   kernel_regularizer=tf.contrib.layers.l1_l2_regularizer(),
                                   data_format="channels_last", padding='SAME', activation=tf.nn.relu)

            net = tf.layers.flatten(net)

            net = self.add_dense_layer(net, 12, tf.nn.relu)

            self.value = self.add_dense_layer(net, 1, name='state_q_value')
            self.advantage = self.add_dense_layer(net, 12, name='action_advantage')

            self.q_values = tf.add(self.value, tf.subtract(self.advantage,
                                                           tf.reduce_mean(self.advantage, axis=1, keepdims=True)),
                                   name="action_q_values")

            self.probabilities = tf.nn.softmax(self.q_values, name='probabilities')

            self.actions = tf.placeholder(shape=[None], dtype=tf.int32, name='actions')
            self.actions_onehot = tf.one_hot(self.actions, 12, dtype=tf.float32)
            self.q = tf.reduce_sum(tf.multiply(self.q_values, self.actions_onehot), axis=1, name="selected_action_q")

            tf.summary.histogram("Action_Q_values", self.q)

            self.td_error = tf.square(self.target_q - self.q)
            self.loss = tf.reduce_mean(self.td_error, name="q_loss")

            tf.summary.scalar("Q_Loss", self.loss)
            self.reg_losses = tf.identity(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES, scope=name),
                                          name="reg_losses")

            reg_loss = self.beta * tf.reduce_mean(self.reg_losses)
            tf.summary.scalar("Regularization_loss", reg_loss)

            self.merge = tf.summary.merge_all()

            self.total_loss = tf.add(self.loss, reg_loss, name="total_loss")
            self.train_step = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate). \
                minimize(self.total_loss, name='train')


class ReplayBuffer:
    """
    This class manages the Experience Replay buffer for the Neural Network player
    """

    def __init__(self, buffer_size=3000):
        """
        Creates a new `ReplayBuffer` of size `buffer_size`.
        :param buffer_size:
        """
        self.buffer = []
        self.buffer_size = buffer_size

    def add(self, experience: []):
        """
        Adds a list of experience Tuples to the buffer. If this operation causes the buffer to be longer than its
        defined maximum, old entries will be evicted until the maximum length is achieved. Entries are added and
        evicated on a FIFO basis.
        :param experience: A list of experience tuples to be added to the replay buffer
        """
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:1] = []
        self.buffer.append(experience)

    def sample(self, size) -> []:
        """
        Returns a random sample of `size` entries from the Replay Buffer. If there are less than `size` entries
        in the buffer, all entries will be returned.
        :param size: Number of sample to be returned
        :return: List of `size` number of randomly sampled  previously stored entries.
        """
        size = min(len(self.buffer), size)
        return random.sample(self.buffer, size)


class deepPlayer(Player):
    """
    Implements a mancala player based on a Reinforcement Neural Network learning the mancala Q function
    """

    def board_state_to_nn_input(self, state):
        """
        Converts a mancala board state to an input feature vector for the Neural Network.

        :param state: The board state that is to be converted to a feature vector.
        :return: The feature vector representing the input Tic Tac Toe board state.
        """
        # res = np.array([(state == self.side).astype(int),
        #                 (state == Board.other_side(self.side)).astype(int),
        #                 (state == EMPTY).astype(int)])
        # res = res.reshape(3, 3, 3)
        # res = np.transpose(res, [1, 2, 0])
        res = np.array(state)
        return res

    def create_graph_copy_op(self, src, target, tau):
        """
        Creates and returns a TensorFlow Operation that copies the content of all trainable variables from the
        sub-graph in scope `src` to the sub-graph in scope `target`. Both graphs need to have the same topology and
        the trainable variable been added in the same order for this to work.
        The value `tau` determines to which degree the src value will replace the target value according to the
        foumla: nee_value = src * (1-tau) + target * tau
        :param src: The name of the scope from which to copy the variables
        :param target: The name of the scope to which the variables are copied
        :param tau: A float value between 0 and 1 which determines the weight of src and target for the new value
        :return: A list of TensorFlow tensors for the copying operations
        """
        src_vars = tf.trainable_variables(src)
        target_vars = tf.trainable_variables(target)

        op_holder = []

        for s, t in zip(src_vars, target_vars):
            op_holder.append(t.assign((s.value() * tau) + ((1 - tau) * t.value())))
        return op_holder

    def __init__(self, name, reward_discount = 0.99, win_value = 10.0, draw_value = 0.0,
                 loss_value = -10.0, learning_rate = 0.01, training = True,
                 random_move_prob = 0.9999, random_move_decrease = 0.9997, batch_size=60,
                 pre_training_games = 500, tau = 0.001):
        """
        Constructor for the Neural Network player.
        :param batch_size: The number of samples from the Experience Replay Buffer to be used per training operation
        :param pre_training_games: The number of games played completely radnomly before using the Neural Network
        :param tau: The factor by which the target Q graph gets updated after each training operation
        :param name: The name of the player. Also the name of its TensorFlow scope. Needs to be unique
        :param reward_discount: The factor by which we discount the maximum Q value of the following state
        :param win_value: The reward for winning a game
        :param draw_value: The reward for playing a draw
        :param loss_value: The reward for losing a game
        :param learning_rate: The learning rate of the Neural Network
        :param training: Flag indicating if the Neural Network should adjust its weights based on the game outcome
        (True), or just play the game without further adjusting its weights (False).
        :param random_move_prob: Initial probability of making a random move
        :param random_move_decrease: Factor by which to decrease of probability of random moves after a game
        """
        self.tau = tau
        self.batch_size = batch_size
        self.reward_discount = reward_discount
        self.win_value = win_value
        self.draw_value = draw_value
        self.loss_value = loss_value
        self.side = None
        self.board_position_log = []
        self.action_log = []
        self.next_state_log = []

        self.name = name
        self.q_net = QNetwork(name + '_main', learning_rate)
        self.target_net = QNetwork(name + '_target', learning_rate)

        self.graph_copy_op = self.create_graph_copy_op(name + '_main', name + '_target', self.tau)
        self.training = training
        self.random_move_prob = random_move_prob
        self.random_move_decrease = random_move_decrease

        self.replay_buffer_win = ReplayBuffer()
        self.replay_buffer_loss = ReplayBuffer()
        self.replay_buffer_draw = ReplayBuffer()

        self.game_counter = 0
        self.pre_training_games = pre_training_games

        self.writer = None

        super().__init__()

    def new_game(self):
        """
        Prepares for a new games. Store which side we play and clear internal data structures for the last game.
        :param side: The side it will play in the new game.
        """
        self.board_position_log = []
        self.action_log = []

    def add_game_to_replay_buffer(self, reward: float):
        """
        Adds the game history of the current game to the replay buffer. This method is called internally
        after the game has finished
        :param reward: The reward for the final move in the game
        """
        game_length = len(self.action_log)

        if reward == self.win_value:
            buffer = self.replay_buffer_win
        elif reward == self.loss_value:
            buffer = self.replay_buffer_loss
        else:
            buffer = self.replay_buffer_draw

        for i in range(game_length - 1):
            buffer.add([self.board_position_log[i], self.action_log[i],
                        self.board_position_log[i + 1], 0])

        buffer.add([self.board_position_log[game_length - 1], self.action_log[game_length - 1], None, reward])

    def get_probs(self, input_pos, network):
        """
        Feeds the feature vectors `input_pos` (which encode a board states) into the Neural Network and computes the
        Q values and corresponding probabilities for all moves (including illegal ones).
        :param network: The network to get probabilities from
        :param input_pos: A list of feature vectors to be fed into the Neural Network.
        :return: A list of tuples of probabilities and q values of all actions (including illegal ones).
        """
        probs, qvalues = TFSN.get_session().run([network.probabilities, network.q_values],
                                                feed_dict={network.input_positions: [input_pos]})
        return probs, qvalues

    def get_valid_probs(self, input_pos, network, boards, special=True):
        """
        Evaluates the board positions `input_pos` with the Neural Network `network`. It post-processes the result
        by setting the probability of all illegal moves in the current position to -1.
        It returns a tuple of post-processed probabilities and q values.
        :param input_pos: The board position to be evaluated as feature vector for the Neural Network
        :param network: The Neural Network
        :param boards: A list of corresponding Board objects for testing if a move is illegal.
        :return: A tuple of post-processed probabilities and q values. Probabilities for illegal moves are set to -1.
        """
        probabilities, qvals = self.get_probs(input_pos, network)
        # print(qvals[0].shape)
        # print(qvals[1])
        # print(qvals)
        if boards[0].myTurn:
            qvals = np.copy(qvals[0][0:6])
            probabilities = np.copy(probabilities[0][0:6])
        else:
            qvals = np.copy(qvals[0][6:])
            probabilities = np.copy(probabilities[0][6:])
        qvals = np.copy(qvals.reshape(1,6))
        probabilities = np.copy(probabilities.reshape(1,6))
    # else:
    #     probabilities = np.copy(probabilities)
    #     qvals = np.copy(qvals)
        # We filter out all illegal moves by setting the probability to 0. We don't change the q values
        # as we don't want the NN to waste any effort of learning different Q values for moves that are illegal
        # anyway.
        for q, prob, b in zip(qvals, probabilities, boards):
            for index, p in enumerate(q):
                # print(index)
                # input()
                if not b.is_valid(b.myTurn, index):
                    prob[index] = -1
                elif prob[index] < 0:
                    prob[index] = 0.0
            # print('f')
        return probabilities, qvals

    def move(self, board):
        """
        Implements the Player interface and makes a move on Board `board`
        :param board: The Board to make a move on
        :return: A tuple of the GameResult and a flag indicating if the game is over after this move.
        """

        # We record all game positions to feed them into the NN for training with the corresponding updated Q
        # values.
        self.board_position_log.append(board.getState().copy())

        nn_input = self.board_state_to_nn_input(board.getState())
        probs, _ = self.get_valid_probs([nn_input], self.q_net, [board])
        probs = probs[0]
        # print(probs)
        # print(type(probs))
        # print(probs.shape)
        # input()
        # print(probs)
        # Most of the time our next move is the one with the highest probability after removing all illegal ones.
        # Occasionally, however we randomly chose a random move to encourage exploration
        if (self.training is True) and \
                ((self.game_counter < self.pre_training_games) or (np.random.rand(1) < self.random_move_prob)):
            available = []
            for index in range(6):
                if probs[index] != -1.0:
                    available.append(index)
            randomOne = random.randint(0,len(available)-1)
            move = available[randomOne]
        else:
            move = np.argmax(probs)
        # We record the action we selected as well as the Q values of the current state for later use when
        # adjusting NN weights.
        self.action_log.append(move)

        # We execute the move and return the result
        board.makeMove(move)
        return board.getState(), board.isOver()

    def final_result(self, board):
        """
        This method is called once the game is over. If `self.training` is True, we execute a training run for
        the Neural Network.
        :param result: The result of the game that just finished.
        """
        if board.myMarbles>board.opMarbles:
            reward = self.win_value + self.myMarbles - self.opMarbles
        elif board.myMarbles == board.opMarbles:
            reward = self.draw_value
        else:
            reward = self.loss_value + self.myMarbles-self.opMarbles
        self.game_counter += 1
        self.add_game_to_replay_buffer(reward)

        # If we are in training mode we run the optimizer.
        if self.training and (self.game_counter > self.pre_training_games):

            batch_third = self.batch_size // 3
            train_batch = self.replay_buffer_win.sample(batch_third)
            train_batch.extend(self.replay_buffer_loss.sample(batch_third))
            train_batch.extend(self.replay_buffer_draw.sample(batch_third))
            train_batch = np.array(train_batch)

            #
            # Let's compute the target q values for all non terminal move
            # We extract the resulting state, run it through the target net work and
            # get the maximum q value (of all valid moves)
            next_states = [s[2] for s in train_batch if s[2] is not None]
            # print('current board\n', board)
            # print('next_states', next_states)
            target_qs = []

            if len(next_states) > 0:
                firstInput = [self.board_state_to_nn_input(s) for s in next_states]
                # print(firstInput)
                firstInput = np.asarray(firstInput).reshape(20, 1,2,6)[0]
                # print(firstInput.shape)
                # for i in next_states:
                #     print(i[0])
                #     print(i[1])
                #     input()
                probs, qvals = self.get_valid_probs(firstInput,
                                                    self.target_net, [Board(s[0], s[1]) for s in next_states], True)
                # print(probs)
                # print(qvals)
                # input()
                probs=probs[0]
                qvals=qvals[0]
                # print(qvals)
                i = 0
                for t in train_batch:
                    if t[2] is not None:
                        # print(t[2])
                        # print(probs)
                        # input()
                        max_move = np.argmax(probs)
                        max_qval = qvals[max_move]
                        target_qs.append(max_qval * self.reward_discount)
                        i += 1
                    else:
                        target_qs.append(t[3])

                if i != len(next_states):
                    ("Something wrong here!!!")
            else:
                target_qs.extend(train_batch[:, 6])

            # We convert the input states we have recorded to feature vectors to feed into the training.
            nn_input = [self.board_state_to_nn_input(x[0]) for x in train_batch]
            actions = train_batch[:, 1]

            # We run the training step with the recorded inputs and new Q value targets.
            # print(self.q_net.merge.shape)
            # print(self.q_net.train_step.shape)
            # print(np.asarray([self.q_net.merge, self.q_net.train_step]).shape)
            # print(self.q_net.input_positions.shape)
            # print(nn_input.shape)
            # print(self.q_net.target_q.shape)
            # print(target_qs.shape)
            # print(self.q_net.actions.shape)
            # print(actions.shape)
            # print(type(nn_input))
            summary, _ = TFSN.get_session().run([self.q_net.merge, self.q_net.train_step],
                                                feed_dict={self.q_net.input_positions: np.asarray(nn_input).reshape(20,1,2,6),
                                                           self.q_net.target_q: target_qs,
                                                           self.q_net.actions: actions})
            self.random_move_prob *= self.random_move_decrease

            if self.writer is not None:
                self.writer.add_summary(summary, self.game_counter)
                summary = tf.Summary(value=[tf.Summary.Value(tag='Random_Move_Probability',
                                                             simple_value=self.random_move_prob)])
                self.writer.add_summary(summary, self.game_counter)

            TFSN.get_session().run(self.graph_copy_op)  


tf.reset_default_graph()

nnplayer = deepPlayer("QLearner1")
rndplayer = RandomPlayer()

TFSN.set_session(tf.Session())
TFSN.get_session().run(tf.global_variables_initializer())

game_number, p1_wins, p2_wins, draws = evaluate_players(rndplayer, nnplayer,games_per_battle=1000, num_battles=5)

p = plt.plot(game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')

plt.show()
TFSN.set_session(None)
