import game_engine.action_space as action_space


def start(index_to_start):
    starting_space = investor
    for i in range(0, index_to_start):
        starting_space = starting_space.next()

    return starting_space


class RondelSpace:
    def __init__(self, action):
        self.action = action
        self.next_space = None

    def set_next_space(self, rondel_space):
        self.next_space = rondel_space

    def next(self):
        return self.next_space

    def get_action(self):
        return self.action

    def get_name(self):
        return self.action.get_name()


def advance(rondel_space, num_to_move):
    for i in range(0, num_to_move):
        rondel_space = rondel_space.next()

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
