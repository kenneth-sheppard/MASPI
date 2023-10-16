import copy
import random
import game_engine.action_space as action_space
import game_engine.game_engine as game_engine
import tensorflow as tf
from tensorflow import keras

id_count = 0


class Player:
    def __init__(self):
        """
        The player object represents an autonomous acting player and may link to external calculators that make decisions
        """
        self.bonds = []
        self.controlled_countries = []
        self.money = 0
        self.has_investor_card = False
        self.is_swiss_bank = False
        self.banana = 0
        self.type = 'Human'
        global id_count
        self.id = id_count % 6
        id_count = (id_count + 1) % 6

    def __evaluate_game_state(self, game_state):
        return random.random()

    def get_id(self):
        """
        getter for the id of the player
        :return: int - between 0 and 5
        """
        return self.id

    def get_bonds(self):
        """
        getter for the set of bonds held by the player
        :return: List - the list of bonds
        """
        return self.bonds

    def get_type(self):
        """
        getter for the type of player, Human or otherwise
        :return: String - the type of player
        """
        return self.type

    def add_bond(self, bond):
        """
        add a bond to the set of bonds held by a player
        :param bond: Bond - the bond to be added
        """
        self.bonds.append(bond)

    def swap_bonds(self, bond_in, bond_out):
        """
        add a bond and remove another bond.
        :param bond_in: Bond - the bond to be added
        :param bond_out: Bond - the bond to be removed
        """
        self.bonds.remove(bond_out)
        self.bonds.append(bond_in)

    def get_investment_in_country(self, country):
        """
        getter for the level of investment of a player in a country.
        :param country: Country - the country to be counted
        :return: int - the amount, in cost, currently invested in that country
        """
        amount = 0
        for bond in self.bonds:
            if bond.get_country() == country:
                amount += bond.get_cost()

        return amount

    def get_controlled_countries(self):
        """
        getter for the list of countries being run by this player
        :return: List - the list of countries run by this player
        """
        return self.controlled_countries

    def add_controlled_country(self, country):
        """
        add a country to the list of countries controlled by this player
        :param country: Country - the country to add
        """
        self.controlled_countries.append(country)

    def remove_controlled_country(self, country):
        """
        remove a country from the list of countries controlled by this player
        :param country: Country - the country to remove
        """
        self.controlled_countries.remove(country)

    def reset_controlled_countries(self):
        """
        set the list of controlled countries to an empty list
        """
        self.controlled_countries = []

    def get_money(self):
        """
        getter for the amount of money held by the player
        :return: int - the amount
        """
        return self.money

    def add_money(self, amount):
        """
        add money to the current held pool
        :param amount: int - the amount to add
        """
        self.money += amount

    def remove_money(self, amount):
        """
        remove money from the current held pool
        :param amount: int - the amount to remove
        """
        self.money -= amount

    def get_has_investor_card(self):
        """
        getter for if the investor card is currently held by this player
        :return: boolean - True if held, False otherwise
        """
        return self.has_investor_card

    def set_has_investor_card(self, has_card):
        """
        setter for if the investor card is currently held by this player
        :param has_card: boolean - True if held, False otherwise
        """
        self.has_investor_card = has_card

    def get_is_swiss_bank(self):
        """
        getter for if this player is a swiss banker
        :return: boolean
        """
        return self.is_swiss_bank

    def set_is_swiss_bank(self, is_swiss):
        """
        setter for if this player is a swiss banker
        :param is_swiss: boolean
        """
        self.is_swiss_bank = is_swiss

    def get_worth(self):
        """
        calculate the worth of the player by adding the value of their bonds to the money they hold
        :return: int - the worth
        """
        value = self.get_money()
        for bond in self.get_bonds():
            value += bond.get_value()

        return value

    def buy_bond(self, bond_to_buy, bond_to_sell=None):
        """
        adjust money held by the amount the bond is worth potentially modified by a bond being traded in
        :param bond_to_buy:
        :param bond_to_sell:
        """
        if bond_to_sell is not None:
            self.money += bond_to_sell.get_cost()
            self.bonds.remove(bond_to_sell)
            bond_to_sell.set_owner(None)

        self.money -= bond_to_buy.get_cost()
        bond_to_buy.get_country().add_money(bond_to_buy.get_cost())
        if bond_to_sell is not None:
            bond_to_sell.get_country().remove_money(bond_to_sell.get_cost())
        bond_to_buy.set_owner(self)
        self.bonds.append(bond_to_buy)

    def sell_bond(self, bond_to_buy, bond_to_sell=None):
        """
        adjust money held by the amount the bond is worth potentially modified by a bond being traded in
        :param bond_to_buy:
        :param bond_to_sell:
        """
        if bond_to_sell is not None:
            self.money -= bond_to_sell.get_cost()
            bond_to_sell.set_owner(self)
            self.bonds.append(bond_to_sell)

        self.money += bond_to_buy.get_cost()
        if bond_to_sell is not None:
            bond_to_sell.get_country().add_money(bond_to_sell.get_cost())
        bond_to_buy.get_country().remove_money(bond_to_buy.get_cost())
        bond_to_buy.set_owner(None)
        self.bonds.remove(bond_to_buy)

    def make_import_choice(self, options, game_state):
        """
        make a choice about where to import
        :param options: List - a set of move options
        :param game_state: GameState - the current game state
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            game_state = action_space.hypothetical_import(choice=option, game_state=game_state)
            new_eval = self.__evaluate_game_state(game_state=game_state)
            game_state = action_space.reverse_import(choice=option, game_state=game_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_maneuver_choice(self, options, game_state):
        """
        make a choice about where to maneuver
        :param options: List - a set of move options
        :param game_state: GameState - the current game state
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            game_state = action_space.hypothetical_move_piece(command=option, game_state=game_state)
            new_eval = self.__evaluate_game_state(game_state=game_state)
            game_state = action_space.reverse_move_piece(command=option, game_state=game_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_battle_choice(self, options, game_state):
        """
        make a choice about whether to battle
        :param options: List - a set of move options
        :param game_state: GameState - the current game state
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            game_state = action_space.do_battle(choice=option, game_state=game_state)
            new_eval = self.__evaluate_game_state(game_state=game_state)
            game_state = action_space.reverse_battle(choice=option, game_state=game_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_rondel_choice(self, options, engine_game):
        """
        make a choice about how far to advance on the rondel
        :param options: List - a set of move options
        :param engine_game: GameEngine - the current game engine
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            engine_game = game_engine.potential_advance(option, engine_game)
            new_eval = self.__evaluate_game_state(engine_game.state)
            engine_game = game_engine.reverse_advance(option, engine_game)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_factory_choice(self, options, game_state):
        """
        make a choice about where to put a factory
        :param options: List - a set of move options
        :param game_state: GameState - the current game state
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            game_state = action_space.hypothetical_factory(option, game_state)
            new_eval = self.__evaluate_game_state(game_state)
            game_state = action_space.reverse_factory(option, game_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_investment_choice(self, options, game_state):
        """
        make a choice about which bond to buy
        :param options: List - a set of move options
        :param game_state: GameState - the current game state
        :return: List - one element from options
        """
        best_option = None
        best_value = None
        for option in options:
            game_state = action_space.hypothetical_investment(choice=option, game_state=game_state)
            new_eval = self.__evaluate_game_state(game_state=game_state)
            game_state = action_space.reverse_investment(choice=option, game_state=game_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def to_numbers(self):
        """
        convert the player into the relevant encodings
        :return: List - [held cash, is swiss bank (0 or 1)]
        """
        return [self.money, int(self.is_swiss_bank)]


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


class GreedyPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Greedy'

    def __evaluate_game_state(self, game_state):
        value = 0
        for player in game_state.get_players():
            if player.get_id() is self.id:
                value += player.get_worth()
            else:
                # value -= player.get_worth()
                pass

        return value

    def make_import_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_import(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_maneuver_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_move_piece(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_battle_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.do_battle(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_rondel_choice(self, options, engine_game):
        best_option = None
        best_value = None
        for option in options:
            new_engine = game_engine.potential_advance(option, copy.deepcopy(engine_game))
            new_eval = self.__evaluate_game_state(new_engine.state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_factory_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_factory(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_investment_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_investment(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option


class BasicNeuralNetPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Basic Neural Net'
        self.model = keras.models.load_model('recent_model')

    def __evaluate_game_state(self, game_state):
        state = game_state.get_numerical_representation()
        reshaped_state = tf.reshape(state, (1, 1302))
        values = self.model.predict(reshaped_state)[0]

        return values[self.id]

    def make_import_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_import(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_maneuver_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_move_piece(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_battle_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.do_battle(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_rondel_choice(self, options, engine_game):
        best_option = None
        best_value = None
        for option in options:
            new_engine = game_engine.potential_advance(option, copy.deepcopy(engine_game))
            new_eval = self.__evaluate_game_state(new_engine.state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_factory_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_factory(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_investment_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_investment(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state)
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option
