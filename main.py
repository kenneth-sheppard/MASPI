
from game_engine.game_engine import GameEngine
from statistics_observer.game_results import GameStateObserver
from statistics_observer.player_observer import PlayerObserver

if __name__ == '__main__':
    op = []
    go = None

    for i in range(100):
        ge = GameEngine()

        if go is None:
            go = GameStateObserver(ge.get_state())
        else:
            go.update_game_state(ge.get_state())

        if len(op) == 0:
            for j in range(len(ge.get_state().get_players())):
                op.append(PlayerObserver(ge.get_state().get_players()[j]))
        else:
            for j in range(len(ge.get_state().get_players())):
                op[j].update_player(ge.get_state().get_players()[j])

        ge.play()

        for player_observer in op:
            player_observer.observe()

        # calculate a winner
        winner = op[0]

        for player_observer in op:
            if player_observer.get_player_info()['money'] > winner.get_player_info()['money']:
                winner = player_observer
            elif player_observer.get_player_info()['money'] == winner.get_player_info()['money']:
                for country in ge.get_state().get_countries_sorted_by_power():
                    if winner.get_player().get_investment_in_country(country) < \
                            player_observer.get_player().get_investment_in_country(country):
                        winner = player_observer
                    elif winner.get_player().get_investment_in_country(country) > \
                            player_observer.get_player().get_investment_in_country(country):
                        break
                    else:
                        continue
            else:
                continue

        winner.was_winner()

        go.game_end()

        for player_observer in op:
            player_observer.game_end()

    for player_observer in op:
        print(player_observer)

    print(go)

    with open('recorded_results.txt', 'wt') as f:
        for player_observer in op:
            f.write(player_observer.__str__())
        f.write(go.__str__())
