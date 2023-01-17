

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
