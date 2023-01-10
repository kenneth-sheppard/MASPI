import game_engine.game_setup


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
            self.active_player = self.state.get_country(self.active_country).get_controller
            # Ask that player to choose how far on the rondel they want to go
            ntm = self.active_player.make_choice(self.state)
            # Advance that many spaces on the rondel
            self.active_country.advance(ntm)
            # Activate that action space on the rondel
            self.active_country.get_rondel_space().action().action(self.active_country, self.active_player, self.state)
            # Update the game state
            self.state.update()

    def __next_active_country(self):
        if self.active_country is 'European Union' or self.active_country is None:
            self.active_country = 'Russia'
        elif self.active_country is 'Russia':
            self.active_country = 'China'
        elif self.active_country is 'China':
            self.active_country = 'India'
        elif self.active_country is 'India':
            self.active_country = 'Brazil'
        elif self.active_country is 'Brazil':
            self.active_country = 'America'
        elif self.active_country is 'America':
            self.active_country = 'European Union'
        