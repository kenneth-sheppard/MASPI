import game_engine.game_setup
import game_engine.helper as helper


class GameEngine:
    def __init__(self):
        self.state = game_engine.game_setup.setup()
        self.active_country = None
        self.active_player = None

    def play(self):
        while not self.state.is_over():
            # Get the active country
            self.__next_active_country()
            # Get the active player of the active country
            self.active_player = self.active_country.get_controller()
            # Ask that player to choose how far on the rondel they want to go
            ntm = self.active_player.make_rondel_choice(
                [[o, self.active_country.hypothetical_advance(o).get_name()] for o in range(1, 7)],
                self.state
            )[0]
            # Tax the player if moving too far
            self.__move_tax(ntm)
            # Advance that many spaces on the rondel
            self.active_country.advance(ntm)
            # Activate that action space on the rondel
            self.active_country.get_rondel_space().get_action().action(self.active_country, self.active_player, self.state)
            # Update the game state
            self.state.update()

    def __next_active_country(self):
        if self.active_country is None or self.active_country.get_name() == 'European Union':
            self.active_country = self.state.get_country('Russia')
        elif self.active_country.get_name() == 'Russia':
            self.active_country = self.state.get_country('China')
        elif self.active_country.get_name() == 'China':
            self.active_country = self.state.get_country('India')
        elif self.active_country.get_name() == 'India':
            self.active_country = self.state.get_country('Brazil')
        elif self.active_country.get_name() == 'Brazil':
            self.active_country = self.state.get_country('America')
        elif self.active_country.get_name() == 'America':
            self.active_country = self.state.get_country('European Union')

    def __move_tax(self, ntm):
        # TODO cannot go negative in money
        if ntm > 3:
            self.active_player.remove_money((ntm - 3) * (1 + helper.power_chart(self.active_country.get_power())))

        return
        