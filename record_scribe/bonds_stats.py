import game_engine.helper


class BondStats:
    def __init__(self):
        self.points_cost = {}
        self.bonds = {}

    def take_end_of_game_state_for_relative_bonds(self, current_turn):
        for country in current_turn['Countries'].keys():
            for bond in current_turn['Countries'][country]['Bonds']:
                if bond[2] is None or bond[2] == 'No Player':
                    continue
                else:
                    if bond[2] not in self.points_cost.keys():
                        self.points_cost[bond[2]] = (
                                game_engine.helper.power_chart(int(current_turn['Countries'][country]['Power']))
                                * int(bond[1]) - int(bond[0])
                        )
                    else:
                        self.points_cost[bond[2]] += (
                                game_engine.helper.power_chart(int(current_turn['Countries'][country]['Power']))
                                * int(bond[1]) - int(bond[0])
                        )

    def take_end_of_game_state_for_absolute_points(self, current_turn):
        for country in current_turn['Countries'].keys():
            for bond in current_turn['Countries'][country]['Bonds']:
                if bond[2] is None or bond[2] == 'No Player':
                    continue
                else:
                    if bond[2] not in self.points_cost.keys():
                        self.points_cost[bond[2]] = (
                                game_engine.helper.power_chart(int(current_turn['Countries'][country]['Power']))
                                * int(bond[1])
                        )
                    else:
                        self.points_cost[bond[2]] += (
                                game_engine.helper.power_chart(int(current_turn['Countries'][country]['Power']))
                                * int(bond[1])
                        )


class MoneyStats:
    def __init__(self):
        self.end_wealth = {}

    def take_end_of_game_stats(self, current_turn):
        for player in current_turn['Players'].keys():
            if player in self.end_wealth:
                self.end_wealth[player] += int(current_turn['Players'][player][0])
            else:
                self.end_wealth[player] = int(current_turn['Players'][player][0])
