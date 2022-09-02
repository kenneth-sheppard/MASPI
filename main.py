from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for player in gs.get_players():
        for bond in player.get_bonds():
            pass

    gs.update()

    for player in gs.get_players():
        print(player.get_controlled_countries())
