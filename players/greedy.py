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
                pass

        return value


class GreedyWithPenaltiesPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Greedy Penalty'

    def evaluate_game_state(self, game_state):
        value = 0
        for player in game_state.get_players():
            if player.get_id() is self.id:
                value += player.get_worth()
            else:
                value -= player.get_worth()

        return value


class GreedyOnTheBoardPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Greedy On Board'

    def evaluate_game_state(self, game_state):
        value = self.get_worth()
        for country in game_state.get_countries():
            if country.get_country_controller().get_id() is self.id:
                value += len(country.get_controlled_neutral_territories()) + country.get_placed_units()
            else:
                value -= len(country.get_controlled_neutral_territories()) + country.get_placed_units()

        return value
