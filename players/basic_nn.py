import copy
import random

import tensorflow as tf

import game_engine.action_space as action_space
import game_engine.game_engine as game_engine

from game_engine.player import Player
from tensorflow import keras

basic_model = None


class BasicNeuralNetPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Basic Neural Net'
        global basic_model
        keras.backend.clear_session()
        basic_model = keras.models.load_model('models/BasicNeuralNetPlayerModel/recent_model')

    def evaluate_game_state(self, game_state):
        state = game_state.get_numerical_representation()
        reshaped_state = tf.reshape(state, (1, 1302))
        values = basic_model.predict(reshaped_state, verbose=0)[0]

        return values[self.id]


fifty_games_model = None


class FiftyGamesNeuralNetPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Fifty Games Neural Net'
        global fifty_games_model
        fifty_games_model = keras.models.load_model('models/50_games')

    def evaluate_game_state(self, game_state):
        state = game_state.get_numerical_representation()
        reshaped_state = tf.reshape(state, (1, 1302))
        values = fifty_games_model.predict(reshaped_state, verbose=0)[0]

        return values[self.id]


class FullScopeNeuralNetPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Full Scope Neural Net'
        global basic_model
        keras.backend.clear_session()
        basic_model = keras.models.load_model('scoped_model')

    def evaluate_game_state(self, game_state):
        state = game_state.get_numerical_representation()
        reshaped_state = tf.reshape(state, (1, 1302))
        values = basic_model.predict(reshaped_state, verbose=0)[0]

        return values[self.id]
