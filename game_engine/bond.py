import game_engine.helper


class Bond:
    def __init__(self, country, cost, interest_rate):
        self.owner = None
        self.country = country
        self.cost = cost
        self.interest_rate = interest_rate

    def __str__(self):
        return f'{self.country.get_name()} - {self.cost}({self.interest_rate})'

    def get_country(self):
        return self.country

    def get_cost(self):
        return self.cost

    def get_interest_rate(self):
        return self.interest_rate

    def get_owner(self):
        return self.owner

    def set_owner(self, o):
        self.owner = o

    def get_value(self):
        return self.interest_rate * game_engine.helper.power_chart(self.country.get_power())

    def to_numbers(self):
        numerical_representation = [0, 0, 0, 0, 0, 0, self.cost, self.interest_rate]
        if self.owner is not None:
            numerical_representation[self.owner.get_id()] = 1

        return numerical_representation
