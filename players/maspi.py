
import copy
import math

import game_engine.action_space as action_space
import game_engine.game_engine as game_engine
from game_engine import helper, rondel

from game_engine.player import Player


class PlayerMASPI(Player):
    def __init__(self):
        super().__init__()
        self.type = 'MASPI Player'

    def __evaluate_game_state(self, game_state):
        return 0

    def propagate_game_state_information(self, game_state):
        new_state = {}
        new_state['g_money'] = None

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


class MASPIPart:

    def __init__(self):
        """

        """
        self.name = 'Basic Part'
        self.player = None

    def inner_evaluation(self):
        """

        """
        pass

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        pass

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        pass

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        pass


class TerritoryAgent(MASPIPart):

    def __init__(self, territory, maneuver_collector):
        """

        :param territory:
        """
        super().__init__()
        self.name = 'Territory Agent'
        self.territory = territory
        self.neighbors = []
        self.aggressiveness = 1
        self.carelessness = 1
        self.maneuver_collector = maneuver_collector

    def territory_value(self):
        """

        """
        # owned + neighbor_owned
        # owned = 10 * has_my_flag + has_my_pieces - 2 * another_flag - has_their_pieces
        # Aggressiveness -> another_flag / 3 | neutral + 5
        # Carelessness -> has_their_pieces * -1
        value = 10 * (self.territory.get_territory_controller() == self.player.get_id())
        value += 1 * (self.territory.get_tanks().as_list()[self.player.get_id()] != 0 or
                      self.territory.get_ships().as_list()[self.player.get_id()] != 0)
        for adjacent in self.neighbors:
            value -= 2 * (adjacent.get_territory_controller() != self.player.get_id())
            value -= 1 * (sum(adjacent.get_tanks().as_list().pop(self.player.get_id())) != 0 or
                          sum(adjacent.get_ships().as_list().pop(self.player.get_id())) != 0)

    def add_neighbor(self, n):
        """

        :param n:
        """
        self.neighbors.append(n)

    def inner_evaluation(self):
        """

        :return:
        """
        return self.territory_value()

    def pass_up(self, new_state):
        """

        :param new_state:
        :return:
        """
        # Get all adjacent territories
        # For each adjacent territory query value
        # Calculate own value
        # Identify the best location for each unit in territory
        # Probably best to loop for number of units present times
        # Return unit plans
        self.maneuver_collector.recieve_up({'eval': self.inner_evaluation()})

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        # Aggressiveness
        # Carelessness
        self.aggressiveness = new_state.get('aggressiveness')
        self.carelessness = new_state.get('carelessness')


class ManeuverCollector(MASPIPart):
    # When passed a set of choices for moves, choose a territory to start with
    # Then for each end territory destination query the appropriate Territory Agent
    # Choose the one with the maximum value
    # Since each move is independent of every other one (mostly) we don't need to calculate the full turn right
    # from the outset and can instead break it down in this more efficient fashion

    def __init__(self):
        """

        """
        super().__init__()
        self.name = 'Maneuver Collector'
        self.violence = 1
        self.expansiveness = 1
        self.set_of_territory_agents = []
        self.set_of_evaluations = []
        # TODO Fill this

    def inner_evaluation(self):
        """

        """
        pass

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass down
        # Aggressiveness
        # Carelessness
        for t in self.set_of_territory_agents:
            t.pass_down(
                {
                    'aggressiveness': 0,
                    'carelessness': 0
                }
            )

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass that to the rondel manager maybe?
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        # Violence
        # Expansiveness
        self.expansiveness = new_state['expansiveness']
        self.violence = new_state['violence']

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        # A bunch of territory agent evaluations
        # Select the best priorities
        self.set_of_evaluations.append(new_state['eval'])


class RondelManager(MASPIPart):

    def __init__(self):
        """

        """
        super().__init__()
        self.name = 'Rondel Manager'
        self.money_needs = 1
        self.army_needs = 1
        self.expand_needs = 1

        self.get_money = 1
        self.spend_money = 1
        self.get_units = 1
        self.default_value = 20
        self.get_power = 1

        self.cost_per_space = 1

        self.active_country = None

    def space_eval(self, space):
        if space.get_name() == 'Investor':
            return self.get_money + self.spend_money
        elif space.get_name() == 'Import':
            return self.get_units + self.spend_money
        elif space.get_name() == 'Production':
            return self.get_units + self.default_value
        elif space.get_name() == 'Maneuver':
            return self.get_power + self.default_value
        elif space.get_name() == 'Taxation':
            return self.get_power + self.get_money
        elif space.get_name() == 'Factory':
            return self.get_units + self.spend_money
        else:
            # Space type is unknown
            return None

    def advance(self, num_to_advance):
        return rondel.hypothetical_advance(self.active_country.get_rondel_space(), num_to_advance)

    def inner_evaluation(self):
        """

        """
        options = {}
        for num_to_advance in range(1, 7):
            options[num_to_advance] = self.space_eval(self.advance(num_to_advance)) + .5 * \
                                      (math.pow(num_to_advance * self.cost_per_space, 2))

        return options

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass Down
        pass

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # I don't think anything needs to be passed up
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        # Make money
        # Build force
        # Expand Territory
        self.money_needs = new_state['money']
        self.army_needs = new_state['army']
        self.expand_needs = new_state['expand']
        self.get_money = new_state['g_money']
        self.spend_money = new_state['s_money']
        self.get_units = new_state['g_units']
        self.get_power = new_state['g_power']
        self.cost_per_space = 1 + new_state['country_power']

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        # The way to perform the maneuver action
        pass

    # Spaces on the Rondel
    # Maneuver - Expand territory
    # Production - Build force
    # Import - Build force
    # Taxation - Make money
    # Investor - Make money
    # Factory - Build force
    def select_space(self):
        """

        """
        pass


class MilitaryManager(MASPIPart):

    def __init__(self):
        """

        """
        super().__init__()
        self.name = 'Military Manager'

    def inner_evaluation(self):
        """

        """
        pass

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass Down
        # Violence
        # Expansiveness
        pass

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # I don't think anything needs to be passed up
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        pass

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass


class InvestorManager(MASPIPart):

    def __init__(self):
        """

        """
        super().__init__()
        self.name = 'Investor Manager'
        self.countries = None
        self.current_evaluations = {
            'Russia': None,
            'China': None,
            'India': None,
            'Brazil': None,
            'United States': None,
            'European Union': None
        }

    def inner_evaluation(self):
        """

        """
        for country in self.countries:
            c_val = -10
            for bond in country.get_bonds():
                if bond.get_owner() == self.player:
                    c_val += bond.get_cost()
                if bond.get_owner() is not None:
                    c_val += 2
            if country.get_country_controller() == self.player:
                c_val += 5
            c_val += 2 ** helper.power_chart(country.get_power())
            self.current_evaluations[country.get_name()] = c_val

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass Down
        pass

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass Up
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        pass

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass


class CountryEvaluator(MASPIPart):

    def __init__(self):
        """

        """
        super().__init__()
        self.name = 'Country Evaluator'

    def inner_evaluation(self):
        """

        """
        pass

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass Down
        pass

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass Up
        pass

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        pass

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass
