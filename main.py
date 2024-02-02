import csv
import os
import time
import random as r

import game_engine.game_setup
import game_engine.settings
from neural_network.NeuralNetwork import training_iteration, train_off_data, test_model_directly, train_on_all_data
from players import random, greedy, basic_nn, maspi, human
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameEngineObserver
from statistics_observer.player_observer import PlayerObserver


def play_game(amount):
    op = []
    go = None

    start_time = time.time()

    for i in range(amount):
        # print(f'Game {i}')
        ge = GameEngine()

        if go is None:
            go = GameEngineObserver(ge)
        else:
            go.update_game_state(ge)

        ge.subscribe(go)

        if len(op) == 0:
            for j in range(len(ge.get_state().get_players())):
                op.append(PlayerObserver(ge.get_state().get_players()[j]))
        else:
            for j in range(len(ge.get_state().get_players())):
                op[j].update_player(ge.get_state().get_players()[j])

        for player_observer in op:
            ge.subscribe(player_observer)

        ge.play()

        # calculate a winner
        winner = op[0]

        for player_observer in op:
            if player_observer.get_player_info()['money'] > winner.get_player_info()['money']:
                winner = player_observer
            elif player_observer.get_player_info()['money'] == winner.get_player_info()['money']:
                for country in ge.get_state().get_countries_sorted_by_power():
                    if winner.get_player().get_investment_in_country(country) < \
                            player_observer.get_player().get_investment_in_country(country):
                        winner = player_observer
                    elif winner.get_player().get_investment_in_country(country) > \
                            player_observer.get_player().get_investment_in_country(country):
                        break
                    else:
                        continue
            else:
                continue

        winner.was_winner()

        go.game_end()

        for player_observer in op:
            player_observer.game_end()

    for player_observer in op:
        print(player_observer)

    end_time = time.time()

    print(end_time - start_time)

    print(go)

    if not os.path.isdir(os.path.join(game_engine.settings.folder_to_write)):
        os.mkdir(os.path.join(game_engine.settings.folder_to_write))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt'))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv'))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv'))

    with open(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt'), 'wt') as f:
        for player_observer in op:
            f.write(player_observer.__str__() + ' ')
        f.write(go.__str__())

    with open(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv'), 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(go.get_turn_by_turn())

    with open(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv'), 'wt') as f:
        csv_writer = csv.writer(f)
        rows = go.get_game_by_game_stats()
        for i in range(0, len(rows)):
            for player_observer in op:
                rows[i].append(player_observer.get_score(i))
        csv_writer.writerows(rows)


def play_games_with_changing_sets(amount_of_games, list_of_players):
    set_of_available_player_counts = {}
    set_of_available_player_classes = {}

    if amount_of_games // 5 < 1 or amount_of_games % 5 != 0:
        raise RuntimeError('Choose an amount of games greater than and divisible by five!')

    for player_count in range(2, 7):
        set_of_available_player_counts[player_count] = amount_of_games // 5

    total_players_used = ((amount_of_games // 5) * 2 + (amount_of_games // 5) * 3 + (amount_of_games // 5) * 4 +
                          (amount_of_games // 5) * 5 + (amount_of_games // 5) * 6)

    if total_players_used // len(list_of_players) < 1 or total_players_used % len(list_of_players) != 0:
        raise RuntimeError(f'Choose an amount of players that evenly distributes across '
                           f'a total of {total_players_used} players')

    for player_type in list_of_players:
        set_of_available_player_classes[player_type] = total_players_used // len(list_of_players)

    op = []
    go = None
    game_results = []

    start_time = time.time()

    for i in range(amount_of_games):
        game_engine.settings.num_players = None

        while game_engine.settings.num_players is None:
            random_num_players_choice = r.randint(2, 6)
            if set_of_available_player_counts[random_num_players_choice] != 0:
                set_of_available_player_counts[random_num_players_choice] -= 1
                game_engine.settings.num_players = random_num_players_choice

        for p in range(game_engine.settings.num_players):
            while True:
                random_player_type_choice = r.randint(0, len(list_of_players) - 1)
                if set_of_available_player_classes[list_of_players[random_player_type_choice]] != 0:
                    set_of_available_player_classes[list_of_players[random_player_type_choice]] -= 1
                    break
            if p == 0:
                game_engine.settings.player_1 = list_of_players[random_player_type_choice]
            elif p == 1:
                game_engine.settings.player_2 = list_of_players[random_player_type_choice]
            elif p == 2:
                game_engine.settings.player_3 = list_of_players[random_player_type_choice]
            elif p == 3:
                game_engine.settings.player_4 = list_of_players[random_player_type_choice]
            elif p == 4:
                game_engine.settings.player_5 = list_of_players[random_player_type_choice]
            elif p == 5:
                game_engine.settings.player_6 = list_of_players[random_player_type_choice]
            else:
                raise RuntimeError('Wrong player count selected during configuration')

        ge = GameEngine()

        if go is None:
            go = GameEngineObserver(ge)
        else:
            go.update_game_state(ge)

        ge.subscribe(go)

        for j in range(len(ge.get_state().get_players())):
            if j >= len(op):
                op.append(PlayerObserver(ge.get_state().get_players()[j]))
            else:
                op[j].update_player(ge.get_state().get_players()[j])

        for player_observer in op:
            ge.subscribe(player_observer)

        ge.play()

        # calculate a winner
        winner = op[0]

        for player_observer in op:
            if player_observer.get_player_info()['money'] > winner.get_player_info()['money']:
                winner = player_observer
            elif player_observer.get_player_info()['money'] == winner.get_player_info()['money']:
                for country in ge.get_state().get_countries_sorted_by_power():
                    if winner.get_player().get_investment_in_country(country) < \
                            player_observer.get_player().get_investment_in_country(country):
                        winner = player_observer
                    elif winner.get_player().get_investment_in_country(country) > \
                            player_observer.get_player().get_investment_in_country(country):
                        break
                    else:
                        continue
            else:
                continue

        winner.was_winner()

        go.game_end()

        for player_observer in op:
            player_observer.game_end()

        game_results.append(
            [f'{op[p].player_info["type"]} scored {op[p].scores[-1] }' for p in range(game_engine.settings.num_players)]
        )

    for player_observer in op:
        print(player_observer)

    end_time = time.time()

    print(end_time - start_time)

    print(go)

    if not os.path.isdir(os.path.join(game_engine.settings.folder_to_write)):
        os.mkdir(os.path.join(game_engine.settings.folder_to_write))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt'))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv'))

    if os.path.isfile(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv')):
        os.remove(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv'))

    with open(os.path.join(game_engine.settings.folder_to_write, 'recorded_results.txt'), 'wt') as f:
        for result in game_results:
            f.write(str(result) + '\n')

    with open(os.path.join(game_engine.settings.folder_to_write, 'game_turns.csv'), 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(go.get_turn_by_turn())

    with open(os.path.join(game_engine.settings.folder_to_write, 'quick_stats.csv'), 'wt') as f:
        csv_writer = csv.writer(f)
        rows = go.get_game_by_game_stats()
        # for i in range(0, len(rows)):
        #     for player_observer in op:
        #         rows[i].append(player_observer.get_score(i))
        csv_writer.writerows(rows)


if __name__ == '__main__':
    game_engine.settings.num_players = 6

    game_engine.settings.player_1 = basic_nn.FullScopeNeuralNetPlayer
    game_engine.settings.player_2 = basic_nn.FullScopeNeuralNetPlayer
    game_engine.settings.player_3 = basic_nn.FullScopeNeuralNetPlayer
    game_engine.settings.player_4 = basic_nn.FullScopeNeuralNetPlayer
    game_engine.settings.player_5 = basic_nn.FullScopeNeuralNetPlayer
    game_engine.settings.player_6 = basic_nn.FullScopeNeuralNetPlayer

    # game_engine.settings.player_1 = greedy.GreedyPlayer
    # game_engine.settings.player_2 = random.RandPlayer
    # game_engine.settings.player_3 = greedy.GreedyOnTheBoardPlayer
    # game_engine.settings.player_4 = random.RandPlayer
    # game_engine.settings.player_5 = greedy.GreedyWithPenaltiesPlayer
    # game_engine.settings.player_6 = random.RandPlayer

    # game_engine.settings.folder_to_write = 'practice_data/some_games'

    for i in range(57, 60):
        training_iteration(i)

    # for i in range(0, 500):
    #     train_off_data(i)
    #
    # train_on_all_data(1400, 1500, '100_games_full')

    # play_game(10)

    # play_games_with_changing_sets(
    #     amount_of_games=200,
    #     list_of_players=[random.RandPlayer, greedy.GreedyPlayer, basic_nn.BasicNeuralNetPlayer, maspi.MASPIPlayer])

    # test_model_directly()
