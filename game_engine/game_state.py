

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

    def get_territories(self):
        return self.territories

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

    def update(self):
        # Update each territory and check for new flag
        self.__update_territories()
        # Update each country checking for new controller
        self.__update_countries()
        # Update each player checking for change in swiss bank
        pass

    def __update_territories(self):
        for territory in self.territories:
            players_in_territory = []
            if territory.is_water:
                # Count ships
                for c_name, c_pieces in territory.get_ships().items():
                    if c_pieces > 0:
                        players_in_territory.append(c_name)
            else:
                # Count tanks
                for c_name, c_pieces in territory.get_tanks().items():
                    if c_pieces > 0:
                        players_in_territory.append(c_name)
            # Update flag if there is exactly one country in neutral territory
            if territory.is_neutral:
                if len(players_in_territory) == 1:
                    c_name = players_in_territory[0]
                    if self.get_country(c_name).place_flag():
                        territory.controller = c_name
            # Territory is not neutral
            else:
                # If more than two people are in territory is occupied
                if len(players_in_territory) > 1:
                    self.get_country(territory.get_in_country()).is_occupied = True
                # If one player must check which
                elif len(players_in_territory) == 1:
                    territory.controller = players_in_territory[0]
                    if territory.get_in_country().get_name() != players_in_territory[0]:
                        self.get_country(territory.get_in_country()).is_occupied = True
                # If zero no action required
                else:
                    pass

    def __update_countries(self):
        pass