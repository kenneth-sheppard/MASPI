from game_engine.helper import list_of_sea_factories
from game_engine.helper import list_of_land_factories
from game_engine.helper import tax_chart


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


class Investor(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Investor'
        self.players = None

    def action(self, country):
        # Make a dictionary of what people are owed
        owed = dict([(i, 0) for i in self.players])
        for bond in country.get_bonds():
            if bond.get_owner() is not None:
                owed[bond.get_owner()] += bond.get_interest_rate()

        while owed:
            next_up = (min(owed, key=owed.get), owed.get(min(owed, key=owed.get)))
            # If the player is owed money
            if next_up[1] > 0:
                # If the country has enough money to pay
                if country.get_treasury() >= next_up[1]:
                    country.remove_money(next_up[1])
                    next_up[0].add_money(next_up[1])
                # If the country doesn't have enough but has more than zero
                elif next_up[1] > country.get_treasury() > 0:
                    # Pay out rest of what country has
                    next_up[0].add_money(country.get_treasury())
                    owed[next_up[0]] -= country.get_treasury()
                    country.remove_money(country.get_treasury())
                    # Check if country controller is the player being paid
                    if country.get_controller() is not next_up[0]:
                        # get amount available
                        aa = country.get_controller().get_money()
                        if next_up[1] < aa:
                            next_up[0].add_money(next_up[1])
                            country.get_controller().remove_money(next_up[1])
                        else:
                            next_up[0].add_money(aa)
                            country.get_controller().remove_money(aa)
                # Country is broke, player must pay
                else:
                    if country.get_controller() is not next_up[0]:
                        aa = country.get_controller().get_money()
                        if next_up[1] < aa:
                            next_up[0].add_money(next_up[1])
                            country.get_controller().remove_money(next_up[1])
                        else:
                            next_up[0].add_money(aa)
                            country.get_controller().remove_money(aa)

            del owed[next_up[0]]


class Import(ActionSpace):
    def __init__(self):
        super().__init__()
        pass


class Production(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Production'

    def action(self, country):
        # Might want a helper action for adding pieces to a territory that can automatically resolve conflicts
        # Will eventually need a priority system in case not enough pieces probably
        for territory in country.get_home_territories():
            if territory.get_controller() is country or territory.get_controller() is None:
                if territory.has_factory():
                    if territory in list_of_land_factories:
                        if country.remove_tank_from_pool():
                            territory.set_num_tanks(territory.get_num_tanks() + 1)
                    elif territory in list_of_sea_factories:
                        if country.remove_ship_from_pool():
                            territory.set_num_ships(territory.get_num_ships() + 1)
            else:
                return 1


class Maneuver(ActionSpace):
    def __init__(self):
        super().__init__()
        pass


class Taxation(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Taxation'

    def action(self, country):
        amount = 0
        for territory in country.get_home_territories():
            if territory.get_controller() is country and territory.has_factory():
                amount += 2

        amount += len(country.get_controlled_neutral_territories())

        power_up, owner_payout = tax_chart(amount)

        amount -= country.get_placed_units()

        if amount < 0:
            amount = 0

        country.add_power(power_up)
        # Give money to controller
        country.get_controller().add_money(owner_payout)

        country.add_money(amount)

        return 0


class Factory(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Factory'

    def action(self, country, territory):
        if territory in country.get_home_territories():
            if country.get_treasury() >= 5:
                if not territory.has_factory():
                    # Might need a check in case the territory is occupied by hostiles
                    country.remove_money(5)
                    territory.build_factory()
                    if territory in list_of_land_factories:
                        country.remove_tank_factory_from_supply()
                    elif territory in list_of_sea_factories:
                        country.remove_ship_factory_from_supply()
                    return 0

        return 1

