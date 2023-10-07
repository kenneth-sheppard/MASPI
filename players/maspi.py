
import math

from game_engine import helper, rondel

from game_engine.player import Player


class PlayerMASPI(Player):
    def __init__(self):
        super().__init__()
        self.type = 'MASPI Player'
        self.maspi_interface = None
        self.current_action = None

    def __evaluate_game_state(self, game_state):
        if self.maspi_interface is None:
            self.maspi_interface = MASPIface(initial_game_state=game_state, initial_action=self.current_action, player=self)

        self.maspi_interface.send_state(game_state=game_state, action=self.current_action)

        return self.maspi_interface.get_eval()

    def make_import_choice(self, options, game_state):
        self.current_action = 'Import'
        return super().make_import_choice(options=options, game_state=game_state)

    def make_maneuver_choice(self, options, game_state):
        self.current_action = 'Maneuver'
        return super().make_maneuver_choice(options=options, game_state=game_state)

    def make_battle_choice(self, options, game_state):
        self.current_action = 'Battle'
        return super().make_battle_choice(options=options, game_state=game_state)

    def make_rondel_choice(self, options, engine_game):
        self.current_action = 'Rondel'
        return super().make_rondel_choice(options=options, engine_game=engine_game)

    def make_factory_choice(self, options, game_state):
        self.current_action = 'Factory'
        return super().make_factory_choice(options=options, game_state=game_state)

    def make_investment_choice(self, options, game_state):
        self.current_action = 'Investor'
        return super().make_investment_choice(options=options, game_state=game_state)


class MASPIface:
    def __init__(self, initial_game_state, initial_action, player):
        self.maspi_pile = InvestorManager(player=player, game_state=initial_game_state, interface=self)
        self.game_state = initial_game_state
        self.action = initial_action
        self.up_to_date = False
        self.maspi_response = None

    def send_state(self, game_state, action):
        self.up_to_date = False
        self.maspi_pile.receive_down(new_state={'game_state': game_state, 'action': action})

    def get_eval(self):
        if self.up_to_date:
            return self.maspi_response
        raise RuntimeError('The Player asked for their MASPI evaluation too early!')

    def is_eval_ready(self):
        return self.up_to_date

    def receive_up(self, maspi_response):
        self.up_to_date = True
        self.maspi_response = maspi_response


class MASPIPart:

    def __init__(self, player):
        """

        """
        self.name = 'Basic Part'
        self.player = player

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

    def __init__(self, player, territory, maneuver_collector):
        """

        :param territory:
        """
        super().__init__(player=player)
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
            new_state['evaluation'] += self.inner_evaluation()
        elif new_state['action'] == 'Factory':
            if self.territory.has_factory():
                new_state['evaluation'] = self.inner_evaluation()
            else:
                new_state['evaluation'] = 0
        elif new_state['action'] == 'Import':
            if self.territory.get_in_country():
                new_state['evaluation'] = self.inner_evaluation()
            else:
                new_state['evaluation'] = 0
        else:
            raise RuntimeError('Unexpected action passed to the Territory Agent')
        self.pass_up(new_state=new_state)


class ManeuverCollector(MASPIPart):
    # When passed a set of choices for moves, choose a territory to start with
    # Then for each end territory destination query the appropriate Territory Agent
    # Choose the one with the maximum value
    # Since each move is independent of every other one (mostly) we don't need to calculate the full turn right
    # from the outset and can instead break it down in this more efficient fashion

    def __init__(self, player, game_state, military_manager):
        """

        """
        super().__init__(player=player)
        self.name = 'Maneuver Collector'
        self.violence = 1
        self.expansiveness = 1
        self.set_of_territory_agents = {}
        self.set_of_evaluations = []
        self.military_manager = military_manager
        for territory in game_state.get_territories().values():
            self.set_of_territory_agents[territory.get_name()] = TerritoryAgent(
                player=player, territory=territory, maneuver_collector=self
            )

    def inner_evaluation(self):
        """

        """
        count = 0
        for elem in self.set_of_evaluations:
            count += elem
        return count

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        # Pass down
        # Aggressiveness
        # Carelessness
        new_state['aggressiveness'] = self.expansiveness - self.violence
        new_state['carelessness'] = self.violence - self.expansiveness
        for t in self.set_of_territory_agents:
            t.receive_down(
                new_state=new_state
            )

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass that to the rondel manager maybe?
        new_state['evaluation'] = self.inner_evaluation()
        self.set_of_evaluations.clear()
        self.military_manager.receive_up(new_state=new_state)

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
        else:
            raise RuntimeError('Unexpected action passed to the Maneuver Collector')

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        # A bunch of territory agent evaluations
        # Select the best priorities
        self.set_of_evaluations.append(new_state['evaluation'])
        if len(self.set_of_evaluations) == len(new_state['game_state'].get_territories().keys()):
            self.pass_up(new_state=new_state)


class RondelManager(MASPIPart):

    def __init__(self, player, investment_manager):
        """

        """
        super().__init__(player=player)
        self.name = 'Rondel Manager'
        self.get_money = 1
        self.spend_money = 1
        self.get_units = 1
        self.default_value = 20
        self.get_power = 1
        self.investment_manager = investment_manager
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

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        self.investment_manager.recieve_up(new_state)

    def receive_down(self, new_state):
        """

        :param new_state:
        """
        # Expected from above
        # Make money
        # Build force
        # Expand Territory
        active_country = new_state['game_state'].get_active_country()
        if new_state['action'] == 'Update':
            self.get_money = active_country.get_tax_payout() + min(active_country.get_total_payout(),
                                                                   active_country.get_player_investments(self.player))
            self.spend_money = active_country.get_treasury() - active_country.get_total_payout()
            self.get_units = (active_country.get_tank_pool() + active_country.get_ship_pool() -
                              2 * active_country.get_placed_units())
            self.get_power = math.pow(active_country.get_tax_increase(), 2)
            self.cost_per_space = 1 + active_country.get_power()
        elif new_state['action'] == 'Rondel':
            # Pass up the evaluation of the current space the country sits upon
            new_state['evaluation'] = self.space_eval(active_country.get_rondel_space()) + self.player.get_worth() ^ 2
            self.pass_up(new_state=new_state)
        else:
            raise RuntimeError('Unexpected action passed to Rondel Manager')


class MilitaryManager(MASPIPart):

    def __init__(self, player, game_state, investor_manager):
        """

        """
        super().__init__(player=player)
        self.name = 'Military Manager'
        self.investor_manager = investor_manager
        self.flags = None
        self.units = None
        self.priority = None
        self.territory_manager = ManeuverCollector(player=player, game_state=game_state, military_manager=self)

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
        self.investor_manager.recieve_up(new_state=new_state)

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
        self.pass_up(new_state=new_state)


class InvestorManager(MASPIPart):

    def __init__(self, player, game_state, interface):
        """

        """
        super().__init__(player=player)
        self.name = 'Investor Manager'
        self.current_evaluations = {
            'Russia': 0,
            'China': 0,
            'India': 0,
            'Brazil': 0,
            'United States': 0,
            'European Union': 0
        }
        self.active_evaluation = 0
        self.country_evaluators = [
            CountryEvaluator(player=player, country='Russia', investor_manager=self),
            CountryEvaluator(player=player, country='China', investor_manager=self),
            CountryEvaluator(player=player, country='India', investor_manager=self),
            CountryEvaluator(player=player, country='Brazil', investor_manager=self),
            CountryEvaluator(player=player, country='United States', investor_manager=self),
            CountryEvaluator(player=player, country='European Union', investor_manager=self)
        ]
        self.military_manager = MilitaryManager(player=player, game_state=game_state, investor_manager=self)
        self.rondel_manager = RondelManager(player=player, investment_manager=self)
        self.game_state = game_state
        self.interface = interface

    def inner_evaluation(self):
        """

        """
        active_investments = 0
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
            active_investments += c_val * self.current_evaluations[country.get_name()]

        self.active_evaluation = active_investments

    def pass_down(self, new_state):
        """

        :param new_state:
        """
        new_state['priority'] = (self.current_evaluations[self.game_state.get_active_country().get_name()] +
                                 self.game_state.get_active_country().get_player_investments(self.player))
        # Pass Down
        self.military_manager.receive_down(
            new_state=new_state
        )
        self.rondel_manager.receive_down(
            new_state=new_state
        )
        for country_evaluator in self.country_evaluators:
            country_evaluator.receive_down(
                new_state=new_state
            )

    def pass_up(self, new_state):
        """

        :param new_state:
        """
        # Pass Up
        # Parse what to pass using the information in the game state
        if new_state['action'] == 'Maneuver':
            return new_state['evaluation']
        elif new_state['action'] == 'Factory':
            return new_state['evaluation']
        elif new_state['action'] == 'Import':
            return new_state['evaluation']
        elif new_state['action'] == 'Investor':
            return self.active_evaluation
        elif new_state['action'] == 'Rondel':
            return new_state['evaluation']
        elif new_state['action'] == 'Battle':
            return new_state['evaluation']
        else:
            # Go cry or something because we didn't expect this
            raise RuntimeError('The action passed to the InvestorManager was not recognized')

    def receive_down(self, new_state):
        """
        From above will be the new game_state for analysis and
        an action that is going to be taken (rondel, battle, maneuver, etc.)
        :param new_state:
        """
        self.pass_down(new_state)
        # # Expected from above
        # if new_state['action'] == 'Maneuver':
        #     pass
        # elif new_state['action'] == 'Factory':
        #     pass
        # elif new_state['action'] == 'Import':
        #     pass
        # elif new_state['action'] == 'Investor':
        #     self.inner_evaluation()
        # elif new_state['action'] == 'Rondel':
        #     pass
        # elif new_state['action'] == 'Battle':
        #     pass
        # else:
        #     # Go cry or something because we didn't expect this
        #     raise RuntimeError('The action passed to the InvestorManager was not recognized')

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        # Anything we get should be passed up to the Agent above us
        for country in self.current_evaluations.keys():
            if country in new_state:
                self.current_evaluations[country] = new_state[country]
        self.pass_up(new_state=new_state)


class CountryEvaluator(MASPIPart):

    def __init__(self, player, country, investor_manager):
        """

        """
        super().__init__(player=player)
        self.name = 'Country Evaluator'
        self.total_investment = None
        self.relative_power = None
        self.tax_increase = None
        self.country = country
        self.investor_manager = investor_manager

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
        self.investor_manager.recieve_up(new_state)

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
        new_state[self.country.get_name()] = self.inner_evaluation()
        self.pass_up(new_state)

    def receive_up(self, new_state):
        """

        :param new_state:
        """
        # Expected from below
        pass
