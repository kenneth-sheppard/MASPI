import random

from game_engine.player import Player


class RandPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Random'

    def make_import_choice(self, options, game_state):
        self.banana = 2

        return options[int(random.random() * len(options))]

    def make_maneuver_choice(self, options, game_state):
        self.banana = 3

        return options[int(random.random() * len(options))]

    def make_battle_choice(self, options, game_state):
        self.banana = 4

        return options[int(random.random() * len(options))]

    def make_rondel_choice(self, options, game_engine):
        self.banana = 5

        return options[int(random.random() * len(options))]

    def make_factory_choice(self, options, game_state):
        self.banana = 6

        return options[int(random.random() * len(options))]

    def make_investment_choice(self, options, game_state):
        self.banana = 7

        return options[int(random.random() * len(options))]