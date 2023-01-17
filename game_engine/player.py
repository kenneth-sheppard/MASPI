import random


class Player:
    def __init__(self):
        self.bonds = []
        self.controlled_countries = []
        self.money = 0
        self.has_investor_card = False
        self.is_swiss_bank = False
        self.banana = 0

    def get_bonds(self):
        return self.bonds

    def add_bond(self, bond):
        self.bonds.append(bond)

    def swap_bonds(self, bond_in, bond_out):
        self.bonds.remove(bond_out)
        self.bonds.append(bond_in)

    def get_controlled_countries(self):
        return self.controlled_countries

    def add_controlled_country(self, country):
        self.controlled_countries.append(country)

    def remove_controlled_country(self, country):
        self.controlled_countries.remove(country)

    def reset_controlled_countries(self):
        self.controlled_countries = []

    def get_money(self):
        return self.money

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        self.money -= amount

    def get_has_investor_card(self):
        return self.has_investor_card

    def set_has_investor_card(self, has_card):
        self.has_investor_card = has_card

    def get_is_swiss_bank(self):
        return self.is_swiss_bank

    def set_is_swiss_bank(self, is_swiss):
        self.is_swiss_bank = is_swiss

    def get_worth(self):
        value = self.get_money()
        for bond in self.get_bonds():
            value += bond.get_value()

        return value

    def buy_bond(self, bond_to_buy, bond_to_sell=None):
        if bond_to_sell is not None:
            self.money += bond_to_sell.get_cost()
            bond_to_sell.set_owner(None)

        self.money -= bond_to_buy.get_cost()
        bond_to_buy.set_owner(self)
        self.bonds.append(bond_to_buy)

    def make_choice(self, options, game_state):
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

    def make_rondel_choice(self, options, game_state):
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


class RandPlayer(Player):
    def __init__(self):
        super().__init__()

    def make_choice(self, options, game_state):
        self.banana = 2

        return options[int(random.random() * len(options))]

    def make_maneuver_choice(self, options, game_state):
        self.banana = 3

        return options[int(random.random() * len(options))]

    def make_battle_choice(self, options, game_state):
        self.banana = 4

        return options[int(random.random() * len(options))]

    def make_rondel_choice(self, options, game_state):
        self.banana = 5

        return options[int(random.random() * len(options))]

    def make_factory_choice(self, options, game_state):
        self.banana = 6

        return options[int(random.random() * len(options))]

    def make_investment_choice(self, options, game_state):
        self.banana = 7

        return options[int(random.random() * len(options))]
