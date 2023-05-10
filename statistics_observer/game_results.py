

class GameEngineObserver:

    def __init__(self, ge):
        self.game_engine = ge
        self.countries = {}
        self.records = []
        self.buffer = []
        self.game_engine.subscribe(self)
        for country in self.game_engine.get_state().get_countries():
            self.countries[country.get_name()] = CountryObserver(country)

    def __str__(self):
        result = ''
        for country_name in self.countries.keys():
            result += f'{country_name} - wins {self.countries[country_name].get_top_finishes()} - average ' \
                      f'{self.countries[country_name].get_average_finish()}\n'

        return result

    def observe(self):
        self.buffer.append(self.game_engine.get_state().get_numerical_representation())

    def get_turn_by_turn(self):
        return self.records

    def __append_end_scores(self, end_scores):
        for i in range(len(self.buffer)):
            self.buffer[i].extend(end_scores)

    def game_end(self):
        position = 6
        for country in self.game_engine.get_state().get_countries_sorted_by_power():
            self.countries[country.get_name()].game_end(position)
            position -= 1
        self.__append_end_scores(self.game_engine.get_state().get_normalized_end_scores())
        self.records.extend(self.buffer)
        self.buffer = []

    def update_game_state(self, ge):
        self.game_engine.unsubscribe(self)
        self.game_engine = ge
        self.game_engine.subscribe(self)
        for country in self.game_engine.get_state().get_countries():
            self.countries[country.get_name()].update_country(country)


class CountryObserver:

    def __init__(self, c):
        self.country = c
        self.top_finishes = 0
        self.games_played = 0
        self.summed_finishes = 0

    def update_country(self, country):
        self.country = country

    def game_end(self, position):
        self.games_played += 1
        if self.country.get_power() == 25:
            self.top_finishes += 1
        self.summed_finishes += position

    def get_top_finishes(self):
        return self.top_finishes

    def get_average_finish(self):
        return self.summed_finishes / self.games_played
