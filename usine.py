import tkinter as tk
from machine import Machine
from materiaux import Material
from materiaux import Recipes
from materiaux import Gestion

# Création de l'usine
class Factory:
    def __init__(self,name, localization, capacity):
        self.nom = name #nom de l'usine
        self.localization = localization #localisation de l'usine
        self.capacity = capacity #capacité de stockage de l'usine
        self.machines = [] #liste des machines de l'usine




if __name__ == '__main__':

    print("Début de la simulation")   

    # Création de l'usine 
    USINE = Factory("Mettalurgic", "France", 1972000)

    # Création de machines 
    MACHINE = Machine()
    machine1 = MACHINE.init("PM1", "Découpe", 10, 10, "running")
    machine2 = MACHINE.init("PM2", "Fonderie", 15, 10, "running")
    machine3 = MACHINE.init("PM3", "Assemblage", 20, 10, "running")

    # Ajout des machines à l'usine
    USINE.machines.append(machine1)
    USINE.machines.append(machine2)
    USINE.machines.append(machine3)

    # Affichage des informations de l'usine
    print("Nom de l'usine : ", USINE.nom)
    print("Localisation de l'usine : ", USINE.localization)
    print("Capacité de l'usine : ", USINE.capacity)
    print("Liste des machines de l'usine : ")
    for i in range(len(USINE.machines)):
        print(USINE.machines[i].name, " : ", USINE.machines[i].type, " : ", USINE.machines[i].speed, " : ", USINE.machines[i].cycle_time, " : ", USINE.machines[i].state)
    
    # Afficher les materiaux
    GESTION = Gestion()
    GESTION.display_materials()
    GESTION.display_recipes() 
    
    # Vérification de la disponibilité des matériaux
    print("Exemple de la disponibilité du fer")
    GESTION.available_material("Iron")

    # Lancement en prodction d'une recette
    print("Exemple de production de vis")
    GESTION.start_production("Screw")