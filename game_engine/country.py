import game_engine.rondel
from game_engine.helper import tax_chart


class Country:
    def __init__(self, name, c_id):
        """
        A Country represents one of the six superpowers that are controlled by the players.
        Countries hold pools of units (Tanks and Ships).
        Countries have nine bonds that can be bought by players over the course of the game.
        The Player who controls the largest stake in a given country becomes its controller.
        The Controller is responsible for making gameplay choices when the Country acts.
        Countries hold a space on the power track, when one hits 25 the game ends.
        :param name: String - the name of the country [Russia, China, India, Brazil, America, European Union]
        :param c_id: int - the id of the country (0-5) ((1-6)??)
        """
        self.name = name
        self.id = c_id
        self.starting_tanks = 0
        self.starting_ships = 0
        self.starting_check = True
        self.tank_pool = 0
        self.tank_factory_pool = 0
        self.ship_pool = 0
        self.ship_factory_pool = 0
        self.bonds = {}
        self.treasury = 0
        self.controller = None
        self.power = 0
        self.controlled_neutral_territories = []
        self.home_territories = []
        self.flag_count = 0
        self.max_flags = 15
        self.is_occupied = False
        self.rondel_space = None

    def __str__(self):
        """
        The string representation of the country.
        :return: String - the name
        """
        return self.name

    def get_id(self):
        """
        The unique id of the country.
        :return: int - the id
        """
        return self.id

    def get_name(self):
        """
        The name only, this should stay the same but __str__ could change if needed.
        :return: String - the name
        """
        return self.name

    def get_tank_pool(self):
        """
        Returns how many tanks are available in reserve.
        :return: int
        """
        return self.tank_pool

    def remove_tank_from_pool(self):
        """
        Remove a tank from the pool of reserve tanks, cannot remove a tank if None are present (0)
        :return: Boolean - True if process succeeded, False otherwise
        """
        if self.tank_pool <= 0:
            return False
        else:
            self.tank_pool -= 1
            return True

    def add_tank_to_pool(self):
        """
        Add a tank to the reserve pool
        """
        self.tank_pool += 1

    def get_ship_pool(self):
        """
        Returns how many ships are available in the pool
        :return: int
        """
        return self.ship_pool

    def remove_ship_from_pool(self):
        """
        Remove a ships from the pool of reserve ships, cannot remove a ships if None are present (0)
        :return: Boolean - True if process succeeded, False otherwise
        """
        if self.ship_pool <= 0:
            return False
        else:
            self.ship_pool -= 1
            return True

    def add_ship_to_pool(self):
        """
        Add a ship to the reserve pool
        """
        self.ship_pool += 1

    def add_tank_factory_to_supply(self):
        """
        Add a factory to the pool of available tank factories
        :return: boolean - True
        """
        self.tank_factory_pool += 1
        return True

    def remove_tank_factory_from_supply(self):
        """
        Remove a factory from the pool of available tank factories
        :return: boolean - True if there are available factories, False otherwise
        """
        if self.tank_factory_pool > 0:
            self.tank_factory_pool -= 1
            return True
        else:
            return False

    def add_ship_factory_to_supply(self):
        """
        Add a factory to the pool of available ship factories
        :return: boolean - True
        """
        self.ship_factory_pool += 1
        return True

    def remove_ship_factory_from_supply(self):
        """
        Remove a factory from teh pool of available ship factories
        :return: boolean - True if there are available factories, False otherwise
        """
        if self.ship_factory_pool > 0:
            self.ship_factory_pool -= 1
            return True
        else:
            return False

    def get_bonds(self):
        """
        Return a list of all bonds associated with the country
        :return: List - the bonds for this country
        """
        return self.bonds.values()

    def get_bond(self, bond_cost):
        """
        Get a specific bond, using the cost (larger number) for sorting
        :param bond_cost: int - the cost of the bond (2, 4...30)
        :return: None or Bond - the appropriate bond, could be None if bond was removed
        """
        return self.bonds[bond_cost]

    def add_bond(self, bond):
        """
        Add a bond to the bond dict
        :param bond: Bond - a bond to be added, stored based on cost
        """
        self.bonds[bond.cost] = bond

    def remove_bond(self, bond):
        """
        Remove a bond from the dict
        :param bond: Bond - the bond to be removed, replaced with None
        """
        self.bonds[bond.cost] = None

    def get_player_investments(self, player):
        """
        Count how much a player holds in the country, by bond interest rate
        :param player: Player - The player to check
        :return: Integer - the sum of interest rates for bonds held by Player
        """
        count = 0
        for bond in self.bonds:
            if bond.get_owner() == player:
                count += bond.get_interest_rate()

        return count

    def get_total_payout(self):
        """
        Calculate how much money must be spent to pay all bonds
        :return: the calculated amount
        """
        payout = 0
        for bond in self.bonds:
            if bond.get_owner() is not None:
                payout += bond.get_interest_rate()

        return payout

    def get_treasury(self):
        """
        getter for treasury
        :return: int - the treasury variable
        """
        return self.treasury

    def add_money(self, amount):
        """
        add money to current bank
        :param amount: int - the amount to add
        """
        self.treasury += amount

    def remove_money(self, amount):
        """
        Remove money from the bank. Cannot remove more than is present currently in the bank.
        :param amount: int - the amount to remove
        :return: Boolean - True if operation succeeded, False otherwise
        """
        if self.treasury >= amount:
            self.treasury -= amount
            return True

        return False

    def get_country_controller(self):
        """
        getter for controller variable
        :return: Player - the Player that has the controlling stake currently.
        """
        return self.controller

    def set_country_controller(self, player):
        """
        setter for controller variable
        :param player: Player - the new controller
        """
        self.controller = player

    def get_power(self):
        """
        getter for power variable
        :return: int - the power variable
        """
        return self.power

    def add_power(self, amount):
        """
        increase the power by an amount. This value can never exceed 25.
        :param amount: int - the amount to be increased by
        """
        self.power += amount
        if self.power > 25:
            self.power = 25

    def get_tax_payout(self):
        """
        Get the amount that will be paid to the controller if a tax were to occur immediately
        :return: int - the calculated number
        """
        count = 0

        for territory in self.get_home_territories():
            if not territory.is_occupied() and territory.has_factory():
                count += 2

        count += len(self.get_controlled_neutral_territories())

        _, owner_payout = tax_chart(count)

        return owner_payout

    def get_tax_increase(self):
        """
        Get the amount that will be paid to the controller if a tax were to occur immediately
        :return: int - the calculated number
        """
        count = 0

        for territory in self.get_home_territories():
            if not territory.is_occupied() and territory.has_factory():
                count += 2

        count += len(self.get_controlled_neutral_territories())

        increase, _ = tax_chart(count)

        return increase

    def get_controlled_neutral_territories(self):
        """
        getter for controlled neutral territories
        :return: List - a list of the territories
        """
        return self.controlled_neutral_territories

    def add_controlled_neutral_territory(self, territory):
        """
        add a territory to the list of controlled territories.
        :param territory: Territory - the territory to be added
        """
        self.controlled_neutral_territories.append(territory)

    def remove_controlled_neutral_territory(self, territory):
        """
        remove a territory from the list of controlled territories, if present
        :param territory: Territory - the territory to be removed
        :return: Boolean - True if found, False otherwise
        """
        if territory in self.controlled_neutral_territories:
            self.controlled_neutral_territories.remove(territory)
            return True
        return False
        
    def get_home_territories(self):
        """
        getter for home_territories variable
        :return: List - home territories of this Country
        """
        return self.home_territories

    def set_home_territories(self, territories):
        """
        setter for home_territories variable
        :param territories: List - home territories of this Country
        """
        self.home_territories = territories

    def get_placed_units(self):
        """
        get the amount of units currently on the board, the difference between what starts in the pools and what is now
        present
        :return: int - diff between starting pools and current pools
        """
        return (self.starting_tanks - self.tank_pool) + (self.starting_ships - self.ship_pool)

    def place_flag(self):
        """
        place a flag on the board
        :return: True if there are flags to place, False otherwise
        """
        if self.flag_count > 0:
            self.flag_count -= 1
            return True
        return False

    def pickup_flag(self):
        """
        pickup a flag from the board, increases the amount of flags in the flag pool
        """
        self.flag_count += 1

    def get_placed_flags(self):
        return self.max_flags - self.flag_count

    def get_total_flags(self):
        return self.max_flags

    def sell_bond(self, bond, player):
        """
        sell a bond to a player, only responsible for transferring ownership, does not currently handle money
        :param bond: Bond - the bond to be sold
        :param player: Player - the player gaining ownership
        """
        self.bonds[bond.cost].set_owner(player)

    def reclaim_bond(self, bond):
        """
        reclaim a bond, setting the current owner to the default value (None)
        :param bond: Bond - the bond to be reclaimed
        """
        self.bonds[bond.cost].set_owner(None)

    def advance(self, num_to_advance, game_state):
        """
        Moves the marker around the rondel, jumping from space to space and storing the last space visited
        :param num_to_advance: int - the number of spaces to jump
        :param game_state: GameState - used to access the rondel, probably could be passed directly
        """
        if self.rondel_space is None:
            self.rondel_space = game_engine.rondel.start(num_to_advance)
        else:
            self.rondel_space = game_engine.rondel.advance(self.rondel_space, num_to_advance, game_state)

    def get_advance_option(self, num_to_advance):
        """
        Returns a hypothetical advance, never changing the true state of the rondel
        :param num_to_advance:
        :return:
        """
        if self.rondel_space is None:
            return game_engine.rondel.start(index_to_start=num_to_advance)
        else:
            return game_engine.rondel.hypothetical_advance(rondel_space=self.rondel_space, num_to_move=num_to_advance)

    def hypothetical_advance(self, num_to_advance):
        """
        Performs a hypothetical advance, never changing the true state of the rondel
        :param num_to_advance:
        """
        if self.rondel_space is None:
            self.starting_check = True
            self.rondel_space = game_engine.rondel.start(num_to_advance)
        else:
            self.rondel_space = game_engine.rondel.hypothetical_advance(rondel_space=self.rondel_space, num_to_move=num_to_advance)

    def reverse(self, num_to_advance):
        if self.rondel_space is None:
            raise RuntimeError('Tried to reverse without setting the rondel space first!')
        elif self.starting_check:
            self.starting_check = False
            self.rondel_space = None
        else:
            self.rondel_space = game_engine.rondel.reverse(rondel_space=self.rondel_space, num_to_move=num_to_advance)

    def get_rondel_space(self):
        """
        getter for rondel space
        :return: RondelSpace - the current space the Country is at
        """
        return self.rondel_space

    def to_numbers(self):
        """
        Converts the country into a set of numbers for the neural network, including calls down to the bond representation
        :return: List - some numbers in a list
        """
        numerical_representation = [self.power, self.treasury, self.tank_pool, self.ship_pool]
        controller_list = [0, 0, 0, 0, 0, 0]
        if self.controller is not None:
            controller_list[self.controller.get_id()] = 1
        numerical_representation.extend(controller_list)
        rondel_space_list = [0, 0, 0, 0, 0, 0, 0, 0]
        if self.rondel_space is not None:
            rondel_space_list[self.rondel_space.get_id()] = 1
        numerical_representation.extend(rondel_space_list)
        for bond in self.bonds.values():
            numerical_representation.extend(bond.to_numbers())
        return numerical_representation
