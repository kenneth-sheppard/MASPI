from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for territory in gs.get_territories():
        print(f'{territory.get_name()} - {territory.is_water} - {territory.factory_is_sea}')
