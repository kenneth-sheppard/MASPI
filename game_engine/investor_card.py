

class InvestorCard:
    def __init__(self):
        self.controller = None

    def get_controller(self):
        return self.controller

    def set_controller(self, c):
        self.controller = c

    def add_player(self, p):
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
        # now that done adding player move control to the Russia controller
        while 'Russia' not in self.controller.get_player().get_controlled_countries():
            print('Next')
            self.controller = self.controller.get_next()

    def do_investor_card(self, game_state):
        self.controller.get_player().add_money(2)
        # Create a list of all potential options

        # Available bonds with no controller direct buy
        # Start with default option of buying no bonds
        options = [[0, None, None]]
        for country in game_state.get_countries():
            for bond in country.get_bonds():
                # Do not do the bonds that cannot be paid for
                if bond.get_owner() is None and bond.get_cost() <= self.controller.get_player().get_money():
                    # options are structured as amount to pay, bond to buy, bond to trade in
                    options.append([bond.get_cost(), bond, None])
        # Available bonds through trade in
        for country in game_state.get_countries():
            for bond in country.get_bonds():
                if bond.get_owner() is None and bond.get_cost() > self.controller.get_player().get_money():
                    # Check if there is a lower bond to trade in
                    # Do not do the bonds that cannot be paid for
                    for owned_bond in self.controller.get_player().get_bonds():
                        if owned_bond.get_owner() == bond.get_owner() and bond.get_cost() - owned_bond.get_cost() <= \
                                self.controller.get_player().get_money():
                            # options are structured as bond to buy then bond to trade in
                            options.append([bond.get_cost() - owned_bond.get_cost(), bond, owned_bond])

        choice = self.controller.get_player().make_investment_choice(options, game_state)

        if choice[1] is not None:
            self.controller.get_player().buy_bond(choice[1], choice[2])

        # Pass the card to the next player
        self.set_controller(self.get_controller().get_next())

    class ICPlayer:
        def __init__(self, player):
            self.player = player
            self.next_player = None

        def set_next(self, next_player):
            self.next_player = next_player

        def get_next(self):
            return self.next_player

        def get_player(self):
            return self.player
