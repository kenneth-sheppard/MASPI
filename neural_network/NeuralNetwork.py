
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameEngineObserver
from statistics_observer.player_observer import PlayerObserver


def load_data(file_path):
    df = pd.read_csv(file_path, header=None)
    data = df.to_numpy()
    return np.array(data[:, :-6]), np.array(data[:, -6])


def load_data_from_file(file_path="game_turns.txt"):
    file = open(file_path, "r")

    all_the_data = []

    for sample in file:
        sample_vector = []
        for element in sample.split(','):
            element = element.strip('\n').strip('[').strip(']').strip(' ')
            sample_vector.append(float(element))
        print(len(sample_vector))
        all_the_data.append(sample_vector)

    file.close()

    return np.array(all_the_data)


# def format_entries_for_nn(data_array):
#     updated_data_array_not_numpy_array = []
#     for data_entry in data_array:
#         updated_data_array_not_numpy_array.append(format_gamestate_for_nn(data_entry))
#
#     return np.array(updated_data_array_not_numpy_array)


# def format_gamestate_for_nn(data_entry):
#     updated_entry_array = []
#     for i in range(0, len(data_entry)):
#         if i <= 24:
#             # adding a piece vector for each position
#             # < 1, 0, 0, 0, 0 > is an empty space
#             # < 0, 1, 0, 0, 0 > is a pawn stored as 1 in the gamestate
#             # < 0, 0, 1, 0, 0 > is a master stored as 2
#             # < 0, 0, 0, 1, 0 > is a pawn stored as -1
#             # < 0, 0, 0, 0, 1 > is a master stored as -2
#             if data_entry[i] == 0:
#                 updated_entry_array.append(1)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#             if data_entry[i] == 1:
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(1)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#             if data_entry[i] == 2:
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(1)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#             if data_entry[i] == -1:
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(1)
#                 updated_entry_array.append(0)
#             if data_entry[i] == -2:
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(0)
#                 updated_entry_array.append(1)
#         elif i > 24 and i < 30:
#             for value in Card.get_card_grid_by_id(data_entry[i]):
#                 updated_entry_array.append(value)
#         else:
#             updated_entry_array.append(data_entry[i])
#
#     return updated_entry_array


def get_neural_network():
    # this will return a nn
    # it should be able to have the right weights
    # currently it does not do that
    # TODO: be able to import weights
    input_vector = tf.keras.Input(shape=(1302,), dtype=tf.int16)
    dense1 = tf.keras.layers.Dense(200, activation='gelu')
    output1 = dense1(input_vector)
    dropout1 = tf.keras.layers.Dropout(0.8)
    output2 = dropout1(output1)
    dense2 = tf.keras.layers.Dense(100, activation='gelu')
    output3 = dense2(output2)
    dropout2 = tf.keras.layers.Dropout(0.8)
    output4 = dropout2(output3)
    dense3 = tf.keras.layers.Dense(6, activation='sigmoid')

    final_output = dense3(output4)

    model = tf.keras.Model(inputs=[input_vector], outputs=[final_output])

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

    # game_observer = None
    #
    # for i in range(20):
    #     game_engine = GameEngine()
    #
    #     if game_observer is None:
    #         game_observer = GameEngineObserver(game_engine)
    #     else:
    #         game_observer.update_game_state(game_engine)
    #
    #     game_engine.play()
    #
    #     game_observer.game_end()

    # so first we're just going to pull the data and run it through training and build from there
    data_values, data_class = load_data('game_turns.csv')

    x_train, x_test, y_train, y_test = train_test_split(data_values, data_class, test_size=0.25, random_state=5, shuffle=True)

    # model = keras.models.load_model('current_model')
    model = get_neural_network()
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=200, batch_size=250)
    model.save('current_model')
    # model.save('./data/models/model' + str(iteration_number))

    # rand_game_engine = Engine.GameEngine(Player.RandomPlayer(), Player.MiniMaxPlayer('current_model'))

    # Engine.play_n_games_and_record(rand_game_engine, 5, True, './data/games/games' + str(iteration_number) + '.csv')

    return None
