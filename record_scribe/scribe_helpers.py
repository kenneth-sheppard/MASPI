country_name_helper = {
    0: 'Russia',
    1: 'China',
    2: 'India',
    3: 'Brazil',
    4: 'America',
    5: 'European Union'
}
rondel_space_dict = {
    0: 'Investor',
    1: 'Import',
    2: 'Production1',
    3: 'Maneuver1',
    4: 'Taxation',
    5: 'Factory',
    6: 'Production2',
    7: 'Maneuver2'
}


def player_name_helper(player_set, first_player_id):
    if player_set[first_player_id] == '1':
        return 'Player 1'
    elif player_set[(first_player_id + 1) % 6] == '1':
        return 'Player 2'
    elif player_set[(first_player_id + 2) % 6] == '1':
        return 'Player 3'
    elif player_set[(first_player_id + 3) % 6] == '1':
        return 'Player 4'
    elif player_set[(first_player_id + 4) % 6] == '1':
        return 'Player 5'
    elif player_set[(first_player_id + 5) % 6] == '1':
        return 'Player 6'
    elif len(player_set) == 6:
        return 'No Player'
    else:
        raise RuntimeError('Incorrect player list passed to player name helper')


def rondel_space_helper(rondel_set):
    if rondel_set[0] == '1':
        return 'Investor'
    elif rondel_set[1] == '1':
        return 'Import'
    elif rondel_set[2] == '1':
        return 'Production1'
    elif rondel_set[3] == '1':
        return 'Maneuver1'
    elif rondel_set[4] == '1':
        return 'Taxation'
    elif rondel_set[5] == '1':
        return 'Factory'
    elif rondel_set[6] == '1':
        return 'Production2'
    elif rondel_set[7] == '1':
        return 'Maneuver2'
    elif len(rondel_set) == 8:
        return 'Not Placed'
    else:
        raise RuntimeError('Incorrect rondel list passed to rondel space helper')


def territory_helper(territory_set):
    flag_present = 'None'
    pieces_present = {}

    if territory_set[0] == '1':
        flag_present = country_name_helper[0]
    elif territory_set[1] == '1':
        flag_present = country_name_helper[1]
    elif territory_set[2] == '1':
        flag_present = country_name_helper[2]
    elif territory_set[3] == '1':
        flag_present = country_name_helper[3]
    elif territory_set[4] == '1':
        flag_present = country_name_helper[4]
    elif territory_set[5] == '1':
        flag_present = country_name_helper[5]

    for j in range(6):
        if int(territory_set[6 + j]) > 0:
            pieces_present[country_name_helper[j]] = int(territory_set[6 + j])

    return flag_present, pieces_present
