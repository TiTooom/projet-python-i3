class Machine:
    def __init__(self, name, type, speed, cycle_time, state):
        self.name = name #nom de la machine -> PM1, PM2, PM3
        self.type = type #type de la machine -> découpe, fonderie, assemblage
        self.speed = speed #vitesse de la machine -> pourcentage de la vitesse de production
        self.cycle_time = cycle_time #temps de cycle de la machine -> temps pour produire une pièce en seconde
        self.state = state #état de la machine -> running, stopped, maintenance

    

