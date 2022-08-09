from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for t in gs.territories:
        print('{} - {}'.format(t.get_name(), t.has_factory()))
