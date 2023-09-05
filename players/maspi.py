
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
        self.maspi_interface = None

    def __evaluate_game_state(self, game_state, action):
        if self.maspi_interface is None:
            self.maspi_interface = MASPIface(initial_game_state=game_state, initial_action=action)

        self.maspi_interface.send_state(game_state=game_state, action=action)

        return self.maspi_interface.get_eval()

    def make_import_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_import(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state, 'Import')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_maneuver_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_move_piece(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state, 'Maneuver')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_battle_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.do_battle(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state, 'Battle')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_rondel_choice(self, options, engine_game):
        best_option = None
        best_value = None
        for option in options:
            new_engine = game_engine.potential_advance(option, copy.deepcopy(engine_game))
            new_eval = self.__evaluate_game_state(new_engine.state, 'Rondel')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_factory_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_factory(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state, 'Factory')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option

    def make_investment_choice(self, options, game_state):
        best_option = None
        best_value = None
        for option in options:
            new_state = action_space.hypothetical_investment(option, copy.deepcopy(game_state))
            new_eval = self.__evaluate_game_state(new_state, 'Investor')
            if best_option is None or new_eval > best_value:
                best_value = new_eval
                best_option = option

        return best_option


class MASPIface:
    def __init__(self, initial_game_state, initial_action):
        self.maspi_pile = InvestorManager(initial_game_state)
        self.game_state = initial_game_state
        self.action = initial_action
        self.up_to_date = False
        self.maspi_response = None

    def send_state(self, game_state, action):
        self.maspi_pile.receive_down(new_state={'game_state': game_state, 'action': action})

    def get_eval(self):
        if self.up_to_date:
            self.up_to_date = False
            return self.maspi_response
        raise RuntimeError('The Player asked for their MASPI evaluation too early!')

    def receive_up(self, maspi_response):
        self.up_to_date = True
        self.maspi_response = maspi_response


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

        return value

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
        new_state['eval'] = self.inner_evaluation()
        self.maneuver_collector.receive_up(new_state)

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        # Aggressiveness
        # Carelessness
        if new_state['action'] == 'Update':
            self.aggressiveness = new_state.get('aggressiveness')
            self.carelessness = new_state.get('carelessness')
        elif new_state['action'] == 'Maneuver':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Factory':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Import':
            # @TODO fill this in
            pass
        else:
            raise RuntimeError('Unexpected action passed to the Territory Agent')


class ManeuverCollector(MASPIPart):
    # When passed a set of choices for moves, choose a territory to start with
    # Then for each end territory destination query the appropriate Territory Agent
    # Choose the one with the maximum value
    # Since each move is independent of every other one (mostly) we don't need to calculate the full turn right
    # from the outset and can instead break it down in this more efficient fashion

    def __init__(self, game_state):
        """

        """
        super().__init__()
        self.name = 'Maneuver Collector'
        self.violence = 1
        self.expansiveness = 1
        self.set_of_territory_agents = {}
        self.set_of_evaluations = []
        for territory in game_state.get_territories().values():
            self.set_of_territory_agents[territory.get_name()] = TerritoryAgent(territory, self)

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
            t.receive_down(
                {
                    'aggressiveness': self.expansiveness - self.violence,
                    'carelessness': self.violence - self.expansiveness
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
        if new_state['action'] == 'Update':
            self.expansiveness = new_state['expansiveness']
            self.violence = new_state['violence']
        elif new_state['action'] == 'Maneuver':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Factory':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Import':
            # @TODO fill this in
            pass
        else:
            raise RuntimeError('Unexpected action passed to the Maneuver Collector')

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
        """

        :param space:
        :return:
        """
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
        """

        :param num_to_advance:
        :return:
        """
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
        if new_state['action'] == 'Update':
            self.money_needs = new_state['money']
            self.army_needs = new_state['army']
            self.expand_needs = new_state['expand']
            self.get_money = new_state['g_money']
            self.spend_money = new_state['s_money']
            self.get_units = new_state['g_units']
            self.get_power = new_state['g_power']
            self.cost_per_space = 1 + new_state['country_power']
        elif new_state['action'] == 'Rondel':
            # @TODO fill this in
            pass
        else:
            raise RuntimeError('Unexpected action passed to Rondel Manager')

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

    def __init__(self, game_state):
        """

        """
        super().__init__()
        self.name = 'Military Manager'
        self.flags = None
        self.units = None
        self.priority = None
        self.territory_manager = ManeuverCollector(game_state)

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
        new_state['expansiveness'] = (15 - self.flags) + self.units + self.priority,
        new_state['violence'] = self.flags + self.units + (15 - self.priority)
        self.territory_manager.receive_down(new_state)

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
        self.priority = new_state['priority']
        self.flags = new_state['game_state'].active_country.get_placed_flags()
        self.units = new_state['game_state'].active_country.get_placed_units()

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass


class InvestorManager(MASPIPart):

    def __init__(self, game_state):
        """

        """
        super().__init__()
        self.name = 'Investor Manager'
        self.current_evaluations = {
            'Russia': CountryEvaluator('Russia'),
            'China': CountryEvaluator('China'),
            'India': CountryEvaluator('India'),
            'Brazil': CountryEvaluator('Brazil'),
            'United States': CountryEvaluator('United States'),
            'European Union': CountryEvaluator('European Union')
        }
        self.military_manager = MilitaryManager(game_state)
        self.rondel_manager = RondelManager()
        self.game_state = game_state

    def inner_evaluation(self):
        """

        """
        for country in self.game_state.get_countries():
            c_val = -10
            for bond in country.get_bonds():
                if bond.get_owner() == self.player:
                    c_val += bond.get_cost()
                if bond.get_owner() is not None:
                    c_val += 2
            if country.get_country_controller() == self.player:
                c_val += 5
            c_val += 2 ** helper.power_chart(country.get_power())
            return c_val

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass Down
        self.military_manager.receive_down(
            {
                'game_state': self.game_state,
                # TODO: Define this
                'priority': 0
            }
        )
        for country_evaluator in self.current_evaluations.values():
            country_evaluator.receive_down(
                {
                    'game_state': self.game_state
                }
            )

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass Up
        # Parse what to pass using the information in the game state
        if new_state['action'] == 'Maneuver':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Factory':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Import':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Investor':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Rondel':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Battle':
            # @TODO fill this in
            pass
        else:
            # Go cry or something because we didn't expect this
            raise RuntimeError('The action passed to the InvestorManager was not recognized')

    def receive_down(self, new_state):
        """
        From above will be the new game_state for analysis and
        an action that is going to be taken (rondel, battle, maneuver, etc.)
        :param new_state:
        """
        # Expected from above
        if new_state['action'] == 'Maneuver':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Factory':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Import':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Investor':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Rondel':
            # @TODO fill this in
            pass
        elif new_state['action'] == 'Battle':
            # @TODO fill this in
            pass
        else:
            # Go cry or something because we didn't expect this
            raise RuntimeError('The action passed to the InvestorManager was not recognized')
        self.pass_down(new_state)

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        # Anything we get should be passed up to the Agent above us
        self.pass_up(new_state=new_state)


class CountryEvaluator(MASPIPart):

    def __init__(self, country):
        """

        """
        super().__init__()
        self.name = 'Country Evaluator'
        self.total_investment = None
        self.relative_power = None
        self.tax_increase = None
        self.country = country

    def inner_evaluation(self):
        """

        """
        return self.total_investment + self.relative_power * self.tax_increase

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
        investments = 0
        for bond in new_state['game_state'].get_country(self.country).get_bonds():
            if bond.get_owner() is not None:
                investments += bond.get_interest_rate()
        self.total_investment = investments
        rel_pow = 0
        for country in new_state['game_state'].get_countries():
            if new_state['game_state'].get_country(self.country).get_power() >= country.get_power():
                rel_pow += 1
        self.relative_power = rel_pow
        self.tax_increase = new_state['game_state'].get_country(self.country).get_tax_payout()
        self.pass_up(new_state)

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass
