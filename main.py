from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for c in gs.get_countries():
        for t in c.get_home_territories():
            print('{} - {}'.format(t.get_name(), t.has_factory()))
