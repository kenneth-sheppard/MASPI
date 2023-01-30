import game_engine.game_setup
import game_engine.helper as helper


class GameEngine:
    def __init__(self):
        self.state = game_engine.game_setup.setup()
        self.active_country = None
        self.active_player = None
        self.turns = 0

    def play(self):
        while not self.state.is_over():
            self.turns += 1

            if self.turns % 6 == 0:
                print(f'Turn - {self.turns // 6}')
                print(self.state)
            # Get the active country
            self.__next_active_country()
            # Get the active player of the active country
            self.active_player = self.active_country.get_country_controller()
            # Ask that player to choose how far on the rondel they want to go
            # Tax the player if moving too far
            ntm = self.__move_query()
            # Advance that many spaces on the rondel
            self.active_country.advance(ntm, self.state)
            # Activate that action space on the rondel
            self.active_country.get_rondel_space().get_action().action(self.active_country, self.active_player, self.state)
            # Update the game state
            self.state.update()

        for country in self.state.get_countries():
            print(f'{country.get_name()} - {country.get_power()}')

        space = self.active_country.get_rondel_space()
        for i in range(0, 8):
            print(f'{space.get_name()} - {space.get_action().get_times_activated()} times')
            space = space.next()

        print(self.state)

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

    def __move_query(self):
        options = []

        for i in range(0, 6):
            if self.active_player.get_money() - (i - 3) * \
                    (1 + helper.power_chart(self.active_country.get_power())) >= 0:
                options.append([i, self.active_country.hypothetical_advance(i).get_name()])

        ntm = self.active_player.make_rondel_choice(options, self.state)[0]

        if ntm > 3:
            self.active_player.remove_money((ntm - 3) * (1 + helper.power_chart(self.active_country.get_power())))

        return ntm
        