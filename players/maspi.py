
import copy
import game_engine.action_space as action_space
import game_engine.game_engine as game_engine

from game_engine.player import Player


class PlayerMASPI(Player):
    def __init__(self):
        super().__init__()
        self.type = 'MASPI Player'

    def __evaluate_game_state(self, game_state):
        return 0

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
        self.name = 'Basic Part'

    def pass_down(self):
        pass

    def pass_up(self):
        pass

    def receive_up(self):
        pass

    def receive_down(self):
        pass


class TerritoryAgent(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Territory Agent'

    def pass_up(self):
        # Get all adjacent territories
        # For each adjacent territory query value
        # Calculate own value
        # Identify the best location for each unit in territory
        # Probably best to loop for number of units present times
        # Return unit plans
        pass

    def receive_down(self):
        # Expected from above
        # Aggressiveness
        # Carelessness
        pass


class ManeuverCollector(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Maneuver Collector'

    def pass_down(self):
        # Pass down
        # Aggressiveness
        # Carelessness
        pass

    def pass_up(self):
        # Pass that to the rondel manager maybe?
        pass

    def receive_down(self):
        # Expected from above
        # Violence
        # Expansiveness
        pass

    def receive_up(self):
        # Expected from below
        # A bunch of territory agent evaluations
        # Select the best priorities
        pass


class RondelManager(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Rondel Manager'

    def pass_down(self):
        # Pass Down
        pass

    def pass_up(self):
        # I don't think anything needs to be passed up
        pass

    def receive_down(self):
        # Expected from above
        # Make money
        # Build force
        # Expand Territory
        pass

    def receive_up(self):
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
        pass


class MilitaryManager(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Military Manager'

    def pass_down(self):
        # Pass Down
        # Violence
        # Expansiveness
        pass

    def pass_up(self):
        # I don't think anything needs to be passed up
        pass

    def receive_down(self):
        # Expected from above
        pass

    def receive_up(self):
        # Expected from below
        pass


class InvestorManager(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Investor Manager'

    def pass_down(self):
        # Pass Down
        pass

    def pass_up(self):
        # Pass Up
        pass

    def receive_down(self):
        # Expected from above
        pass

    def receive_up(self):
        # Expected from below
        pass


class CountryEvaluator(MASPIPart):

    def __init__(self):
        super().__init__()
        self.name = 'Country Evaluator'

    def pass_down(self):
        # Pass Down
        pass

    def pass_up(self):
        # Pass Up
        pass

    def receive_down(self):
        # Expected from above
        pass

    def receive_up(self):
        # Expected from below
        pass
