

class Territory:
    def __init__(self, name, t_id):
        self.name = name
        self.id = t_id
        self.controller = None
        self.factory = False
        self.num_tanks = 0
        self.num_ship = 0
