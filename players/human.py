import random

from game_engine.player import Player


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Human'

    def make_import_choice(self, options, game_state):
        self.banana = 2
        for i in enumerate(options):
            print('{} - Tanks: {}, Ships: {}, Territory: {}'.format(i[0], i[1][0].get('Tanks'), i[1][0].get('Ships'),
                                                                    i[1][1]))

        return options[int(input('Choose: '))]

    def make_maneuver_choice(self, options, game_state):
        self.banana = 3
        for i in enumerate(options):
            if type(i[1][2]) is list:
                print(f'{i[0]} - {i[1][0]} from {i[1][1]} to {i[1][2][0]}')
            else:
                print(f'{i[0]} - {i[1][0]} from {i[1][1]} to {i[1][2]}')

        return options[int(input('Choose: '))]

    def make_battle_choice(self, options, game_state):
        self.banana = 4
        for i in enumerate(options):
            print(f'{i[0]} - {i[1]}')

        return options[int(input('Choose: '))]

    def make_rondel_choice(self, options, game_engine):
        self.banana = 5
        for i in enumerate(options):
            print(f'{i[0]} - {i[1][1]}')

        return options[int(input('Choose: '))]

    def make_factory_choice(self, options, game_state):
        self.banana = 6
        for i in enumerate(options):
            print(f'{i[0]} - {i[1]}')

        return options[int(input('Choose: '))]

    def make_investment_choice(self, options, game_state):
        self.banana = 7
        for i in enumerate(options):
            print(f'{i[0]} - {i[1]}')

        return options[int(input('Choose: '))]
