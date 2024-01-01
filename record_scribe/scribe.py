import csv
import operator
import os

import game_engine.helper as helper
from record_scribe.rondel_stats import RondelStats
from record_scribe.scribe_helpers import country_name_helper, player_name_helper, rondel_space_helper, territory_helper
from record_scribe.tax_stats import TaxStats


class Scribe:

    # games is a path to a folder of game results
    def __init__(self, games, old_id_count):
        self.path_to_games = games
        self.rondel_stats = RondelStats()
        self.tax_stats = None
        self.invest_stats = None
        self.game_lengths = {}

    def process_games(self):
        player_count = None
        with open(os.path.join(self.path_to_games, 'quick_stats.csv')) as s:
            turns_reader = csv.reader(s)
            for stat_line in turns_reader:
                if not stat_line:
                    continue
                # Handle extra blank lines
                if all([blank == '' for blank in stat_line]):
                    continue
                if player_count is None:
                    # 14 elements break down as
                    # 1 Game number
                    # 1 Game length
                    # 6 Country Power Value at end
                    # 6 Country Relative Scoring Position
                    player_count = len(stat_line) - 14
                self.game_lengths[int(stat_line[0])] = int(stat_line[1])

        with open(os.path.join(self.path_to_games, 'game_turns.csv')) as f:
            csv_reader = csv.reader(f)
            turn_counter = 0
            first_player_id = 0
            rondel_selection = True
            self.tax_stats = TaxStats()
            self.invest_stats = TaxStats()
            previous_turn = {}
            self.rondel_stats = RondelStats()

            for turn in csv_reader:
                if not turn:
                    continue
                if rondel_selection:
                    turn_counter += 1
                    rondel_selection = False
                else:
                    rondel_selection = True

                ai = 0
                players = {}
                for i in range(player_count):
                    players[f'Player {i + 1}'] = (turn[(i * 2)], turn[(i * 2)+1])
                ai += 12
                # Six countries are always present
                countries = {}
                for c in range(6):
                    countries[country_name_helper[c]] = {
                        'Power': turn[ai],
                        'Treasury': turn[ai + 1],
                        'Available Tanks': turn[ai + 2],
                        'Available Ships': turn[ai + 3],
                        'Controller': player_name_helper(turn[ai + 4:ai + 10], first_player_id),
                        'Rondel Space': rondel_space_helper(turn[ai + 10:ai + 18]),
                        'Bonds': []
                    }
                    ai += 18
                    # Read in the bonds for the country
                    # Bonds have eight elements (interest, cost, owner[6])
                    for bond_index in range(1, 10):
                        countries[country_name_helper[c]]['Bonds'].append(
                            (turn[ai + 6],
                             turn[ai + 7],
                             player_name_helper(turn[ai:ai + 6], first_player_id))
                        )
                        ai += 8
                # Read in all territories and store
                # Territory dict is helper.territory_id_and_names
                territories = {}
                for territory_id in helper.territory_id_and_names.keys():
                    territories[helper.territory_id_and_names[territory_id]] = territory_helper(turn[ai:ai + 12])
                    ai += 12

                investor_card_holder = player_name_helper(turn[ai:ai + 6], first_player_id)

                # Process any interesting information
                # Starting with count how many times a player lands on a Rondel space
                # and
                # Count how many times a country lands on a rondel space
                current_turn = {
                    'Players': players,
                    'Countries': countries,
                    'Territories': territories,
                    'Investor Card': investor_card_holder,
                    'Turn Number': turn_counter
                }
                # Rondel selection changes before this is checked, so I want to see the inverse
                if not rondel_selection:
                    self.rondel_stats.take_current_and_previous_turn(
                        previous_turn=previous_turn,
                        current_turn=current_turn
                    )
                    self.tax_stats.take_current_and_previous_turn_taxes(
                        previous_turn=previous_turn,
                        current_turn=current_turn
                    )
                    self.invest_stats.take_current_and_previous_turn_investor(
                        previous_turn=previous_turn,
                        current_turn=current_turn
                    )

                previous_turn = {
                    'Players': players,
                    'Countries': countries,
                    'Territories': territories,
                    'Investor Card': investor_card_holder,
                    'Turn Number': turn_counter
                }

                if not rondel_selection:
                    for country in countries.values():
                        if country['Power'] == '25':
                            # end of current game reset for next game
                            self.rondel_stats.finalize_game()
                            self.tax_stats.finalize_game()
                            # self.invest_stats.finalize_game()
                            turn_counter = 0
                            first_player_id = (first_player_id + player_count) % 6

    def get_statistics(self):
        player_sums = {}
        country_sums = {}
        tax_sums = {}
        invest_sums = {}
        player_favorite_turns = {}
        # for game in self.rondel_stats.get_games():
        #     for player in game[0].keys():
        #         if player not in player_sums.keys():
        #             player_sums[player] = {}
        #             for space in rondel_space_dict.values():
        #                 player_sums[player][space] = 0
        #         for space in rondel_space_dict.values():
        #             if space in game[0][player]:
        #                 player_sums[player][space] += game[0][player][space]
        #     for country in game[1].keys():
        #         if country not in country_sums.keys():
        #             country_sums[country] = {}
        #             for space in rondel_space_dict.values():
        #                 country_sums[country][space] = 0
        #         for space in rondel_space_dict.values():
        #             if space in game[1][country]:
        #                 country_sums[country][space] += game[1][country][space]

        for game in self.tax_stats.get_information():
            for player in game.keys():
                if player not in tax_sums.keys():
                    tax_sums[player] = game[player]
                else:
                    tax_sums[player] += game[player]

        # for game in self.invest_stats.get_information():
        #     for player in game.keys():
        #         if player not in invest_sums.keys():
        #             invest_sums[player] = game[player]
        #         else:
        #             invest_sums[player] += game[player]

        turns = {}
        for player in self.rondel_stats.get_turns_by_players().keys():
            for turn in self.rondel_stats.get_turns_by_players()[player]:
                if turn not in turns:
                    turns[turn] = {}
                choice_max = max(self.rondel_stats.get_turns_by_players()[player][turn].items(),
                                 key=operator.itemgetter(1))
                turns[turn][player] = (
                    choice_max[0],
                    choice_max[1],
                    choice_max[1] / sum(self.rondel_stats.get_turns_by_players()[player][turn].values())
                )

        # # Print Header
        # print('Player Investor Import Production1 Maneuver1 Taxation Factory Production2 Maneuver2')
        # # Print each line
        # for player in sorted(player_sums.keys()):
        #     p = player_sums[player]
        #     print(f'{str(player).replace(" ", "_")} {p["Investor"]} {p["Import"]} {p["Production1"]} {p["Maneuver1"]} '
        #           f'{p["Taxation"]} {p["Factory"]} {p["Production2"]} {p["Maneuver2"]}')
        # print()
        # # Print Header
        # print('Country Investor Import Production1 Maneuver1 Taxation Factory Production2 Maneuver2')
        # # Print each line
        # for country in country_sums.keys():
        #     c = country_sums[country]
        #     print(f'{str(country).replace(" ", "_")} {c["Investor"]} {c["Import"]} {c["Production1"]} {c["Maneuver1"]} '
        #           f'{c["Taxation"]} {c["Factory"]} {c["Production2"]} {c["Maneuver2"]}')
        # print()
        # # Game length max, min, average, mean, median, mode
        # game_lengths_list = list(self.game_lengths.values())
        # print('Game Lengths Information')
        # print(f'Maximum {max(game_lengths_list)} | Minimum {min(game_lengths_list)} | '
        #       f'Average {numpy.average(game_lengths_list)} | Mean {numpy.mean(game_lengths_list)} | '
        #       f'Median {numpy.median(game_lengths_list)} | Mode {stats.mode(game_lengths_list, keepdims=False)}')
        #
        print('Player Tax_Information')
        for player in sorted(tax_sums.keys()):
            t = tax_sums[player]
            print(f'{str(player).replace(" ", "_")} {t}')

        # print('Player Investing_Information')
        # for player in sorted(invest_sums.keys()):
        #     i = invest_sums[player]
        #     print(f'{str(player).replace(" ", "_")} {i}')

    def write_statistics_to_file(self):
        pass


if __name__ == '__main__':
    crib = Scribe(games='../final_tests/one_random_all_neural_6/', old_id_count=True)

    crib.process_games()

    crib.get_statistics()

