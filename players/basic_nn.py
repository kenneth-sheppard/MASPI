import copy
import random

import tensorflow as tf

import game_engine.action_space as action_space
import game_engine.game_engine as game_engine

from game_engine.player import Player
from tensorflow import keras


class BasicNeuralNetPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Basic Neural Net'
        self.model = keras.models.load_model('recent_model')

    def __evaluate_game_state(self, game_state):
        state = game_state.get_numerical_representation()
        reshaped_state = tf.reshape(state, (1, 1302))
        values = self.model.predict(reshaped_state, verbose=0)[0]

        return values[self.id]
    #
    # def make_import_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         game_state = action_space.hypothetical_import(choice=option, game_state=game_state)
    #         new_eval = self.__evaluate_game_state(game_state=game_state)
    #         game_state = action_space.reverse_import(choice=option, game_state=game_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
    #     # return options[int(random.random() * len(options))]
    #
    # def make_maneuver_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         game_state = action_space.hypothetical_move_piece(command=option, game_state=game_state)
    #         new_eval = self.__evaluate_game_state(game_state=game_state)
    #         game_state = action_space.reverse_move_piece(command=option, game_state=game_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
    #     # return options[int(random.random() * len(options))]
    #
    # def make_battle_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         game_state = action_space.do_battle(choice=option, game_state=game_state)
    #         new_eval = self.__evaluate_game_state(game_state=game_state)
    #         game_state = action_space.reverse_battle(choice=option, game_state=game_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
    #
    # def make_rondel_choice(self, options, engine_game):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         engine_game = game_engine.potential_advance(option, engine_game)
    #         new_eval = self.__evaluate_game_state(engine_game.state)
    #         engine_game = game_engine.reverse_advance(option, engine_game)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
    #
    # def make_factory_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         game_state = action_space.hypothetical_factory(option, game_state)
    #         new_eval = self.__evaluate_game_state(game_state)
    #         game_state = action_space.reverse_factory(option, game_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
    #
    # def make_investment_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         game_state = action_space.hypothetical_investment(choice=option, game_state=game_state)
    #         new_eval = self.__evaluate_game_state(game_state=game_state)
    #         game_state = action_space.reverse_investment(choice=option, game_state=game_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
