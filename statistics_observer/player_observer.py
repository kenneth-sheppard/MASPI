import random


class PlayerObserver:
    
    def __init__(self, p):
        self.player = p
        self.player_info = {
            'bonds': p.get_bonds(),
            'money': p.get_worth(),
            'controlled_countries': p.get_controlled_countries(),
            'type': p.get_type(),
        }
        self.scores = []
        self.wins = 0
        self.game_log = []
        self.bond_set = []
        self.id = random.randint(0, 5000)

    def __str__(self):
        result = f'Player {self.id} {self.player_info["type"]} won {self.wins} games with scores of ' \
               f'{self.scores} and bonds:\n'
        for elem in self.bond_set:
            line = ''
            for bond in elem:
                line += str(bond) + ', '
            result += line + '\n'
        return result
        
    def observe(self):
        self.player_info['bonds'] = self.player.get_bonds()
        self.player_info['money'] = self.player.get_worth()
        self.player_info['controlled_countries'] = self.player.get_controlled_countries()
        
    def was_winner(self):
        self.wins += 1

    def game_end(self):
        self.scores.append(self.player.get_worth())
        self.game_log.append(self.player_info)
        self.bond_set.append(self.player.get_bonds())

    def update_player(self, p):
        self.player = p
        self.player_info['type'] = p.get_type()

    def get_player(self):
        return self.player

    def get_player_info(self):
        return self.player_info

    def get_wins(self):
        return self.wins

    def get_score(self, index):
        return self.scores[index]

    def get_game_log(self):
        return self.game_log
