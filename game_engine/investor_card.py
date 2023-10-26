

class InvestorCard:
    def __init__(self):
        """
        The only thing tracked by the Investor Card is which player currently holds it
        """
        self.controller = None

    def get_controller(self):
        """
        getter for the controller
        :return: Player - the current holder of the card
        """
        return self.controller

    def set_controller(self, c):
        """
        setter for the controller
        :param c: Player - the next controller
        """
        self.controller = c

    def to_numbers(self):
        """
        convert to a numerical representation
        :return: List - hot encoded representation of the current holder
        """
        result = [0, 0, 0, 0, 0, 0]
        result[self.controller.get_player().get_id()] = 1
        return result

    def add_player(self, p):
        """
        used during setup, adds a new player to the list of players, players are chained together to track table position
        :param p: Player - the new player
        """
        # if no controller then this player is temporarily the controller
        if self.controller is None:
            self.controller = self.ICPlayer(p)
        # Otherwise add new players as the next player
        else:
            new_player = self.controller
            while new_player.get_next() is not None:
                new_player = new_player.get_next()

            new_player.set_next(self.ICPlayer(p))

    def done_adding_players(self):
        """
        used during setup, links the last player to the first then gives the card to the player next to the Russia player
        """
        # set the last player to loop back to the first
        last_player = self.controller
        while last_player.get_next() is not None:
            last_player = last_player.get_next()

        last_player.set_next(self.controller)

        found = True

        # now that done adding player move control to the Russia controller
        while 'Russia' not in self.controller.get_player().get_controlled_countries():
            # print('Next')
            self.controller = self.controller.get_next()
            if self.controller == last_player:
                found = False
                break

        if not found:
            while 'China' not in self.controller.get_player().get_controlled_countries():
                self.controller = self.controller.get_next()
                if self.controller == last_player:
                    break

        # card starts with the player next in turn order the Russia controller
        self.controller = self.controller.get_next()

    def do_investor_card(self, game_state):
        """
        performs the investor card action
        :param game_state: GameState - the game state to be acted upon
        """
        self.controller.get_player().add_money(2)
        # Create a list of all potential options
        invest(player=self.controller.get_player(), game_state=game_state)

        for player in game_state.get_players():
            if player.get_is_swiss_bank():
                invest(player=player, game_state=game_state)

        # Pass the card to the next player
        self.set_controller(self.get_controller().get_next())

    class ICPlayer:
        def __init__(self, player):
            """
            Tracks players and their order around the table
            :param player: Player - a player object
            """
            self.player = player
            self.next_player = None

        def set_next(self, next_player):
            """
            setter for the next player in seating order
            :param next_player: Player - the next player
            """
            self.next_player = next_player

        def get_next(self):
            """
            getter for the next player in seating order
            :return: Player - the next player
            """
            return self.next_player

        def get_player(self):
            """
            getter for the player represented by the ICPlayer
            :return: Player - this player
            """
            return self.player


def invest(player, game_state):
    # Available bonds with no controller direct buy
    # Start with default option of buying no bonds
    options = [[0, None, None, player.get_id()]]
    for country in game_state.get_countries():
        for bond in country.get_bonds():
            # Do not do the bonds that cannot be paid for
            if bond.get_owner() is None and bond.get_cost() <= player.get_money():
                # options are structured as amount to pay, bond to buy, bond to trade in
                options.append([bond.get_cost(), bond, None, player.get_id()])
    # Available bonds through trade in
    for country in game_state.get_countries():
        for bond in country.get_bonds():
            if bond.get_owner() is None:
                # Check if there is a lower bond to trade in
                # Do not do the bonds that cannot be paid for
                for owned_bond in player.get_bonds():
                    if (owned_bond.get_country() == bond.get_country() and
                            0 <= bond.get_cost() - owned_bond.get_cost() <= player.get_money()):
                        # options are structured as bond to buy then bond to trade in
                        options.append([bond.get_cost() - owned_bond.get_cost(), bond, owned_bond, player.get_id()])

    choice = player.make_investment_choice(options, game_state)

    if choice[1] is not None:
        player.buy_bond(choice[1], choice[2])

