import os

from game_engine.player import Player


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Human'

    def display_basic_game_state_information(self, game_state):
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(f'Player {self.id}')
        print(f'Bonds : [ {" ".join([str(b) for b in self.bonds])} ] - Cash ${self.money}')
        print(f'Active Country is {game_state.get_active_country()}')
        print(f'${game_state.get_active_country().get_treasury()} - Treasury : '
              f'{game_state.get_active_country().get_placed_units()} - Units : '
              f'{game_state.get_active_country().get_placed_flags()} - Flags')
        print(f'{game_state.get_active_country()} controls '
              f'{" ".join([str(t) for t in game_state.get_active_country().get_controlled_neutral_territories()])}')
        for territory in game_state.get_active_country().get_home_territories():
            print(f'{territory.get_name():20} : Factory? {str(territory.has_factory()):5} '
                  f'Occupied? {str(territory.is_occupied()):5}')
        print(f'Power track - ', end='')
        for country in game_state.get_countries():
            print(f'{country.get_name()}({country.get_power()}) ', end='')
        print('\n')

    def get_user_choice(self, options):
        self.banana = 7
        while True:
            user_input = input('Choose: ')
            try:
                user_input = int(user_input)
                if 0 <= user_input < len(options):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('\b \r', end='')

        return options[user_input]

    def make_import_choice(self, options, game_state):
        self.display_basic_game_state_information(game_state=game_state)
        for i in enumerate(options):
            print('{} - Tanks: {}, Ships: {}, Territory: {}'.format(i[0], i[1][0].get('Tanks'), i[1][0].get('Ships'),
                                                                    i[1][1]))

        return self.get_user_choice(options)

    def make_maneuver_choice(self, options, game_state):
        self.display_basic_game_state_information(game_state=game_state)
        for i in enumerate(options):
            if type(i[1][2]) is list:
                print(f'{i[0]} - {i[1][0]} from {str(i[1][1])} to {str(i[1][2][0])} by way of '
                      f'{" ".join([str(t) for t in reversed(i[1][2])])}')
            else:
                print(f'{i[0]} - {i[1][0]} from {str(i[1][1])} to {str(i[1][2])}')

        return self.get_user_choice(options)

    def make_battle_choice(self, options, game_state):
        self.display_basic_game_state_information(game_state=game_state)
        for i in enumerate(options):
            print(f'{i[0]} - {i[1][0]} fights {i[1][1]} at {i[1][2]} between {i[1][3]}s')

        return self.get_user_choice(options)

    def make_rondel_choice(self, options, game_engine):
        self.display_basic_game_state_information(game_state=game_engine.get_state())
        for i in enumerate(options):
            print(f'{i[0]} - {i[1][1]}')

        return self.get_user_choice(options)

    def make_factory_choice(self, options, game_state):
        self.display_basic_game_state_information(game_state=game_state)
        for i in enumerate(options):
            print(f'{i[0]} - For {i[1][1]} in {i[1][0]}')

        return self.get_user_choice(options)

    def make_investment_choice(self, options, game_state):
        self.display_basic_game_state_information(game_state=game_state)
        for i in enumerate(options):
            print(f'{i[0]} - Buy {i[1][1]} for {i[1][0]} and trading {i[1][2]}')

        return self.get_user_choice(options)
