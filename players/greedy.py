import copy
import random

import game_engine.action_space as action_space
import game_engine.game_engine as game_engine

from game_engine.player import Player


class GreedyPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Greedy'

    def evaluate_game_state(self, game_state):
        value = 0
        for player in game_state.get_players():
            if player.get_id() is self.id:
                value += player.get_worth()
            else:
                # value -= player.get_worth()
                pass

        return value
    #
    # def make_import_choice(self, options, game_state):
    #     # best_option = None
    #     # best_value = None
    #     # for option in options:
    #     #     new_state = action_space.hypothetical_import(option, copy.deepcopy(game_state))
    #     #     new_eval = self.__evaluate_game_state(new_state)
    #     #     if best_option is None or new_eval > best_value:
    #     #         best_value = new_eval
    #     #         best_option = option
    #     #
    #     # return best_option
    #     return options[int(random.random() * len(options))]
    #
    # def make_maneuver_choice(self, options, game_state):
    #     # best_option = None
    #     # best_value = None
    #     # for option in options:
    #     #     new_state = action_space.hypothetical_move_piece(option, copy.deepcopy(game_state))
    #     #     new_eval = self.__evaluate_game_state(new_state)
    #     #     if best_option is None or new_eval > best_value:
    #     #         best_value = new_eval
    #     #         best_option = option
    #     #
    #     # return best_option
    #     return options[int(random.random() * len(options))]
    #
    # def make_battle_choice(self, options, game_state):
    #     best_option = None
    #     best_value = None
    #     for option in options:
    #         new_state = action_space.do_battle(option, copy.deepcopy(game_state))
    #         new_eval = self.__evaluate_game_state(new_state)
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
    #         new_engine = game_engine.potential_advance(option, copy.deepcopy(engine_game))
    #         new_eval = self.__evaluate_game_state(new_engine.state)
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
    #         new_state = action_space.hypothetical_factory(option, copy.deepcopy(game_state))
    #         new_eval = self.__evaluate_game_state(new_state)
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
    #         new_state = action_space.hypothetical_investment(option, copy.deepcopy(game_state))
    #         new_eval = self.__evaluate_game_state(new_state)
    #         if best_option is None or new_eval > best_value:
    #             best_value = new_eval
    #             best_option = option
    #
    #     return best_option
