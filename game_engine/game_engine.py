import time
import game_engine.game_setup
from game_engine import helper as helper


class GameEngine:
    def __init__(self):
        """
        A GameEngine is responsible for manipulating the game_state at a macro level.
        Also holds subscribers watching and gathering information.
        """
        self.state = game_engine.game_setup.setup()
        self.subscribers = []
        self.active_country = None
        self.active_player = None
        self.turns = 0

    def play(self):
        """
        Plays the game, ends when a country has reached power 25, or it is turn 300.
        """
        while not self.state.is_over():
            # turn_start_time = time.time()

            if self.turns % 6 == 0:
                pass
                # print(f'Turn - {self.turns // 6}')
                # print(self.state)

            if self.turns // 6 == 100:
                break

            # Get the active country
            self.__next_active_country()
            # Get the active player of the active country
            self.active_player = self.active_country.get_country_controller()
            # Ask that player to choose how far on the rondel they want to go
            # Tax the player if moving too far
            if self.active_player is not None:
                if self.turns // 6 == 0:
                    move = self.__turn_one_move_query()
                else:
                    move = self.__move_query()
            # Advance that many spaces on the rondel
                self.active_country.advance(move, self.state)
            # Activate that action space on the rondel
                self.active_country.get_rondel_space().get_action().action(self.active_country, self.active_player, self.state)
            # Activate the investor card if Investor Space was passed
                if self.state.get_delayed_investor_card():
                    self.state.do_investor_card()
                    self.state.set_delayed_investor_card(False)
            # Update the game state
            self.state.update()

            # turn_end_time = time.time()

            # print(f'elapsed time {turn_end_time - turn_start_time}s')

            self.turns += 1

            # if there are subscribed observers, let them observe
            for subscriber in self.subscribers:
                subscriber.observe()

        # for country in self.state.get_countries():
        #     pass
            # print(f'{country.get_name()} - {country.get_power()}')

        space = self.active_country.get_rondel_space()
        for i in range(0, 8):
            # print(f'{space.get_name()} - {space.get_action().get_times_activated()} times')
            space = space.next()

    def get_state(self):
        """
        getter for the state variable
        :return: GameState - the stored game state
        """
        return self.state

    def subscribe(self, observer):
        """
        Subscribes a subscriber that will watch and gather data of the gameplay
        :param observer: Observer - The Observer that will be added
        """
        self.subscribers.append(observer)

    def unsubscribe(self, game_state_observer):
        """
        Unsubscribes an observer.
        :param game_state_observer: Observer - The Observer that will be removed
        """
        self.subscribers.remove(game_state_observer)

    def get_turns(self):
        """
        getter for current elapsed turns
        :return: int - the amount of turns
        """
        return self.turns // 6

    def __next_active_country(self):
        """
        Finds the next active country using Strings and logic
        """
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
        self.state.set_active_country(self.active_country)

    def __move_query(self):
        """
        Queries the player how far they want to move, accounting for how much there money allows them to move.
        :return: int - the number that they can move
        """
        options = []

        for i in range(1, 7):
            if self.active_player.get_money() - max((i - 3), 0) * \
                    (1 + helper.power_chart(self.active_country.get_power())) >= 0:
                options.append(
                    [i, self.active_country.get_advance_option([i, 'None', 0], self.state).get_name(),
                     max((i - 3), 0) * (1 + helper.power_chart(self.active_country.get_power()))])

        return self.active_player.make_rondel_choice(options, self)

    def __turn_one_move_query(self):
        """
        Queries the player how far they want to move, accounting for how much there money allows them to move.
        :return: int - the number that they can move
        """
        options = []

        for i in range(1, 9):
            options.append([i, self.active_country.get_advance_option([i, 'None', 0], self.state).get_name(), 0])

        return self.active_player.make_rondel_choice(options, self)


def potential_advance(choice, engine):
    """
    Used to try and predict future possibilities
    :param choice: List[int] - how many space to move
    :param engine: GameEngine - the game engine copy that will be acted upon
    :return: GameEngine - the resulting GameEngine
    """
    # Advance that many spaces on the rondel
    engine.active_country.hypothetical_advance(choice, engine.get_state())

    return engine


def reverse_advance(choice, engine):
    """
    Used to try and reverse the prediction of future possibilities
    :param choice: List[int] - how many space to move
    :param engine: GameEngine - the game engine copy that will be acted upon
    :return: GameEngine - the resulting GameEngine
    """
    engine.active_country.reverse(choice, engine.get_state())

    return engine
