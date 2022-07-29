from game_engine.bond import Bond


def make_bonds_for(country):
    #  2 million
    country.add_bond(Bond(country, 2, 1))
    #  4 million
    country.add_bond(Bond(country, 4, 2))
    #  6 million
    country.add_bond(Bond(country, 6, 3))
    #  9 million
    country.add_bond(Bond(country, 9, 4))
    # 12 million
    country.add_bond(Bond(country, 12, 5))
    # 16 million
    country.add_bond(Bond(country, 16, 6))
    # 20 million
    country.add_bond(Bond(country, 20, 7))
    # 25 million
    country.add_bond(Bond(country, 25, 8))
    # 30 million
    country.add_bond(Bond(country, 30, 9))


def tax_chart(tax_amount):
    if tax_amount < 6:
        return 0, 0
    elif tax_amount < 8:
        return 1, 1
    elif tax_amount < 10:
        return 1, 2
    elif tax_amount < 11:
        return 2, 3
    elif tax_amount < 12:
        return 2, 4
    elif tax_amount < 13:
        return 3, 5
    elif tax_amount < 14:
        return 3, 6
    elif tax_amount < 15:
        return 4, 7
    elif tax_amount < 16:
        return 4, 8
    elif tax_amount < 18:
        return 5, 9
    else:
        return 5, 10


def power_chart(power_value):
    return power_value // 5
