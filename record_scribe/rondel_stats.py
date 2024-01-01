class RondelStats:
    def __init__(self):
        self.players = {}
        self.countries = {}
        self.games = []
        self.turns_by_player = {}

    # country, countries[country]['Rondel Space'], countries[country]['Controller']
    def process_change(self, change, turn_int_div_six):
        # if change[2] in self.players.keys():
        #     if change[1] in self.players[change[2]]:
        #         self.players[change[2]][change[1]] = self.players[change[2]][change[1]] + 1
        #     else:
        #         self.players[change[2]][change[1]] = 1
        # else:
        #     self.players[change[2]] = {change[1]: 1}
        #
        # if change[0] in self.countries.keys():
        #     if change[1] in self.countries[change[0]]:
        #         self.countries[change[0]][change[1]] = self.countries[change[0]][change[1]] + 1
        #     else:
        #         self.countries[change[0]][change[1]] = 1
        # else:
        #     self.countries[change[0]] = {change[1]: 1}

        if change[2] in self.turns_by_player.keys():
            if turn_int_div_six in self.turns_by_player[change[2]].keys():
                if change[1] in self.turns_by_player[change[2]][turn_int_div_six].keys():
                    self.turns_by_player[change[2]][turn_int_div_six][change[1]] = (
                            self.turns_by_player[change[2]][turn_int_div_six][change[1]] + 1)
                else:
                    self.turns_by_player[change[2]][turn_int_div_six][change[1]] = 1
            else:
                self.turns_by_player[change[2]][turn_int_div_six] = {change[1]: 1}
        else:
            self.turns_by_player[change[2]] = {turn_int_div_six: {change[1]: 1}}

    def take_current_and_previous_turn(self, previous_turn, current_turn):
        if previous_turn == {}:
            self.process_change(
                change=(
                    'Russia',
                    current_turn['Countries']['Russia']['Rondel Space'],
                    current_turn['Countries']['Russia']['Controller']
                ),
                turn_int_div_six=current_turn['Turn Counter'] // 6
            )
        else:
            for country in current_turn['Countries'].keys():
                if current_turn['Countries'][country]['Rondel Space'] != previous_turn['Countries'][country]['Rondel Space']:
                    self.process_change(
                        change=(
                            country,
                            current_turn['Countries'][country]['Rondel Space'],
                            current_turn['Countries'][country]['Controller']
                        ),
                        turn_int_div_six=current_turn['Turn Counter'] // 6
                    )

    def finalize_game(self):
        # Store the record in the list of games as a set
        self.games.append((self.players, self.countries))

        # Reset the trackers
        self.players = {}
        self.countries = {}

    def get_games(self):
        return self.games

    def get_turns_by_players(self):
        return self.turns_by_player
