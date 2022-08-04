

class ActionSpace:
    def __init__(self):
        self.name = None
        self.next_action = None

    def get_name(self):
        return self.name

    def get_next_action(self):
        return self.next_action

    def set_next_action(self, na):
        self.next_action = na

    def action(self):
        pass


class Investor(ActionSpace):
    def __init__(self):
        pass


class Import(ActionSpace):
    def __init__(self):
        pass


class Production(ActionSpace):
    def __init__(self):
        pass


class Maneuver(ActionSpace):
    def __init__(self):
        pass


class Taxation(ActionSpace):
    def __init__(self):
        pass


class Factory(ActionSpace):
    def __init__(self):
        ActionSpace()
        self.name = 'Factory'

    def action(self, territory):
        territory.build_factory()
