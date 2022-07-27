

class Tank:
    def __init__(self):
        self.owner = None
        self.territory = None

    def get_owner(self):
        return self.owner

    def get_territory(self):
        return self.territory

    def set_territory(self, t):
        self.territory = t
