

class GameEngineObserver:

    def __init__(self, ge):
        self.game_engine = ge
        self.countries = {}
        self.records = []
        self.buffer = []
        self.games_count = 0
        self.game_by_game_stats = []
        self.game_engine.subscribe(self)
        for country in self.game_engine.get_state().get_countries():
            self.countries[country.get_name()] = CountryObserver(country)

    def __str__(self):
        result = ''
        for country_name in self.countries.keys():
            result += f'{country_name:15} - finishes {self.countries[country_name].get_string_finishes()} - average ' \
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
        self.games_count += 1
        game_stats = []
        game_stats.extend([self.games_count, self.game_engine.get_turns()])
        position = 6
        for country in self.game_engine.get_state().get_countries_sorted_by_power():
            self.countries[country.get_name()].game_end(position)
            position -= 1
        for country_observer in self.countries.values():
            game_stats.extend(country_observer.get_finishes()[self.games_count - 1])
        self.__append_end_scores(self.game_engine.get_state().get_end_scores_between_zero_and_one())
        self.records.extend(self.buffer)
        self.buffer = []
        self.game_by_game_stats.append(game_stats)

    def update_game_state(self, ge):
        self.game_engine.unsubscribe(self)
        self.game_engine = ge
        self.game_engine.subscribe(self)
        for country in self.game_engine.get_state().get_countries():
            self.countries[country.get_name()].update_country(country)

    def get_game_by_game_stats(self):
        return self.game_by_game_stats


class CountryObserver:

    def __init__(self, c):
        self.country = c
        self.top_finishes = 0
        self.games_played = 0
        self.summed_finishes = 0
        self.finishes = []

    def update_country(self, country):
        self.country = country

    def game_end(self, position):
        self.games_played += 1
        if self.country.get_power() == 25:
            self.top_finishes += 1
        self.summed_finishes += position
        self.finishes.append([position, self.country.get_power()])

    def get_top_finishes(self):
        return self.top_finishes

    def get_average_finish(self):
        return self.summed_finishes / self.games_played

    def get_finishes(self):
        return self.finishes

    def get_string_finishes(self):
        result = ''
        for elem in self.finishes:
            result += f'{elem[0]:2}({elem[1]:2}), '

        return result
