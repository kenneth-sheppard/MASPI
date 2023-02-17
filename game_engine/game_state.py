

class GameState:
    def __init__(self):
        self.territories = {}
        self.countries = {}
        self.players = []
        self.investor_card = None

    def __str__(self):
        output = ''
        for country in self.countries.values():
            output += f'{country.get_name()} - {country.get_power()}, '
        output += '\n'
        # for player in self.players:
        #     output += f'Player controlling {" ".join([c_name for c_name in player.get_controlled_countries()])} ' \
        #               f'current worth {player.get_worth()}\nPlayer bonds are {" ".join([str(b) for b in player.get_bonds()])}'
        #     output += '\n'

        # for territory in self.territories.values():
        #     output += f'{territory.get_name()} with flag of {territory.get_territory_controller()} and tanks {territory.get_tanks()} and ships {territory.get_ships()}\n'

        return output

    def add_territory(self, t):
        self.territories[t.get_id()] = t

    def remove_territory(self, t):
        self.territories.pop(t.get_id())

    def get_territory(self, t_id):
        return self.territories.get(t_id)

    def update_territory(self, t):
        self.territories[t.get_id()] = t

    def get_territories(self):
        return self.territories

    def add_country(self, c):
        self.countries[c.get_name()] = c

    def remove_country(self, c):
        self.countries.pop(c.get_name())

    def update_country(self, old_c, new_c):
        self.countries[old_c.get_name()] = new_c

    def get_countries(self):
        return list(self.countries.values())

    def set_countries(self, sc):
        self.countries = sc

    def get_country(self, c_name):
        try:
            return self.countries[c_name]
        except KeyError as e:
            print(e)
            print(c_name)
            input()

    def add_player(self, p):
        self.players.append(p)

    def get_players(self):
        return self.players

    def get_player(self, p_id):
        for player in self.players:
            if player.get_id() == p_id:
                return player

    def update(self):
        # Update each territory and check for new flag
        self.__update_territories()
        # Update each country checking for new controller
        self.__update_countries()
        # Update each player checking for change in swiss bank
        self.__update_players()

        return 0

    def is_over(self):
        for country in self.countries.values():
            if country.get_power() == 25:
                return True

        return False

    def __update_territories(self):
        for territory in self.territories.values():
            players_in_territory = []
            if territory.get_is_water():
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
                for country in self.countries.values():
                    if country.remove_controlled_neutral_territory(territory):
                        country.pickup_flag()
                if len(players_in_territory) == 1:
                    c_name = players_in_territory[0]
                    if self.get_country(c_name).place_flag():
                        territory.set_territory_controller(c_name)
                        self.get_country(c_name).add_controlled_neutral_territory(territory)

            # Territory is not neutral
            else:
                # If more than two people are in territory is occupied
                if len(players_in_territory) > 1:
                    self.get_country(territory.get_in_country().get_name()).is_occupied = True
                # If one player must check which
                elif len(players_in_territory) == 1:
                    territory.set_territory_controller(players_in_territory[0])
                    if territory.get_in_country().get_name() != players_in_territory[0]:
                        self.get_country(territory.get_in_country().get_name()).is_occupied = True
                # If zero no action required
                else:
                    pass

        return 0

    def __update_countries(self):
        for country in self.get_countries():
            bond_owners = dict([(i, 0) for i in self.get_players()])
            bond_owners[None] = 0
            for bond in country.get_bonds():
                bond_owners[bond.get_owner()] += bond.get_cost()

            bond_owners[None] = 0
            curr_owner = max(bond_owners, key=bond_owners.get)
            for player, amount_owned in bond_owners.items():
                if amount_owned == bond_owners[curr_owner] and player is not curr_owner:
                    # do nothing
                    return 0
            if bond_owners[curr_owner] > 0:
                if country.get_country_controller() is not curr_owner:
                    country.set_country_controller(curr_owner)

        return 0

    def __update_players(self):
        # Reset country ownership
        for player in self.get_players():
            player.reset_controlled_countries()
        # Go through the list of countries and assign them to their owners
        for country in self.get_countries():
            if country.get_country_controller():
                country.get_country_controller().add_controlled_country(country.name)
        # Check for swiss banks
        for player in self.get_players():
            if not player.get_controlled_countries():
                player.set_is_swiss_bank(True)

        return 0

    def do_investor_card(self):
        self.investor_card.do_investor_card(self)

    def get_countries_sorted_by_power(self):
        return sorted(self.countries.values(), key=lambda country: country.power)
