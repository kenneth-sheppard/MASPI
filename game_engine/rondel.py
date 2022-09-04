import game_engine.action_space as action_space


class Rondel:
    def __init__(self):
        self.name = 'Rondie'
        self.investor = RondelSpace(action_space.Investor())
        self.imports = RondelSpace(action_space.Import())
        self.production1 = RondelSpace(action_space.Production())
        self.maneuver1 = RondelSpace(action_space.Maneuver())
        self.taxation = RondelSpace(action_space.Taxation())
        self.factory = RondelSpace(action_space.Factory())
        self.production2 = RondelSpace(action_space.Production())
        self.maneuver2 = RondelSpace(action_space.Maneuver())
        self.investor.set_next_space(self.imports)
        self.imports.set_next_space(self.production1)
        self.production1.set_next_space(self.maneuver1)
        self.maneuver1.set_next_space(self.taxation)
        self.taxation.set_next_space(self.factory)
        self.factory.set_next_space(self.production2)
        self.production2.set_next_space(self.maneuver2)
        self.maneuver2.set_next_space(self.investor)

    def start(self, index_to_start):
        starting_space = self.investor
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

    def action(self):
        return self.action


def advance(rondel_space, num_to_move):
    for i in range(0, num_to_move):
        rondel_space = rondel_space.next()

    return rondel_space
