#Fichier qui va invoquer de manière aléatoire des évenements

import random
import logging
import random
import os
import time

import database

TIME_SLEEP = 1 # Accelérer le temps de l'aléa
ALEA_PROBA = 90 # probabilité de ne pas avoir d'aléa

class Alea:

    def __init__(self, factory,name, localization, description, duration, machine_state):
        self.factory = factory # aléa lié à l'usine
        self.name = name # nom de l'aléa
        self.localization = localization # localisation de l'aléa
        self.description = description # description de l'aléa
        self.duration = duration # durée de l'aléa en seconde
        self.machine_state = machine_state # état de la machine après l'aléa

        # Configuration du logger
        log_file = "logs/simulation.txt"
        setup_logger(log_file)

    @staticmethod
    def launch_random_event(factory):

        # Choix aléatoire d'un aléa
        alea_number = random.randint(0, len(factory.alea)-1)
        print("\nAléa survenu : ", factory.alea[alea_number].name)
        print("Description de l'aléa : ", factory.alea[alea_number].description)
        logging.critical(f"Alea apparu : {factory.alea[alea_number].name}")
        
        # Arrêt de la machine
        factory.alea[alea_number].factory.machines[alea_number].state = factory.alea[alea_number].machine_state
        print("L'état de la machine ", factory.alea[alea_number].factory.machines[alea_number].name, " est : ", factory.alea[alea_number].machine_state)
        logging.warning(f"L'etat de la machine {factory.alea[alea_number].factory.machines[alea_number].name} est : {factory.alea[alea_number].machine_state}")
        
        # Durée de l'aléa
        print("Durée de l'aléa : ", factory.alea[alea_number].duration, " secondes")
        logging.info(f"Duree de l'alea : {factory.alea[alea_number].duration} secondes\n")
        time.sleep(factory.alea[alea_number].duration / TIME_SLEEP) # pause de la durée de l'aléa

        # Sauvegarde des données de l'aléa dans la database
        database.db_alea["name"].append(factory.alea[alea_number].name)
        database.db_alea["machine"].append(factory.alea[alea_number].factory.machines[alea_number].name)
        database.db_alea["type"].append(factory.alea[alea_number].factory.machines[alea_number].type)
        database.db_alea["message"].append(factory.alea[alea_number].description)



    def start_event_proba(factory):
        # Probabilité d'aléa
        proba = random.randint(0, 100)
        if proba > ALEA_PROBA:
            Alea.launch_random_event(factory)
            return True

# Configuration du logger (une seule fois au début du programme)
def setup_logger(log_file_path):
    """Configure le logger pour écrire dans un fichier, en écrasant le contenu existant."""
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        filename=log_file_path,
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


