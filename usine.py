import tkinter as tk
import threading

from machine import Machine
from materiaux import Material
from materiaux import Recipes
from materiaux import Gestion
from window import App
from commandes import Order

# Choisir si on veut activer les aléas
ALLOW_ALEA = False

'''
Fichier à executer pour lancer la simulation.
'''

# Création de l'usine
class Factory:
    def __init__(self,name, localization, capacity):
        self.nom = name #nom de l'usine
        self.localization = localization #localisation de l'usine
        self.capacity = capacity #capacité de stockage de l'usine
        self.machines = [] #liste des machines de l'usine
        self.alea = [] #liste des aléas de l'usine




if __name__ == '__main__':

    print("\nDébut de la simulation")   

    # Création de l'usine 
    USINE = Factory("ConnectProd Industries", "France", 972000)

    # Création de machines 
    machine1 = Machine("PM1", "Découpe", 95, 0.11, "running")
    machine2 = Machine("PM2", "Fonderie", 95, 0.12, "running")
    machine3 = Machine("PM3", "Assemblage", 95, 0.21, "running")

    # Ajout des machines à l'usine
    USINE.machines.append(machine1)
    USINE.machines.append(machine2)
    USINE.machines.append(machine3)

    # Création des aléas de l'usine
    from alea import Alea
    alea1 = Alea(USINE, "Bourage",USINE.machines[0], "Arret de la machine ", 3, "stopped")
    alea2 = Alea(USINE, "Probleme electrique",USINE.machines[1], "Arret de la machine ", 3, "stopped")
    alea3 = Alea(USINE, "Maintenance",USINE.machines[2], "Arret de la machine ", 3, "maintenance")

    # Ajout des aléas à l'usine
    USINE.alea.append(alea1)
    USINE.alea.append(alea2)
    USINE.alea.append(alea3)


    # Affichage des informations de l'usine
    print("\nNom de l'usine : ", USINE.nom)
    print("Localisation de l'usine : ", USINE.localization)
    print("Capacité de l'usine : ", USINE.capacity)
    print("\nListe des machines de l'usine : ")
    for i in range(len(USINE.machines)):
        print(USINE.machines[i].name, " : ", USINE.machines[i].type, " : ", USINE.machines[i].speed, "% : ", USINE.machines[i].cycle_time, "sec : ", USINE.machines[i].state)
    
    # Afficher les materiaux de l'usine
    GESTION = Gestion(USINE)
    GESTION.display_materials()
    GESTION.display_recipes(True) # True = Affichage des recettes / False = Récuperation des recettes
    
    # Vérification de la disponibilité des matériaux
    print("\nExemple de la disponibilité du fer :")
    GESTION.available_material("Fer")

    # Lancement en prodction d'une recette
    print("\nExemple de production :")
    GESTION.start_production("Couteau", 1, True)
    GESTION.start_production("Fourchette", 1, True)
    #GESTION.start_production("Cuillère", 18181, True)
    #GESTION.start_production("Spatule", 18181, True)
    #GESTION.start_production("Louche", 18181, True)
    #GESTION.start_production("Pelle à tarte", 18181, True)

    # Affichag du carnet de commande de l'usine
    ORDER = Order(USINE)

    # Lancement d'un aléa aléatoire
    if ALLOW_ALEA:
        Alea.launch_random_event(USINE)

    # Charge, capacité et taux de charge des machines
    ORDER.machine_capacity(USINE)



    # Boucle de la simulation (envoyer USINE et GESTION en paramètre) 
    #App.set_up()
        

