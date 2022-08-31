import random

import game_engine.settings
from game_engine.game_state import GameState
from game_engine.territory import Territory
from game_engine.country import Country
from game_engine.helper import make_bonds_for, list_of_starting_factories, get_territory_id_from_name, \
    country_id_and_names, territory_id_and_names, starting_distributions, buy_bond
from game_engine.helper import home_territories as home_territories
from game_engine.player import Player


# Returns a GameState object to the game engine
def setup():
    new_game_state = GameState()

    # Create territories
    for t_id, name in territory_id_and_names.items():
        new_game_state.add_territory(Territory(name, t_id))

    # Create countries
    for c_id, name in country_id_and_names.items():
        c = Country(name, c_id)
        h_t_list = []
        for home_t in home_territories.get(name):
            h_t_list.append(new_game_state.get_territory(get_territory_id_from_name(home_t)))
        c.set_home_territories(h_t_list)
        # add starting factories, 2 tank for China, 2 ship for America, 1 and 1 otherwise
        # also piece counts
        # China 10 tanks, 6 ships
        # America 6 tanks, 10 ships
        # Others 8 and 8
        if name == 'China':
            c.starting_tanks = 10
            c.starting_ships = 6
        elif name == 'America':
            c.starting_tanks = 6
            c.starting_ships = 10
        else:
            c.starting_tanks = 8
            c.starting_ships = 8

        # all countries get 15 flags
        c.flag_count = 15
        new_game_state.add_country(c)

    # Create bonds for each country
    for country in new_game_state.get_countries():
        new_game_state.update_country(country, make_bonds_for(country))

    # Build starting factories
    for t_name in list_of_starting_factories:
        new_game_state.get_territory(get_territory_id_from_name(t_name)).build_factory()

    # Setup players
    for i in range(0, game_engine.settings.num_players):
        temp_player = Player()
        temp_player.add_money(13 * (6 // game_engine.settings.num_players))
        for j in range(0, 6 // game_engine.settings.num_players):
            # Assign a set of starting bonds to each player from list
            # Choose random available option
            k = random.randint(0, len(starting_distributions) - 1)
            buy_bond(temp_player, new_game_state.get_country(starting_distributions[k][0][0]),
                     starting_distributions[k][0][1])
            buy_bond(temp_player, new_game_state.get_country(starting_distributions[k][1][0]),
                     starting_distributions[k][1][1])
            starting_distributions.remove(starting_distributions[k])

        new_game_state.add_player(temp_player)

    return new_game_state