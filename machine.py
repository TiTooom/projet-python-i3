
class Machine:
    def __init__(self):
        pass

    def init(self, name, type, speed, cycle_time, state):
        self.name = name #nom de la machine
        self.type = type #type de la machine
        self.speed = speed #vitesse de la machine
        self.cycle_time = cycle_time #temps de cycle de la machine
        self.state = state #état de la machine
