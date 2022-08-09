from game_engine.game_state import GameState
from game_engine.helper import territory_id_and_names
from game_engine.helper import country_id_and_names
from game_engine.territory import Territory
from game_engine.country import Country
from game_engine.helper import make_bonds_for
from game_engine.helper import list_of_starting_factories
from game_engine.helper import get_territory_id_from_name


# Returns a GameState object to the game engine
def setup():
    new_game_state = GameState()

    # Create territories
    for t_id, name in territory_id_and_names.items():
        new_game_state.add_territory(Territory(name, t_id))

    # Create countries
    for c_id, name in country_id_and_names.items():
        new_game_state.add_country(Country(name, c_id))

    # Create bonds for each country
    for country in new_game_state.get_countries():
        new_game_state.update_country(country, make_bonds_for(country))

    # Build starting factories
    for t_name in list_of_starting_factories:
        new_game_state.get_territory(get_territory_id_from_name(t_name)).build_factory()

    return new_game_state
