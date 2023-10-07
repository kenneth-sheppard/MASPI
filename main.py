
import csv
import time
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameEngineObserver
from statistics_observer.player_observer import PlayerObserver
from neural_network.NeuralNetwork import training_iteration, train_off_data, test_model_directly


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

    with open('recorded_results.txt', 'wt') as f:
        for player_observer in op:
            f.write(player_observer.__str__() + ' ')
        f.write(go.__str__())

    with open('game_turns.csv', 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(go.get_turn_by_turn())


if __name__ == '__main__':

    # for i in range(450, 500):
    #     training_iteration(i)

    # for i in range(0, 17):
    #     train_off_data(i)

    play_game(300)

    # test_model_directly()
