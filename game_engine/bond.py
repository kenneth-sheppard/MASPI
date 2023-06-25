import game_engine.helper


class Bond:
    def __init__(self, country, cost, interest_rate):
        """
        A Bond object represents a single bond of a country, could be held by a player or the country itself.
        :param country: Country - the country associated with bond.
        :param cost: int - the price to acquire the bond (bigger number)
        :param interest_rate: int - the price paid out from the investor space (smaller number)
        """
        self.owner = None
        self.country = country
        if cost < interest_rate:
            raise RuntimeError('A Bond\'s Cost must be less than its Interest!')
        self.cost = cost
        self.interest_rate = interest_rate

    def __str__(self):
        """
        A String representation of a bond
        :return: String - [Country] - [Cost]([Interest Rate])
        """
        return f'{self.country.get_name()} - {self.cost}({self.interest_rate})'

    def get_country(self):
        """
        Returns the owning country.
        :return: Country - The owning country.
        """
        return self.country

    def get_cost(self):
        """
        getter for cost variable
        :return: int - The cost
        """
        return self.cost

    def get_interest_rate(self):
        """
        getter for interest_rate variable
        :return: int - The interest rate
        """
        return self.interest_rate

    def get_owner(self):
        """
        getter for the owner variable
        If no player owns this bond, returns None.
        :return: None or Player
        """
        return self.owner

    def set_owner(self, o):
        """
        setter for the owner variable
        :param o: None or Owner - the new Owner
        """
        self.owner = o

    def get_value(self):
        """
        getter for the value variable
        :return: int - interest_rate * power of country
        """
        return self.interest_rate * game_engine.helper.power_chart(self.country.get_power())

    def to_numbers(self):
        """
        formats the bond for use in the neural network
        :return: List - hot-encoded owner with cost and interest rate
        """
        numerical_representation = [0, 0, 0, 0, 0, 0, self.cost, self.interest_rate]
        if self.owner is not None:
            numerical_representation[self.owner.get_id()] = 1

        return numerical_representation
