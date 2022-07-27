

class Territory:
    def __init__(self, name, t_id):
        self.name = name
        self.id = t_id
        self.controller = None
        self.factory = False
        self.num_tanks = 0
        self.num_ships = 0

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_controller(self):
        return self.controller

    def set_controller(self, c):
        self.controller = c

    def has_factory(self):
        return self.factory

    def build_factory(self):
        if not self.factory:
            self.factory = True
        return self.factory

    def get_num_tanks(self):
        return self.num_tanks

    def set_num_tanks(self, t):
        self.num_tanks = t

    def get_num_ships(self):
        return self.num_ships

    def set_num_ships(self, s):
        self.num_ships = s
