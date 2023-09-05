import csv
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.metrics import precision_recall_fscore_support
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameEngineObserver
from statistics_observer.player_observer import PlayerObserver


def load_data(file_path):
    df = pd.read_csv(file_path, header=None)
    data = df.to_numpy()
    x_data = []
    y_data = []
    for row in data:
        x_data.append(row[:-6])
        y_data.append(row[-6:])
    return np.array(x_data), np.array(y_data)


# def load_data_from_file(file_path="game_turns.txt"):
#     file = open(file_path, "r")
#
#     all_the_data = []
#
#     for sample in file:
#         sample_vector = []
#         for element in sample.split(','):
#             element = element.strip('\n').strip('[').strip(']').strip(' ')
#             sample_vector.append(float(element))
#         print(len(sample_vector))
#         all_the_data.append(sample_vector)
#
#     file.close()
#
#     return np.array(all_the_data)


def get_neural_network():
    # this will return a nn
    input_vector = tf.keras.Input(shape=(1302,), dtype=tf.int16)
    dense1 = tf.keras.layers.Dense(500, activation='gelu')
    output1 = dense1(input_vector)
    dropout1 = tf.keras.layers.Dropout(0.25)
    output2 = dropout1(output1)
    dense2 = tf.keras.layers.Dense(100, activation='gelu')
    output3 = dense2(output2)
    dropout2 = tf.keras.layers.Dropout(0.25)
    output4 = dropout2(output3)
    dense5 = tf.keras.layers.Dense(6, activation='sigmoid')

    final_output = dense5(output4)

    model = tf.keras.Model(inputs=[input_vector], outputs=[final_output])

    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def training_iteration(iteration_number):
    # so here's the plan
    # import the previous weights
    # create the set of games played between two copies of this current iteration
    # store it somewhere for reference later
    # then we're going to pull it out with our function and format it with the other
    # then we need to split it into test, training, and validation
    # then we will train the network on this new data, easy right?
    # then we will store the new weights
    # also we will run like 100 test games against the old network
    # everything should be stored in some text files
    # return the results against the previous opponent
    op = []
    game_observer = None

    for i in range(5):
        print(f'Game {i}')
        game_engine = GameEngine()

        if game_observer is None:
            game_observer = GameEngineObserver(game_engine)
        else:
            game_observer.update_game_state(game_engine)

        game_engine.subscribe(game_observer)

        if len(op) == 0:
            for j in range(len(game_engine.get_state().get_players())):
                op.append(PlayerObserver(game_engine.get_state().get_players()[j]))
        else:
            for j in range(len(game_engine.get_state().get_players())):
                op[j].update_player(game_engine.get_state().get_players()[j])

        for player_observer in op:
            game_engine.subscribe(player_observer)

        game_engine.play()

        # calculate a winner
        winner = op[0]

        for player_observer in op:
            if player_observer.get_player_info()['money'] > winner.get_player_info()['money']:
                winner = player_observer
            elif player_observer.get_player_info()['money'] == winner.get_player_info()['money']:
                for country in game_engine.get_state().get_countries_sorted_by_power():
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

        game_observer.game_end()

        for player_observer in op:
            player_observer.game_end()

    os.mkdir(f'./data/games{iteration_number}')

    with open('recorded_results.txt', 'wt') as f:
        for player_observer in op:
            f.write(player_observer.__str__() + ' ')
        f.write(game_observer.__str__())
        f.close()

    with open(f'./data/games{iteration_number}/recorded_results.txt', 'wt') as f:
        for player_observer in op:
            f.write(player_observer.__str__() + ' ')
        f.write(game_observer.__str__())
        f.close()

    with open('game_turns.csv', 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(game_observer.get_turn_by_turn())
        f.close()

    with open(f'./data/games{iteration_number}/game_turns.csv', 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(game_observer.get_turn_by_turn())
        f.close()

    # so first we're just going to pull the data and run it through training and build from there
    data_values, data_class = load_data('game_turns.csv')

    x_train, x_test, y_train, y_test = train_test_split(data_values, data_class, test_size=0.25, random_state=5, shuffle=True)

    if iteration_number == 0:
        model = get_neural_network()
    else:
        model = keras.models.load_model('recent_model')

    history = model.fit(x_train, y_train, epochs=100, batch_size=500)
    model.save('recent_model', save_format='h5')
    model.save('./models_h5/model' + str(iteration_number), save_format='h5')

    return iteration_number + 1


def train_off_data(iteration_number):
    data_values, data_class = load_data(f'./data/games{iteration_number}/game_turns.csv')

    x_train, x_test, y_train, y_test = train_test_split(data_values, data_class, test_size=0.25, random_state=5, shuffle=True)

    if iteration_number == 0:
        model = get_neural_network()
    else:
        model = keras.models.load_model('recent_model')

    history = model.fit(tf.expand_dims(x_train, axis=-1), y_train, epochs=100, batch_size=500)
    model.save('recent_model', save_format='h5')
    model.save('./models_h5/model' + str(iteration_number), save_format='h5')

    return iteration_number + 1


def test_model_directly():
    model = keras.models.load_model('recent_model')

    data_values, data_class = load_data('game_turns.csv')

    x_train, x_test, y_train, y_test = train_test_split(data_values, data_class, test_size=0.25, random_state=5, shuffle=True)

    print(x_test.shape)

    results = model.predict(x_test)

    for elem in results:
        print(elem)
