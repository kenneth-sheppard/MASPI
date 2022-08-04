from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for c in gs.get_countries():
        print('{} - {}'.format(c.get_id(), c.get_name()))
        for bond in c.get_bonds():
            print(bond)
