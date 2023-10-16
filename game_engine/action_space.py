from game_engine.helper import list_of_sea_factories
from game_engine.helper import list_of_land_factories
from game_engine.helper import tax_chart
from game_engine.helper import territory_adjacency_matrix


class ActionSpace:
    def __init__(self):
        self.name = None
        self.next_action = None
        self.times_activated = 0

    def get_name(self):
        """
        Action spaces are named, the names match the names on the board
        Names are used as identifiers
        :return: String the name of the space
        """
        return self.name

    def get_next_action(self):
        """
        Actions spaces have a logical follower, all of them are linked up during setup
        :return: ActionSpace, the next one in logical order
        """
        return self.next_action

    def set_next_action(self, na):
        """
        Sets the next action that logically follows this one
        :param na: ActionSpace, the next action
        """
        self.next_action = na

    def action(self, country, player, game_state):
        """
        Performs the action associated with this space
        May query the player to make decisions passing the game_state and a list of all possible future game_states
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        """
        self.times_activated += 1

    def get_times_activated(self):
        """
        Used for gathering statistics, allows the retrieval of the amount of times this space has been activated
        :return: int - count of times the space has been activated
        """
        return self.times_activated


class Investor(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Investor'
        self.players = None

    def action(self, country, player, game_state):
        """
        Investor does three things
        1. Pay out from country treasury to bond-holders
        2. Give 2M to the holder of the investor card, let them invest
        3. Ask any swiss banks to invest
        HOWEVER
        In this implementation the investor card handles parts 2 and 3 as such the below action is only responsible
        for paying out appropriately
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return: 0 - that's it, no return really needed, could be used for status codes eventually
        """
        super(Investor, self).action(country, player, game_state)
        self.players = game_state.get_players()
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
                    if country.get_country_controller() is not next_up[0]:
                        # get amount available
                        aa = country.get_country_controller().get_money()
                        if next_up[1] < aa:
                            next_up[0].add_money(next_up[1])
                            country.get_country_controller().remove_money(next_up[1])
                        else:
                            next_up[0].add_money(aa)
                            country.get_country_controller().remove_money(aa)
                # Country is broke, player must pay
                else:
                    if country.get_country_controller() is not next_up[0]:
                        aa = country.get_country_controller().get_money()
                        if next_up[1] < aa:
                            next_up[0].add_money(next_up[1])
                            country.get_country_controller().remove_money(next_up[1])
                        else:
                            next_up[0].add_money(aa)
                            country.get_country_controller().remove_money(aa)

            del owed[next_up[0]]

        return 0


def hypothetical_investment(choice, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param choice: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    if choice[1] is not None:
        if choice[2] is not None:
            game_state.get_player(choice[3]).buy_bond(game_state.get_bond(choice[1]), game_state.get_bond(choice[2]))
        else:
            game_state.get_player(choice[3]).buy_bond(game_state.get_bond(choice[1]))
    return game_state


def reverse_investment(choice, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param choice: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    if choice[1] is not None:
        if choice[2] is not None:
            game_state.get_player(choice[3]).sell_bond(game_state.get_bond(choice[1]), game_state.get_bond(choice[2]))
        else:
            game_state.get_player(choice[3]).sell_bond(game_state.get_bond(choice[1]))
    return game_state


class Import(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Import'

    def action(self, country, player, game_state):
        """

        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return:
        """
        super(Import, self).action(country, player, game_state)
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
                        possibilities.append((c, territory, country))

        if len(possibilities) > 0:
            # Query the player as to what the player would like to choose
            choice = player.make_import_choice(possibilities, game_state)

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


def hypothetical_import(choice, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param choice: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    country = game_state.get_country(choice[2].get_name())
    territory = game_state.get_territory(choice[1].get_id())

    for k in range(0, choice[0].get('Tanks')):
        country.remove_tank_from_pool()
        territory.add_tank(country.get_name())
        country.remove_money(1)

    for m in range(0, choice[0].get('Ships')):
        country.remove_ship_from_pool()
        territory.add_ship(country.get_name())
        country.remove_money(1)

    return game_state


def reverse_import(choice, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param choice: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    country = game_state.get_country(choice[2].get_name())
    territory = game_state.get_territory(choice[1].get_id())

    for k in range(0, choice[0].get('Tanks')):
        country.add_tank_to_pool()
        territory.remove_tank(country.get_name())
        country.add_money(1)

    for m in range(0, choice[0].get('Ships')):
        country.add_ship_to_pool()
        territory.remove_ship(country.get_name())
        country.add_money(1)

    return game_state


class Production(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Production'

    def action(self, country, player, game_state):
        """

        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return:
        """
        super(Production, self).action(country, player, game_state)
        # Might want a helper action for adding pieces to a territory that can automatically resolve conflicts
        # Will eventually need a priority system in case not enough pieces probably
        for territory in country.get_home_territories():
            if territory.get_territory_controller() is country.get_name() or territory.get_territory_controller() is None:
                if territory.has_factory():
                    if territory.get_name() in list_of_land_factories:
                        if country.remove_tank_from_pool():
                            territory.set_num_tanks(country.get_name(), territory.get_num_tanks(country.get_name()) + 1)
                    elif territory.get_name() in list_of_sea_factories:
                        if country.remove_ship_from_pool():
                            territory.set_num_ships(country.get_name(), territory.get_num_ships(country.get_name()) + 1)
            else:
                return 1


class Maneuver(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Maneuver'

    def action(self, country, player, game_state):
        """

        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        """
        super(Maneuver, self).action(country, player, game_state)
        # Step 1 is to move all ships
        self.__move_ships(country, player, game_state)

        # Step 2 do the same for tanks
        self.__move_tanks(country, player, game_state)

    def battle(self, country, player, game_state, territory, unit_type):
        """
        Battle resolves two different countries controlling pieces in the same territory
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :param territory: Territory - the territory that the battle is occurring in
        :param unit_type: String - either 'ship' or 'tank'
        :return: int - 0
        """
        no_peace = True
        while len(get_present(territory, unit_type)) >= 2 and no_peace and country.get_name() in get_present(territory, unit_type):
            present = get_present(territory, unit_type)
            present.append(None)
            options = []
            for i in present:
                if i != country.get_name():
                    options.append((country, i, territory, unit_type))
            to_fight = player.make_battle_choice(options, game_state)
            if to_fight[1] is not None:
                do_battle(to_fight, game_state)
            else:
                no_peace = False
                for country_name in present:
                    if country_name is not None:
                        if game_state.get_country(country_name).get_country_controller() is not None and \
                                game_state.get_country(country_name) is not country:
                            to_fight = game_state.get_country(country_name).get_country_controller().make_battle_choice(
                                [(country, country_name, territory, unit_type),
                                 (country, None, territory, unit_type)], game_state)
                            if to_fight[1] is not None:
                                no_peace = True
                                do_battle(to_fight, game_state)
                                break
                            else:
                                no_peace = no_peace or False

        # If there is only one army in the region, do nothing
        # If there are more than one then
        # Ask the active player if they want to fight any players represented as (Country1, Country2)
        # If yes resolve the fight

        return 0

    def __move_ships(self, country, player, game_state):
        """
        Two steps here
        1. Build up a set of all possible moves
        2. After querying the player for what move, execute the move on the active game state
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        """
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
                if multiple_ships_handler[ship_territory] > 0:
                    # Legal territories are adjacent to the current one (the current one is also classified as adjacent
                    # And must be water or the port that the ship is currently in
                    adjacent_territories = [t for t in game_state.get_territories().values() if
                                            territory_adjacency_matrix[ship_territory.get_id()][t.get_id()] == 1
                                            and (t.get_is_water() or t == ship_territory)]

                    for adjacent_ship_territory in adjacent_territories:
                        legal_moves.append(('Ship', ship_territory, adjacent_ship_territory, country, player))
            # Get the decision from the player
            choice = player.make_maneuver_choice(options=legal_moves, game_state=game_state)

            # Execute the move
            self.__move_piece(choice, country, player, game_state)

            # Remove that ship from the list of territories that have ships of the active country
            multiple_ships_handler[choice[1]] = multiple_ships_handler[choice[1]] - 1
            # If a new unit moving into a peaceful territory causes combat to occur that removes the piece already
            # in the territory, the old piece cannot be moved and should not be a part of msh anymore
            for key in multiple_ships_handler.keys():
                if key.get_num_ships(country.get_name()) < multiple_ships_handler[key]:
                    num_ships_to_move -= multiple_ships_handler[key] - key.get_num_ships(country.get_name())
                    multiple_ships_handler[key] = key.get_num_ships(country.get_name())
                if multiple_ships_handler[key] == 0 and key in active_ship_territories:
                    active_ship_territories.remove(key)

            num_ships_to_move -= 1

    def __move_tanks(self, country, player, game_state):
        """
        Two steps here
        1. Build up a set of all possible moves
        2. After querying the player for what move, execute the move on the active game state
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        """
        num_tanks_to_move = 0
        # Create a list of all territories that have tanks of the active country
        active_tank_territories = [i for i in game_state.get_territories().values() if
                                   i.get_tanks().get(country.get_name()) > 0]

        multiple_tanks_handler = {}

        for ast in active_tank_territories:
            multiple_tanks_handler[ast] = ast.get_num_tanks(country_name=country.get_name())
            num_tanks_to_move += ast.get_num_tanks(country_name=country.get_name())

        # Handle convoying
        active_ship_territories = [i for i in game_state.get_territories().values() if
                                   i.get_ships().get(country.get_name()) > 0]

        convoy_ships = []

        for territory in active_ship_territories:
            for i in range(0, territory.get_num_ships(country.get_name())):
                convoy_ships.append(territory)

        while num_tanks_to_move > 0:

            # Create a list of all legal moves for each of those tanks
            legal_moves = []

            destinations = []

            for tank_territory in active_tank_territories:
                # Skip territories whose tanks have all been moved
                if multiple_tanks_handler[tank_territory] > 0:
                    # Legal territories are adjacent to the current one
                    adjacent_territories = [t for t in game_state.get_territories().values() if
                                            territory_adjacency_matrix[tank_territory.get_id()][t.get_id()] == 1]

                    # Need to search for territories that are legal through convoy
                    temp = []

                    for territory in adjacent_territories:
                        if territory.get_in_country() == country:
                            w = self.__find_railroad(country, territory, game_state, active_ship_territories, [tank_territory])
                        else:
                            w = None
                        if w is not None:
                            if type(w) is list:
                                for elem in w:
                                    temp.append(elem)
                            else:
                                temp.append(w)

                        q = self.__find_convoy(country, territory, game_state, active_ship_territories)
                        if q is not None:
                            if type(q) is list:
                                for elem in q:
                                    temp.append(elem)
                            else:
                                temp.append(q)

                    adjacent_territories = temp

                    for adjacent_tank_territory in adjacent_territories:
                        if ('Tank', tank_territory, adjacent_tank_territory) not in legal_moves:
                            if type(adjacent_tank_territory) is list:
                                if adjacent_tank_territory[0] in destinations:
                                    continue
                                else:
                                    destinations.append(adjacent_tank_territory[0])
                            else:
                                destinations.append(adjacent_tank_territory)
                            legal_moves.append(('Tank', tank_territory, adjacent_tank_territory, country, player))
            # Get the decision from the player
            choice = player.make_maneuver_choice(options=legal_moves, game_state=game_state)

            choice_to_pass = choice

            if type(choice[2]) is list:
                for t in choice[2]:
                    if t in convoy_ships:
                        convoy_ships.remove(t)

                choice_to_pass = (choice[0], choice[1], choice[2][0])

            # Execute the move
            self.__move_piece(choice_to_pass, country, player, game_state)

            # Remove that tank from the list of territories that have tanks of the active country
            multiple_tanks_handler[choice[1]] = multiple_tanks_handler[choice[1]] - 1

            for key in multiple_tanks_handler.keys():
                if key.get_num_tanks(country.get_name()) < multiple_tanks_handler[key]:
                    num_tanks_to_move -= multiple_tanks_handler[key] - key.get_num_tanks(country.get_name())
                    multiple_tanks_handler[key] = key.get_num_tanks(country.get_name())
                if multiple_tanks_handler[key] == 0 and key in active_tank_territories:
                    active_tank_territories.remove(key)

            num_tanks_to_move -= 1

    def __find_convoy(self, country, territory, game_state, available_ships):
        """
        A recursive method that will build out chains of moves that represent possible moves from a territory
        :param country: Country - the acting country full object
        :param territory: Territory - the current territory
        :param game_state: GameState - the full game state object
        :param available_ships: int - a count of ships that have not been used in a convoy
        :return: List - a set of possible convoys
        """
        if not territory.get_is_water():
            return [territory]

        elif territory.get_num_ships(country_name=country.get_name()) == 0 or territory not in available_ships:
            return

        else:
            possible_convoys = []
            available_ships.remove(territory)
            for adjacent_territory in game_state.get_territories().values():
                if territory_adjacency_matrix[territory.get_id()][adjacent_territory.get_id()] == 1 and \
                        territory.get_id() != adjacent_territory.get_id():
                    res = self.__find_convoy(country, adjacent_territory, game_state, available_ships)
                    if res is not None:
                        for path in res:
                            if type(path) is list:
                                path.append(territory)
                                possible_convoys.append(path)
                            else:
                                res.append(territory)
                                possible_convoys.append(res)
                                break
            available_ships.append(territory)
            return possible_convoys

    def __find_railroad(self, country, territory, game_state, available_ships, visited_territories):
        """
        A recursive method that will build out chains of moves that represent possible moves from a territory
        :param country: Country - the acting country full object
        :param territory: Territory - the current territory
        :param game_state: GameState - the full game state object
        :param available_ships: int - a count of ships that have not been used in a convoy
        :param visited_territories: List - a set of territories that have already been checked, helps avoid recursive loops
        :return: List - a set of possible convoys
        """
        if territory.is_occupied() or territory in visited_territories:
            return None
        elif len(visited_territories) > 0 and visited_territories[0].get_in_country() != country:
            return None
        elif not territory.get_in_country() == country and not territory.get_is_water():
            return [territory]
        elif not territory.get_in_country() == country and territory.get_is_water():
            return self.__find_convoy(country, territory, game_state, available_ships)
        else:
            possible_railways = []
            visited_territories.append(territory)
            for adjacent_territory in game_state.get_territories().values():
                if territory_adjacency_matrix[territory.get_id()][adjacent_territory.get_id()] == 1 and \
                        territory.get_id() != adjacent_territory.get_id():
                    res = self.__find_railroad(country, adjacent_territory, game_state, available_ships, visited_territories)
                    if res is not None:
                        for path in res:
                            if type(path) is list:
                                path.append(territory)
                                possible_railways.append(path)
                            else:
                                res.append(territory)
                                possible_railways.append(res)
                                break

            return possible_railways

    def __move_piece(self, command, country, player, game_state):
        """
        Helper method that executes a move using a command tuple
        :param command: Tuple - ('Type of Unit', Territory_Moving_From, Territory_Moving_To)
        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return: int - 0
        """
        # Format of responses should be ('Type of Unit', Territory_Moving_From, Territory_Moving_To)
        t_from = command[1]
        t_to = command[2]
        if command[0] == 'Ship' and t_from.get_ships().get(country.get_name()) != 0:
            t_from.remove_ship(country.get_name())
            t_to.add_ship(country.get_name())
        elif command[0] == 'Tank' and t_from.get_tanks().get(country.get_name()) != 0:
            t_from.remove_tank(country.get_name())
            t_to.add_tank(country.get_name())
        else:
            if command[1] != command[2]:
                raise ValueError(f'Oops! That\'s not right... -> {command[0]} - {command[1]} - {command[2]}')
        self.battle(country, player, game_state, command[2], command[0])

        return 0


def hypothetical_move_piece(command, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param command: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    # Format of responses should be ('Type of Unit', Territory_Moving_From, Territory_Moving_To)
    t_from = game_state.get_territory(command[1].get_id())
    if type(command[2]) is list:
        t_to = game_state.get_territory(command[2][0].get_id())
    else:
        t_to = game_state.get_territory(command[2].get_id())
    country = game_state.get_country(command[3].get_name())
    player = game_state.get_player(command[4].get_id())
    if command[0] == 'Ship' and t_from.get_ships().get(country.get_name()) != 0:
        t_from.remove_ship(country.get_name())
        t_to.add_ship(country.get_name())
    elif command[0] == 'Tank' and t_from.get_tanks().get(country.get_name()) != 0:
        t_from.remove_tank(country.get_name())
        t_to.add_tank(country.get_name())
    else:
        if command[1] != command[2]:
            raise ValueError(f'Oops! That\'s not right... -> {command[0]} - {command[1]} - {command[2]}')

    return game_state


def reverse_move_piece(command, game_state):
    """
    :param command: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    # Format of responses should be ('Type of Unit', Territory_Moving_From, Territory_Moving_To)
    t_from = game_state.get_territory(command[1].get_id())
    if type(command[2]) is list:
        t_to = game_state.get_territory(command[2][0].get_id())
    else:
        t_to = game_state.get_territory(command[2].get_id())
    country = game_state.get_country(command[3].get_name())
    player = game_state.get_player(command[4].get_id())
    if command[0] == 'Ship' and t_to.get_ships().get(country.get_name()) != 0:
        t_from.add_ship(country.get_name())
        t_to.remove_ship(country.get_name())
    elif command[0] == 'Tank' and t_to.get_tanks().get(country.get_name()) != 0:
        t_from.add_tank(country.get_name())
        t_to.remove_tank(country.get_name())
    else:
        if command[1] != command[2]:
            raise ValueError(f'Oops! That\'s not right... -> {command[0]} - {command[1]} - {command[2]}')

    return game_state


def get_present(territory, unit_type):
    """
    Helper function that fetches if a piece of a specified type is in the territory.
    :param territory: Territory - The territory to be checked
    :param unit_type: String - The appropriate type of unit ['Ship', 'Tank']
    :return: List - A list of country names that have pieces present
    """
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


def do_battle(choice, game_state):
    """
    Executes a battle
    :param choice: List - [Initiating Country, Defending Country, Territory, Type of Unit]
                          [Country, Country, Territory, String]
    :param game_state: A full GameState object
    :return: GameState - the resultant game state
    """
    if choice[1] is None:
        return game_state
    country = choice[0]
    to_fight = choice[1]
    territory = choice[2]
    unit_type = choice[3]
    if unit_type == 'Ship':
        game_state.get_territory(territory.get_id()).remove_ship(country.get_name())
        game_state.get_territory(territory.get_id()).remove_ship(to_fight)
    if unit_type == 'Tank':
        game_state.get_territory(territory.get_id()).remove_tank(country.get_name())
        game_state.get_territory(territory.get_id()).remove_tank(to_fight)

    return game_state


def reverse_battle(choice, game_state):
    """
    Executes a battle
    :param choice: List - [Initiating Country, Defending Country, Territory, Type of Unit]
                          [Country, Country, Territory, String]
    :param game_state: A full GameState object
    :return: GameState - the resultant game state
    """
    if choice[1] is None:
        return game_state
    country = choice[0]
    to_fight = choice[1]
    territory = choice[2]
    unit_type = choice[3]
    if unit_type == 'Ship':
        game_state.get_territory(territory.get_id()).add_ship(country.get_name())
        game_state.get_territory(territory.get_id()).add_ship(to_fight)
    if unit_type == 'Tank':
        game_state.get_territory(territory.get_id()).add_tank(country.get_name())
        game_state.get_territory(territory.get_id()).add_tank(to_fight)

    return game_state


class Taxation(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Taxation'

    def action(self, country, player, game_state):
        """

        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return:
        """
        super(Taxation, self).action(country, player, game_state)
        amount = 0
        for territory in country.get_home_territories():
            if not territory.is_occupied() and territory.has_factory():
                amount += 2

        amount += len(country.get_controlled_neutral_territories())

        power_up, owner_payout = tax_chart(amount)

        amount -= country.get_placed_units()

        if amount < 0:
            amount = 0

        country.add_power(power_up)
        # Give money to controller
        country.get_country_controller().add_money(owner_payout)

        country.add_money(amount)

        return 0


class Factory(ActionSpace):
    def __init__(self):
        super().__init__()
        self.name = 'Factory'

    def action(self, country, player, game_state):
        """

        :param country: Country - the acting country full object
        :param player: Player - should be the whole player object ----- @TODO - check this
        :param game_state: GameState - the current game_state class, full object
        :return:
        """
        super(Factory, self).action(country, player, game_state)
        if len([i for i in country.get_home_territories() if not i.has_factory()]) == 0:
            return

        options = []
        if country.get_treasury() >= 5:
            for territory in country.get_home_territories():
                if not territory.has_factory():
                    options.append((territory, country))

            choice = player.make_factory_choice(options, game_state)
            # Might need a check in case the territory is occupied by hostiles
            choice[1].remove_money(5)
            choice[0].build_factory()
            if choice[0] in list_of_land_factories:
                choice[1].remove_tank_factory_from_supply()
            elif choice[0] in list_of_sea_factories:
                choice[1].remove_ship_factory_from_supply()

        return 0

    # def reverse_action(self, country, player, game_state):
    #     country = game_state.get_country(choice[1].get_name())
    #     territory = game_state.get_territory(choice[0].get_id())
    #     country.add_money(5)
    #     territory.remove_factory()
    #     if territory in list_of_land_factories:
    #         country.add_tank_factory_to_supply()
    #     elif territory in list_of_sea_factories:
    #         country.add_ship_factory_to_supply()
    #
    #     return game_state


def hypothetical_factory(choice, game_state):
    """
    This was how I wound up managing trying to look forward and get all potential moves
    Allows users to perform an action on a copied game_state to explore more possibilities
    :param choice: Tuple - A choice tuple, exactly like the one used by the investor card ---- @TODO get example of this
    :param game_state: GameState - A deep copy of a game state
    :return: GameState - The game state with the choice performed
    """
    # Might need a check in case the territory is occupied by hostiles
    country = game_state.get_country(choice[1].get_name())
    territory = game_state.get_territory(choice[0].get_id())
    country.remove_money(5)
    territory.build_factory()
    if territory in list_of_land_factories:
        country.remove_tank_factory_from_supply()
    elif territory in list_of_sea_factories:
        country.remove_ship_factory_from_supply()

    return game_state


def reverse_factory(choice, game_state):
    country = game_state.get_country(choice[1].get_name())
    territory = game_state.get_territory(choice[0].get_id())
    country.add_money(5)
    territory.destroy_factory()
    if territory in list_of_land_factories:
        country.add_tank_factory_to_supply()
    elif territory in list_of_sea_factories:
        country.add_ship_factory_to_supply()

    return game_state
