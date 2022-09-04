import game_engine.action_space
from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for player in gs.get_players():
        for bond in player.get_bonds():
            pass

    gs.update()

    print(gs.get_countries()[0].get_treasury())

    import_action = game_engine.action_space.Import()

    import_action.action(gs.get_countries()[0], gs.get_players()[0])

    for territory in gs.get_countries()[0].get_home_territories():
        print(f'{territory.get_name()} - {territory.get_tanks()} - {territory.get_ships()}')

    print(gs.get_countries()[0].get_treasury())
