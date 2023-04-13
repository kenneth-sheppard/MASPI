

class GameState:
    def __init__(self):
        self.territories = []
        self.countries = []
        self.players = []
        self.investor_card = None

    def add_territory(self, t):
        self.territories.append(t)

    def remove_territory(self, t):
        self.territories.remove(t)

    def get_territory(self, t_id):
        for territory in self.territories:
            if territory.id == t_id:
                return territory
        return None

    def add_country(self, c):
        self.countries.append(c)

    def remove_country(self, c):
        self.countries.remove(c)

    def update_country(self, old_c, new_c):
        for i in range(0, len(self.countries)):
            if self.countries[i] is old_c:
                self.countries[i] = new_c
        return None

    def get_countries(self):
        return self.countries

    def set_countries(self, sc):
        self.countries = sc

    def get_country(self, c_name):
        for country in self.countries:
            if country.get_name() is c_name:
                return country

    def add_player(self, p):
        self.players.append(p)

    def get_players(self):
        return self.players

    def get_numerical_representation(self):
        num_list = []
        for player in self.players:
            num_list.append(player.to_numbers())

        for country in self.countries:
            num_list.append(country.to_numbers())

        for territory in self.territories:
            num_list.append(territory.to_numbers())

        num_list.append(self.investor_card.to_numbers())
