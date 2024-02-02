import numpy as np


class Territory:
    def __init__(self, name, t_id):
        self.name = name
        self.id = t_id
        self.controller = None
        self.factory = False
        self.factory_is_sea = False
        self.is_neutral = True
        self.in_country = None
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
        self.has_peace = False

    def __str__(self):
        return self.name

    def get_name(self):
        """
        Gets the name of the territory
        :return: Name of territory as String
        """
        return self.name

    def get_id(self):
        """
        Territory ids are numeric and stored in helper.py
        :return: ID of territory as int
        """
        return self.id

    def get_territory_controller(self):
        """
        Territory Controllers are the Countries stored as Strings
        :return: Controller name as String
        """
        return self.controller

    def set_territory_controller(self, c):
        """
        Territory Controllers are the Countries stored as Strings
        :param c: The name of the controlling country as a String
        """
        self.controller = c

    def has_factory(self):
        """
        Factories must be present to add units during production
        :return: boolean True if there is a factory, False otherwise
        """
        return self.factory

    def build_factory(self):
        """
        Builds a factory if there is not one present
        :return: boolean True if there is a factory, False otherwise
        """
        if not self.factory:
            self.factory = True
            if self.factory_is_sea:
                self.in_country.remove_ship_factory_from_supply()
            else:
                self.in_country.remove_tank_factory_from_supply()
        return self.factory

    def destroy_factory(self):
        """
        Removes a factory if present
        :return: boolean True if there is a factory, False otherwise
        """
        if self.factory:
            self.factory = False
            if self.factory_is_sea:
                self.in_country.add_ship_factory_to_supply()
            else:
                self.in_country.add_tank_factory_to_supply()
        return self.factory

    def get_tanks(self):
        """
        Returns the tanks present
        :return: Dict of tanks present represented by a count of 1 per tank
        """
        return self.tanks

    def add_tank(self, country_name):
        """
        Adds a tank to the dictionary
        :param country_name: The name of the country adding a tank String
        """
        self.tanks[country_name] += 1

    def remove_tank(self, country_name):
        """
        Remove a tank from the country in the dictionary
        :param country_name: The name of the country removing a tank String
        """
        if self.tanks[country_name] > 0:
            self.tanks[country_name] -= 1
        else:
            raise ValueError('There are no tanks to remove!')

    def get_num_tanks(self, country_name):
        """
        Returns the number of tanks possessed by a specific country
        :param country_name: The name of the country to retrieve String
        :return: The amount of tanks as an int
        """
        return self.tanks[country_name]

    def set_num_tanks(self, country_name, tanks):
        """
        Sets the value of a countries tanks at a fixed number
        :param country_name: The name of country adding tanks String
        :param tanks: The amount to set to as an int
        """
        self.tanks[country_name] = tanks

    def get_ships(self):
        """
        Retrieve the dictionary representing ships at the territory
        :return: Dick of Ships represented by a count of 1 per ship
        """
        return self.ships

    def add_ship(self, country_name):
        """
        Adds a ship to the dictionary
        :param country_name: The name of the country adding a ship String
        """
        self.ships[country_name] += 1

    def remove_ship(self, country_name):
        """
        Remove a ship from the country in the dictionary
        :param country_name: The name of the country removing a ship String
        """
        if self.ships[country_name] > 0:
            self.ships[country_name] -= 1
        else:
            raise ValueError('There are no ships to remove!')

    def get_num_ships(self, country_name):
        """
        Returns the number of ships possessed by a specific country
        :param country_name: The name of the country to retrieve String
        :return: The amount of ships as an int
        """
        return self.ships[country_name]

    def set_num_ships(self, country_name, ships):
        """
        Sets the value of a countries ships at a fixed number
        :param country_name: The name of country adding ships String
        :param ships: The amount to set to as an int
        """
        self.ships[country_name] = ships

    def get_is_water(self):
        """
        Countries that are water can be traversed by ships
        See helper for table of is water or not
        :return: boolean, True if is water, False if otherwise
        """
        return self.is_water

    def set_is_water(self, w):
        """
        Used to set if the country is water, should only be used once at the start of the game
        :param w: boolean True if is water, False otherwise
        """
        self.is_water = w

    def get_in_country(self):
        """
        Returns if territory is a part of a country, one of the four home territories
        :return: Country - the country that the territory is in, or None
        """
        return self.in_country

    def is_occupied(self):
        """
        Checks if there are enemy units in a home territory
        :return: boolean True if there are, False otherwise
        """
        if self.in_country:
            for c_name, count in self.tanks.items():
                if count > 0 and c_name != self.in_country.get_name():
                    return True

        return False

    def get_factory_is_sea(self):
        """
        Represents whether the factory can make ships or not
        :return: boolean True if it can, false otherwise
        """
        return self.factory_is_sea

    def get_has_peace(self):
        return self.has_peace

    def set_has_peace(self, peace):
        self.has_peace = peace

    def to_numbers(self):
        """
        Used when representing the territory for the neural network
        :return: A set of values, either 0 or 1 for controller, then lists for ships and tanks present as one [List]
        """
        numerical_representation = []
        if self.controller == 'Russia':
            numerical_representation.extend([1, 0, 0, 0, 0, 0])
        elif self.controller == 'China':
            numerical_representation.extend([0, 1, 0, 0, 0, 0])
        elif self.controller == 'India':
            numerical_representation.extend([0, 0, 1, 0, 0, 0])
        elif self.controller == 'Brazil':
            numerical_representation.extend([0, 0, 0, 1, 0, 0])
        elif self.controller == 'America':
            numerical_representation.extend([0, 0, 0, 0, 1, 0])
        elif self.controller == 'European Union':
            numerical_representation.extend([0, 0, 0, 0, 0, 1])
        else:
            numerical_representation.extend([0, 0, 0, 0, 0, 0])
        # if self.factory:
        #     numerical_representation.append(1)
        # else:
        #     numerical_representation.append(0)
        # if self.is_neutral:
        #     numerical_representation.append(1)
        # else:
        #     numerical_representation.append(0)
        # if self.is_water:
        #     numerical_representation.append(1)
        # else:
        #     numerical_representation.append(0)
        numpy_tanks = np.array(list(self.tanks.values()))
        numpy_ships = np.array(list(self.ships.values()))
        numerical_representation.extend(np.add(numpy_tanks, numpy_ships).tolist())

        return numerical_representation
