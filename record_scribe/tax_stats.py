class TaxStats:

    def __init__(self):
        self.players = {}
        self.games = []

    def add_information(self, sample):
        if sample[0] in self.players.keys():
            self.players[sample[0]] += sample[1]
        else:
            self.players[sample[0]] = sample[1]

    def take_current_and_previous_turn_tax_power(self, previous_turn, current_turn):
        for country in current_turn['Countries'].keys():
            if current_turn['Countries'][country]['Rondel Space'] == 'Taxation':
                if int(previous_turn['Countries'][country]['Power']) != int(current_turn['Countries'][country]['Power']):
                    controller = current_turn['Countries'][country]['Controller']
                    pre_tax_power = int(previous_turn['Players'][controller][0])
                    pre_tax_controller = previous_turn['Countries'][country]['Controller']
                    # Save the increase in power and the player responsible
                    post_tax_power = int(current_turn['Players'][controller][0])
                    self.add_information((pre_tax_controller, post_tax_power - pre_tax_power))

    def take_current_and_previous_turn_tax_income(self, previous_turn, current_turn, country):
        controller = current_turn['Countries'][country]['Controller']
        if current_turn['Countries'][country]['Rondel Space'] == 'Taxation':
            if int(previous_turn['Players'][controller][0]) != int(current_turn['Players'][controller][0]):
                pre_tax_money = int(previous_turn['Players'][controller][0])
                # Save the increase in power and the player responsible
                post_tax_money = int(current_turn['Players'][controller][0])
                self.add_information((controller, post_tax_money - pre_tax_money))

    def take_current_and_previous_turn_investor(self, previous_turn, current_turn):
        for player in current_turn['Players'].keys():
            if int(previous_turn['Players'][player][0]) < int(current_turn['Players'][player][0]):
                pre_inv_cash = int(previous_turn['Players'][player][0])
                # Save the increase in power and the player responsible
                post_inv_cash = int(current_turn['Players'][player][0])
                self.add_information((player, post_inv_cash - pre_inv_cash))

    def get_information(self):
        return self.games

    def finalize_game(self):
        self.games.append(self.players)

        self.players = {}
