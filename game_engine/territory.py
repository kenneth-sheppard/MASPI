

class Territory:
    def __init__(self, name, t_id):
        self.name = name
        self.id = t_id
        self.controller = None
        self.factory = False
        self.factory_is_sea = False
        self.is_neutral = True
        self.tanks = {
            'Russia': 0,
            'China': 0,
            'India': 0,
            'Brazil': 0,
            'America': 0,
            'European Union': 0
        }
        self.ships = {
            'Russia': 0,
            'China': 0,
            'India': 0,
            'Brazil': 0,
            'America': 0,
            'European Union': 0
        }
        self.is_water = False
        self.is_costal = False

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

    def get_tanks(self):
        return self.tanks

    def get_num_tanks(self, country_name):
        return self.tanks[country_name]

    def set_num_tanks(self, country_name, tanks):
        self.tanks[country_name] = tanks

    def get_ships(self):
        return self.ships

    def get_num_ships(self, country_name):
        return self.ships[country_name]

    def set_num_ships(self, country_name, ships):
        self.ships[country_name] = ships

    def get_is_water(self):
        return self.is_water

    def set_is_water(self, w):
        self.is_water = w
