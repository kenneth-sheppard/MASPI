

class Player:
    def __init__(self):
        self.bonds = []
        self.controlled_countries = []
        self.money = 0
        self.has_investor_card = False
        self.is_swiss_bank = False

    def get_bonds(self):
        return self.bonds

    def add_bond(self, bond):
        self.bonds.append(bond)

    def swap_bonds(self, bond_in, bond_out):
        self.bonds.remove(bond_out)
        self.bonds.append(bond_in)

    def get_controlled_countries(self):
        return self.controlled_countries

    def add_controlled_country(self, country):
        self.controlled_countries.append(country)

    def remove_controlled_country(self, country):
        self.controlled_countries.remove(country)

    def get_money(self):
        return self.money

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        self.money -= amount

    def get_has_investor_card(self):
        return self.has_investor_card

    def set_has_investor_card(self, has_card):
        self.has_investor_card = has_card

    def get_is_swiss_bank(self):
        return self.is_swiss_bank

    def set_is_swiss_bank(self, is_swiss):
        self.is_swiss_bank = is_swiss

    def to_numbers(self):
        return []