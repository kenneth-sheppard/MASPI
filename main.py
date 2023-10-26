
import csv
import os
import time

import game_engine.game_setup
import game_engine.settings
from neural_network.NeuralNetwork import training_iteration, train_off_data, test_model_directly
from players import random, greedy, basic_nn, maspi, human
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameEngineObserver
from statistics_observer.player_observer import PlayerObserver


def play_game(amount):
    op = []
    go = None

    start_time = time.time()

    for i in range(amount):
        print(f'Game {i}')
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


if __name__ == '__main__':

    game_engine.settings.num_players = 6

    # game_engine.settings.player_1 = greedy.GreedyPlayer
    # game_engine.settings.player_2 = random.RandPlayer
    # game_engine.settings.player_3 = greedy.GreedyPlayer
    # game_engine.settings.player_4 = basic_nn.BasicNeuralNetPlayer
    # game_engine.settings.player_5 = maspi.MASPIPlayer
    # game_engine.settings.player_6 = maspi.MASPIPlayer

    # game_engine.settings.player_1 = human.HumanPlayer
    # game_engine.settings.player_2 = human.HumanPlayer
    # game_engine.settings.player_3 = human.HumanPlayer
    # game_engine.settings.player_4 = human.HumanPlayer
    # game_engine.settings.player_5 = human.HumanPlayer
    # game_engine.settings.player_6 = human.HumanPlayer

    game_engine.settings.player_1 = basic_nn.BasicNeuralNetPlayer
    game_engine.settings.player_2 = basic_nn.BasicNeuralNetPlayer
    game_engine.settings.player_3 = basic_nn.BasicNeuralNetPlayer
    game_engine.settings.player_4 = basic_nn.BasicNeuralNetPlayer
    game_engine.settings.player_5 = basic_nn.BasicNeuralNetPlayer
    game_engine.settings.player_6 = basic_nn.BasicNeuralNetPlayer

    game_engine.settings.folder_to_write = 'practice_data\\development'

    for i in range(847, 1000):
        training_iteration(i)

    # for i in range(0, 17):
    #     train_off_data(i)

    play_game(1)

    # test_model_directly()
