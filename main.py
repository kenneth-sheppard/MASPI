from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for player in gs.get_players():
        for bond in player.get_bonds():
            pass

    gs.update()

    for country in gs.get_countries():
        print(country.get_controller())
