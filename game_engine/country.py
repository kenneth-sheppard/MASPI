

class Country:
    def __init__(self, name, c_id):
        self.name = name
        self.id = c_id
        self.starting_tanks = 0
        self.starting_ships = 0
        self.tank_pool = 0
        self.ship_pool = 0
        self.bonds = []
        self.treasury = 0
        self.controller = None
        self.power = 0
        self.controlled_neutral_territories = []
        self.home_territories = []
        self.flag_count = 0

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_tank_pool(self):
        return self.tank_pool

    def remove_tank_from_pool(self):
        if self.tank_pool <= 0:
            return False
        else:
            self.tank_pool -= 1
            return True

    def add_tank_to_pool(self):
        self.tank_pool += 1

    def get_ship_pool(self):
        return self.ship_pool

    def remove_ship_from_pool(self):
        if self.ship_pool <= 0:
            return False
        else:
            self.ship_pool -= 1
            return True

    def add_ship_to_pool(self):
        self.ship_pool += 1

    def get_bonds(self):
        return self.bonds

    def add_bond(self, bond):
        self.bonds.append(bond)

    def remove_bond(self, bond):
        self.bonds.remove(bond)

    def get_treasury(self):
        return self.treasury

    def add_money(self, amount):
        self.treasury += amount

    def remove_money(self, amount):
        if self.treasury >= amount:
            self.treasury -= amount
            return True

        return False

    def get_controller(self):
        return self.controller

    def set_controller(self, player):
        self.controller = player

    def get_power(self):
        return self.power

    def add_power(self, amount):
        self.power += amount
        if self.power > 25:
            self.power = 25

    def get_controlled_neutral_territories(self):
        return self.controlled_neutral_territories

    def add_controlled_neutral_territory(self, territory):
        self.controlled_neutral_territories.append(territory)

    def remove_controlled_neutral_territory(self, territory):
        self.controlled_neutral_territories.remove(territory)
        
    def get_home_territories(self):
        return self.home_territories

    def set_home_territories(self, territories):
        self.home_territories = territories

    def get_placed_units(self):
        return (self.starting_tanks - self.tank_pool) + (self.starting_ships - self.ship_pool)

    def to_numbers(self):
        return []
