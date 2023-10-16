import random

import game_engine.settings
from game_engine.game_state import GameState
from game_engine.territory import Territory
from game_engine.country import Country
from game_engine.helper import make_bonds_for, list_of_starting_factories, get_territory_id_from_name, \
    country_id_and_names, territory_id_and_names, starting_distributions, buy_bond, sea_territories, \
    list_of_sea_factories
from game_engine.helper import home_territories as home_territories
from game_engine.investor_card import InvestorCard


# Returns a GameState object to the game engine
def setup():
    """
    Sets up the game, creating all initial objects
    :return: GameState - the fully configured game state
    """
    new_game_state = GameState()

    # Create territories
    for t_id, name in territory_id_and_names.items():
        new_game_state.add_territory(Territory(name, t_id))

    for t_id in sea_territories:
        new_game_state.get_territory(t_id).is_water = True

    for t_name in list_of_sea_factories:
        new_game_state.get_territory(get_territory_id_from_name(t_name)).factory_is_sea = True

    # Create countries
    for c_id, name_list in country_id_and_names.items():
        name = name_list[0]
        abbr = name_list[1]
        c = Country(name, abbr, c_id)
        h_t_list = []
        for home_t in home_territories.get(name):
            h_t_list.append(new_game_state.get_territory(get_territory_id_from_name(home_t)))
        for territory in h_t_list:
            territory.is_neutral = False
            territory.in_country = c
        c.set_home_territories(h_t_list)
        # add starting factories, 2 tank for China, 2 ship for America, 1 and 1 otherwise
        # also piece counts
        # China 10 tanks, 6 ships
        # America 6 tanks, 10 ships
        # Others 8 and 8
        if name == 'China':
            c.starting_tanks = 10
            c.tank_factory_pool = 3
            c.starting_ships = 6
            c.ship_factory_pool = 1
        elif name == 'America':
            c.starting_tanks = 6
            c.tank_factory_pool = 1
            c.starting_ships = 10
            c.ship_factory_pool = 3
        else:
            c.starting_tanks = 8
            c.tank_factory_pool = 2
            c.starting_ships = 8
            c.ship_factory_pool = 2

        # Add ships and tanks to their respective pools
        for t in range(0, c.starting_tanks):
            c.add_tank_to_pool()

        for s in range(0, c.starting_ships):
            c.add_ship_to_pool()

        # all countries get 15 flags
        c.flag_count = 15
        new_game_state.add_country(c)

    # Create bonds for each country
    for country in new_game_state.get_countries():
        new_game_state.update_country(make_bonds_for(country))

    # Build starting factories
    for t_name in list_of_starting_factories:
        new_game_state.get_territory(get_territory_id_from_name(t_name)).build_factory()

    # Investor card
    i_card = InvestorCard()

    temp_dists = starting_distributions.copy()

    # This can be edited to change players and player types, will need to be more dynamic eventually
    # Setup players
    game_engine.settings.assemble_player_list()
    for i in range(0, game_engine.settings.num_players):
        if game_engine.settings.player_list[i] is None:
            raise RuntimeError('Did not properly configure all players')
        temp_player = game_engine.settings.player_list[i]()
        temp_player.add_money(13 * (6 // game_engine.settings.num_players))
        for j in range(0, 6 // game_engine.settings.num_players):
            # Assign a set of starting bonds to each player from list
            # Choose random available option
            k = random.randint(0, len(temp_dists) - 1)
            buy_bond(temp_player, new_game_state.get_country(temp_dists[k][0][0]),
                     temp_dists[k][0][1])
            buy_bond(temp_player, new_game_state.get_country(temp_dists[k][1][0]),
                     temp_dists[k][1][1])
            new_game_state.get_country(temp_dists[k][0][0]).set_country_controller(temp_player)
            temp_dists.remove(temp_dists[k])

        new_game_state.add_player(temp_player)

        print(f'Adding Player {temp_player.get_id()}')
        print(f'With bonds {" ".join([str(b) for b in temp_player.get_bonds()])}\n')

        i_card.add_player(temp_player)

    new_game_state.update()

    i_card.done_adding_players()

    new_game_state.investor_card = i_card

    return new_game_state
