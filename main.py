import game_engine.action_space
from game_engine import game_setup


if __name__ == '__main__':
    gs = game_setup.setup()
    for player in gs.get_players():
        for bond in player.get_bonds():
            pass

    gs.update()

    investor = game_engine.action_space.Investor()
    investor.players = gs.get_players()
    for country in gs.get_countries():
        investor.action(country)

    for country in gs.get_countries():
        investor.action(country)

    for country in gs.get_countries():
        investor.action(country)

    for country in gs.get_countries():
        investor.action(country)

    for country in gs.get_countries():
        investor.action(country)
