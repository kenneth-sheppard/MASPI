import game_engine.action_space as action_space


def start(index_to_start):
    """
    figure out what space on the rondel to start a given country
    :param index_to_start: int - the number of spaces to move forward from investor
    :return: RondelSpace - the starting space
    """
    starting_space = investor
    for i in range(0, index_to_start):
        starting_space = starting_space.next()

    return starting_space


space_id = 0


class RondelSpace:
    def __init__(self, action):
        """
        A rondel space has a specific action associated with it
        :param action:
        """
        self.action = action
        self.next_space = None
        self.previous_space = None
        global space_id
        self.id_count = space_id
        space_id = (space_id + 1) % 8

    def set_next_space(self, rondel_space):
        """
        setter for the next space on the rondel
        :param rondel_space: RondelSpace - the next space
        """
        self.next_space = rondel_space

    def set_previous_space(self, rondel_space):
        """
        setter for the previous space on the rondel to be used when reversing
        :param rondel_space: RondelSpace - the previous space
        """
        self.previous_space = rondel_space

    def next(self):
        """
        getter for the next space
        :return: RondelSpace - the next space
        """
        return self.next_space

    def previous(self):
        """
        getter for the previous space
        :return: RondelSpace - the previous space
        """
        return self.previous_space

    def get_action(self):
        """
        getter for the action associated with the space
        :return: ActionSpace - the action associated with the space
        """
        return self.action

    def get_name(self):
        """
        getter for the name of the space
        :return: String - the name of the action associated with the space
        """
        return self.action.get_name()

    def get_id(self):
        """
        getter for the id of the space
        :return: int - the id of the space
        """
        return self.id_count


def advance(rondel_space, num_to_move, game_state):
    """
    move from one state to the next space a number of times, maybe triggering the investor card
    :param rondel_space: RondelSpace - the current space
    :param num_to_move: int - the number of spaces to move
    :param game_state: GameState - the current game state
    :return: RondelSpace - the new space
    """
    for i in range(0, num_to_move):
        rondel_space = rondel_space.next()
        # If passing investor space trigger investor card in game_state
        if rondel_space is investor:
            game_state.set_delayed_investor_card(True)

    return rondel_space


# Hypothetical advance does not trigger the investor space
def hypothetical_advance(rondel_space, num_to_move):
    """
    move from one state to the next, not activating the investor space
    :param rondel_space: RondelSpace - the current space
    :param num_to_move: int - the number of spaces to move
    :return: RondelSpace - the new space
    """
    for i in range(0, num_to_move):
        rondel_space = rondel_space.next()

    return rondel_space


def reverse(rondel_space, num_to_move):
    """
    move from one state to the next, not activating the investor space
    :param rondel_space: RondelSpace - the current space
    :param num_to_move: int - the number of spaces to move
    :return: RondelSpace - the new space
    """
    for i in range(0, num_to_move):
        rondel_space = rondel_space.previous()

    return rondel_space


investor = RondelSpace(action_space.Investor())
imports = RondelSpace(action_space.Import())
production1 = RondelSpace(action_space.Production())
maneuver1 = RondelSpace(action_space.Maneuver())
taxation = RondelSpace(action_space.Taxation())
factory = RondelSpace(action_space.Factory())
production2 = RondelSpace(action_space.Production())
maneuver2 = RondelSpace(action_space.Maneuver())
investor.set_next_space(imports)
imports.set_next_space(production1)
production1.set_next_space(maneuver1)
maneuver1.set_next_space(taxation)
taxation.set_next_space(factory)
factory.set_next_space(production2)
production2.set_next_space(maneuver2)
maneuver2.set_next_space(investor)
maneuver2.set_previous_space(production2)
production2.set_previous_space(factory)
factory.set_previous_space(taxation)
taxation.set_previous_space(maneuver1)
maneuver1.set_previous_space(production1)
production1.set_previous_space(imports)
imports.set_previous_space(investor)
investor.set_previous_space(maneuver2)
