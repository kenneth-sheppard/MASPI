from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for player in gs.get_players():
        print()
        for bond in player.get_bonds():
            print(bond)
