from game_engine.helper import list_of_sea_factories
from game_engine.helper import list_of_land_factories
from game_engine.helper import tax_chart
from game_engine.helper import territory_adjacency_matrix
from game_engine.helper import get_territory_id_from_name


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

    def action(self, country, player, game_state):
        pass


class Investor(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Investor'
        self.players = None

    def action(self, country, player, game_state):
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

        return 0


class Import(ActionSpace):
    def __init__(self):
        super().__init__()
        pass

    def action(self, country, player, game_state):
        # How many units can they get
        max_units_to_get = min(3, country.get_treasury())
        # Check which unit combinations are legal
        boat_territories = [i for i in country.get_home_territories() if not i.is_occupied() and i.get_factory_is_sea()]
        tank_territories = [i for i in country.get_home_territories() if not i.is_occupied()]
        unit_combinations = []
        for i in range(0, max_units_to_get + 1):
            for j in range(max_units_to_get - i, -1, -1):
                unit_combinations.append({'Tanks': i, 'Ships': j})

        possibilities = []
        # All units to one location
        for c in unit_combinations:
            for territory in country.get_home_territories():
                if not territory.is_occupied():
                    if c.get('Ships') == 0 or territory.get_factory_is_sea():
                        possibilities.append((c, territory))

        # Query the player as to what the player would like to choose
        choice = player.make_choice(possibilities, game_state)

        # Execute choice
        for k in range(0, choice[0].get('Tanks')):
            country.remove_tank_from_pool()
            choice[1].add_tank(country.get_name())
            country.remove_money(1)

        for m in range(0, choice[0].get('Ships')):
            country.remove_ship_from_pool()
            choice[1].add_ship(country.get_name())
            country.remove_money(1)

        return 0


class Production(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Production'

    def action(self, country, player, game_state):
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
        self.name = 'Maneuver'

    def action(self, country, player, game_state):
        # Step 1 is to move all ships
        self.__move_ships(country, player, game_state)

        # Step 2 do the same for tanks
        self.__move_tanks(country, player, game_state)

    def battle(self, country, player, game_state, territory, unit_type):
        present = get_present(territory, unit_type)
        no_peace = True
        while len(present) >= 2 and no_peace:
            present.append(None)
            to_fight = player.make_choice([i for i in present if not country.get_name()], game_state)
            if to_fight is not None:
                do_battle(country, to_fight, territory, unit_type)
                present = get_present(territory, unit_type)
            else:
                no_peace = False
                for country_name in present:
                    if game_state.get_country(country_name).get_controller() is not None and \
                            game_state.get_country(country_name) is not country:
                        to_fight = game_state.get_country(country_name).get_controller().make_choice([country.get_name()
                                                                                                         , None],
                                                                                                     game_state)
                        if to_fight is not None:
                            no_peace = True
                            do_battle(country, to_fight, territory, unit_type)
                            present = get_present(territory, unit_type)
                        else:
                            no_peace = no_peace or False

        # If there is only one army in the region, do nothing
        # If there are more than one then
        # Ask the active player if they want to fight any players represented as (Country1, Country2)
        # If yes resolve the fight

        return 0

    def __move_ships(self, country, player, game_state):
        num_ships_to_move = 0
        # Create a list of all territories that have ships of the active country
        active_ship_territories = [i for i in game_state.get_territories().values() if
                                   i.get_ships().get(country.get_name()) > 0]

        multiple_ships_handler = {}

        for ast in active_ship_territories:
            multiple_ships_handler[ast] = ast.get_num_ships(country_name=country.get_name())
            num_ships_to_move += ast.get_num_ships(country_name=country.get_name())

        while num_ships_to_move > 0:

            # Create a list of all legal moves for each of those ships
            legal_moves = []

            for ship_territory in active_ship_territories:
                # Skip territories whose ships have all been moved
                if multiple_ships_handler[ship_territory] >= 0:
                    # Legal territories are adjacent to the current one (the current one is also classified as adjacent
                    # And must be water or the port that the ship is currently in
                    adjacent_territories = [t for t in game_state.get_territories().values() if
                                            territory_adjacency_matrix[ship_territory.get_id()][t.get_id()] == 1
                                            and (t.get_is_water() or t == ship_territory)]

                    for adjacent_ship_territory in adjacent_territories:
                        legal_moves.append(('Ship', ship_territory, adjacent_ship_territory))
                    # Get the decision from the player
                    choice = player.make_maneuver_choice(options=legal_moves, game_state=game_state)

                    # Execute the move
                    self.__move_piece(choice, country, player, game_state)

                    # Remove that ship from the list of territories that have ships of the active country
                    multiple_ships_handler[choice[1]] = multiple_ships_handler[choice[1]] - 1
                    num_ships_to_move -= 1

    def __move_tanks(self, country, player, game_state):
        num_tanks_to_move = 0
        # Create a list of all territories that have ships of the active country
        active_tank_territories = [i for i in game_state.get_territories().values() if
                                   i.get_tanks().get(country.get_name()) > 0]

        multiple_tanks_handler = {}

        for ast in active_tank_territories:
            multiple_tanks_handler[ast] = ast.get_num_tanks(country_name=country.get_name())
            num_tanks_to_move += ast.get_num_tanks(country_name=country.get_name())

        while num_tanks_to_move > 0:

            # Create a list of all legal moves for each of those ships
            legal_moves = []

            for tank_territory in active_tank_territories:
                # Skip territories whose ships have all been moved
                if multiple_tanks_handler[tank_territory] >= 0:
                    # Legal territories are adjacent to the current one
                    adjacent_territories = [t for t in game_state.get_territories().values() if
                                            territory_adjacency_matrix[tank_territory.get_id()][t.get_id()] == 1]

                    # Need to search for territories that are legal through convoy
                    temp = []

                    for territory in adjacent_territories:
                        q = self.__find_convoy(country, territory, game_state)
                        if q is not None:
                            if q is list:
                                for elem in q:
                                    temp.append(elem)
                            else:
                                temp.append(q)

                    adjacent_territories = temp

                    for adjacent_tank_territory in adjacent_territories:
                        legal_moves.append(('Tank', tank_territory, adjacent_tank_territory))
                    # Get the decision from the player
                    choice = player.make_maneuver_choice(options=legal_moves, game_state=game_state)

                    # Execute the move
                    self.__move_piece(choice, country, player, game_state)

                    # Remove that ship from the list of territories that have ships of the active country
                    multiple_tanks_handler[choice[1]] = multiple_tanks_handler[choice[1]] - 1
                    num_tanks_to_move -= 1

    def __find_convoy(self, country, territory, game_state):
        if not territory.get_is_water():
            return territory

        elif territory.get_num_ships(country_name=country.get_name()) == 0:
            return

        else:
            possible_convoys = []
            for adjacent_territory in game_state.get_territories().values():
                if territory_adjacency_matrix[territory.get_id()][adjacent_territory.get_id()] == 1 and \
                        territory.get_id() != adjacent_territory.get_id():
                    res = self.__find_convoy(country, adjacent_territory, game_state)
                    if res is not None:
                        possible_convoys.append(self.__find_convoy(country, adjacent_territory, game_state))

            return possible_convoys

    def __move_piece(self, command, country, player, game_state):
        # Format of responses should be ('Type of Unit', Territory_Moving_From, Territory_Moving_To)
        t_from = command[1]
        t_to = command[2]
        if command[0] == 'Ship' and t_from.get_ships().get(country.get_name()) != 0:
            t_from.remove_ship(country.get_name())
            t_to.add_ship(country.get_name())
        if command[0] == 'Tank' and t_from.get_ships().get(country.get_name()) != 0:
            t_from.remove_ship(country.get_name())
            t_to.add_ship(country.get_name())
        self.battle(country, player, game_state, command[2], command[0])

        return 0


def get_present(territory, unit_type):
    present = []
    if unit_type == 'Ship':
        for country_name, piece_count in territory.get_ships().items():
            if piece_count > 0:
                present.append(country_name)
    if unit_type == 'Tank':
        for country_name, piece_count in territory.get_tanks().items():
            if piece_count > 0:
                present.append(country_name)

    return present


def do_battle(country, to_fight, territory, unit_type):
    if unit_type == 'Ship':
        territory.remove_ship(country.get_name())
        territory.remove_ship(to_fight)
    if unit_type == 'Tank':
        territory.remove_tank(country.get_name())
        territory.remove_tank(to_fight)


class Taxation(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Taxation'

    def action(self, country, player, game_state):
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

    def action(self, country, player, game_state):
        territory = player.make_choice(game_state)
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
