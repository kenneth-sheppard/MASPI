

class GameState:
    def __init__(self):
        """
        Initialized GameStates take no parameters, should be filled up during the setup script
        Then passed to a game engine for playing in a game.
        Territories - Dict {key - id(int) : value - territory(Territory)
        Countries - Dict {key - name(string) : value - country(Country)
        Players - List [(Player)]
        Investor Card - instance of InvestorCard
        """
        self.territories = {}
        self.countries = {}
        self.players = []
        self.active_country = None
        self.investor_card = None
        self.delayed_investor_card = False

    def __str__(self):
        """
        Mostly here to be used for debugging, print out relevant characteristics of the state of the game
        :return: String - game info
        """
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
        """
        Add element to the territories dictionary
        :param t: Territory - the territory to be added
        """
        self.territories[t.get_id()] = t

    def remove_territory(self, t):
        """
        Remove a territory from the territories dictionary
        :param t: Territory - the territory to be removed
        """
        self.territories.pop(t.get_id())

    def get_territory(self, t_id):
        """
        getter for territory
        :param t_id: int - the id of a territory to be retrieved (see helper for list of ids)
        :return: Territory - the territory object
        """
        return self.territories.get(t_id)

    def update_territory(self, t):
        """
        change a territory to a newer version of that territory
        :param t:
        """
        self.territories[t.get_id()] = t

    def get_territories(self):
        """
        get the whole dictionary of territories
        :return: Dict - the dictionary of territories
        """
        return self.territories

    def add_country(self, c):
        """
        add a country to the dictionary
        :param c: Country - stored using the name as the key
        """
        self.countries[c.get_name()] = c

    def remove_country(self, c):
        """
        remove a country from the dictionary
        :param c: Country - the country to be removed
        """
        self.countries.pop(c.get_name())

    def update_country(self, new_c):
        """
        update a country to a new version
        :param new_c: the country to replace its older version
        """
        self.countries[new_c.get_name()] = new_c

    def get_countries(self):
        """
        get the full list of countries
        :return: List - the values stored in the countries dict
        """
        return list(self.countries.values())

    def set_countries(self, sc):
        """
        set the full dictionary of countries to a new dictionary
        :param sc:
        """
        self.countries = sc

    def get_country(self, c_name):
        """
        getter for a country in the dictionary
        :param c_name: String - the key for the appropriate country
        :return: The country object
        """
        try:
            return self.countries[c_name]
        except KeyError:
            return None

    def get_active_country(self):
        """
        get the current active country.
        :return: Country - the Country object
        """
        return self.active_country

    def set_active_country(self, country):
        """
        set the current active country.
        :param country: Country - the Country object
        """
        self.active_country = country

    def get_bond(self, bond):
        """
        getter for a bond of a country (used specifically for hypothetical actions
        :param bond: Bond - the bond to retrieved and modified
        :return: Bond - the bond
        """
        return self.get_country(bond.get_country().get_name()).get_bond(bond.get_cost())

    def add_player(self, p):
        """
        add a player to the list
        :param p: Player - the player to be added
        """
        self.players.append(p)

    def get_players(self):
        """
        getter for the list of players
        :return: List - the list of players
        """
        return self.players

    def get_player(self, p_id):
        """
        get a specific player from the list
        :param p_id: int - the id of the player that is desired
        :return: Player - found by iterating through the list until a matching id is found
        """
        for player in self.players:
            if player.get_id() == p_id:
                return player

    def get_winner(self):
        """
        calculate the winning player by finding the one with the highest worth
        :return: Player - the player with the highest worth
        """
        winner = None
        for player in self.players:
            if winner is None:
                winner = player
            elif player.get_worth() > winner.get_worth():
                winner = player
            elif player.get_worth() == winner.get_worth():
                # TODO implement tiebreaker rules for scoring here
                pass

        if winner is None:
            raise RuntimeError('No players were identified in the game')

        return winner

    def get_loser(self):
        """
        calculate the player with the lowest worth
        :return: Player - the player with the lowest worth
        """
        loser = None
        for player in self.players:
            if loser is None:
                loser = player
            elif player.get_worth() < loser.get_worth():
                loser = player
            elif player.get_worth() == loser.get_worth():
                pass

        if loser is None:
            raise RuntimeError('No players were identified in the game')

        return loser

    def update(self):
        """
        update the game state after a move
        :return: int
        """
        # Update each territory and check for new flag
        self.__update_territories()
        # Update each country checking for new controller
        self.__update_countries()
        # Update each player checking for change in swiss bank
        self.__update_players()

        return 0

    def is_over(self):
        """
        checks to see if the game has ended
        :return: boolean - True if a country is at 25 power
        """
        for country in self.countries.values():
            if country.get_power() == 25:
                return True

        return False

    def __update_territories(self):
        """
        Iterate through each territory that is not a part of a superpower
        For water territories check boats to see if only one player is present
        Repeat for neutral territories with tanks
        In both cases if true add a flag for the player that controls
        Return any other flags to the owner
        :return:
        """
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
            if territory.is_neutral and len(players_in_territory) == 1:
                for country in self.countries.values():
                    if country.remove_controlled_neutral_territory(territory):
                        country.pickup_flag()
                c_name = players_in_territory[0]
                if self.get_country(c_name).place_flag():
                    territory.set_territory_controller(c_name)
                    self.get_country(c_name).add_controlled_neutral_territory(territory)
            # Territory is not neutral
            elif territory.is_neutral:
                pass
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
        """
        Update the countries by checking for changes in ownership
        :return: int
        """
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
        """
        Update players checking for new ownership and if any players become swiss banks
        :return:
        """
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

    def get_delayed_investor_card(self):
        """
        Check if an investor card trigger needs to occur after an action completes
        :return: Boolean - True if needed trigger, False otherwise
        """
        return self.delayed_investor_card

    def set_delayed_investor_card(self, sdic):
        """
        Set the value of delayed_investor_card
        :param sdic: Boolean True if needed trigger, False otherwise
        """
        self.delayed_investor_card = sdic

    def do_investor_card(self):
        """
        Activate the investor card
        """
        self.investor_card.do_investor_card(self)

    def get_countries_sorted_by_power(self):
        """
        gets the countries sorted by power
        :return: List - countries sorted by power
        """
        return sorted(self.countries.values(), key=lambda country: country.power)

    def get_string_of_power_values(self):
        """
        used for debugging and/or recording data
        :return: String - power values for each country
        """
        countries = self.get_countries_sorted_by_power()
        result = ''
        for country in countries:
            result += f'{country.get_name()} : {country.get_power()} '

        return result

    def get_numerical_representation(self):
        """
        Ask all the objects to return their own numerical representations then put them all into a list.
        :return: List - all the information of the game state encoded
        """
        num_list = []
        for i in range(6):
            if i < len(self.players):
                num_list.extend(self.players[i].to_numbers())
            else:
                # Add an array of the same size that is filled with just 0's
                # This is to handle the case of less than 6 players
                num_list.extend([0, 0])

        for country in self.countries.values():
            num_list.extend(country.to_numbers())

        for territory in self.territories.values():
            num_list.extend(territory.to_numbers())

        num_list.extend(self.investor_card.to_numbers())

        return num_list

    def get_normalized_end_scores(self):
        """
        normalize the end score of all players by the score of the winning player
        :return: List - function(my_worth/winners_worth)
        """
        winner = self.get_winner()
        num_list = []
        for i in range(6):
            if i < len(self.players):
                num_list.append(self.players[i].get_worth() / winner.get_worth())
            else:
                num_list.append(0)

        return num_list

    def get_end_scores_between_zero_and_one(self):
        """
        calculate the score of the player subtracted from the lowest score divided by the winning score
        :return: List - function(my_worth-losers_worth/winners_worth-losers_worth)
        """
        winner = self.get_winner()
        loser = self.get_loser()
        num_list = []
        for i in range(6):
            if i < len(self.players):
                num_list.append(
                    (self.players[i].get_worth() - loser.get_worth()) / (winner.get_worth() - loser.get_worth()))
            else:
                num_list.append(0)

        return num_list

    def get_players_worth(self):
        """
        get the worth for a specific player
        :return: String - the worth formatted for recording purposes
        """
        result = ''
        for p in self.players:
            result += f'{p.get_id()} : {p.get_worth()} '

        return result
