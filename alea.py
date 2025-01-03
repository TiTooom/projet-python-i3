#Fichier qui va invoquer de manière aléatoire des évenements

from random import randint
import logging
import os

from usine import Factory

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
        alea_number = randint(0, len(factory.alea)-1)
        print("\nAléa choisi : ", factory.alea[alea_number].name)
        print("Description de l'aléa : ", factory.alea[alea_number].description)
        logging.critical(f"Alea apparu : {factory.alea[alea_number].name}")
        
        # Arrêt de la machine
        factory.alea[alea_number].factory.machines[alea_number].state = factory.alea[alea_number].machine_state
        print("L'état de la machine ", factory.alea[alea_number].factory.machines[alea_number].name, " est : ", factory.alea[alea_number].machine_state)
        logging.warning(f"L'etat de la machine {factory.alea[alea_number].factory.machines[alea_number].name} est : {factory.alea[alea_number].machine_state}")
        
        # Durée de l'aléa
        print("Durée de l'aléa : ", factory.alea[alea_number].duration, " secondes")
        logging.info(f"Duree de l'alea : {factory.alea[alea_number].duration} secondes")
        
        # Fin de l'aléa
        factory.alea[alea_number].factory.machines[alea_number].state = "running"
        print("L'état de la machine ", factory.alea[alea_number].factory.machines[alea_number].name, " est : ", factory.alea[alea_number].factory.machines[alea_number].state)
        logging.info(f"L'etat de la machine {factory.alea[alea_number].factory.machines[alea_number].name} est : {factory.alea[alea_number].factory.machines[alea_number].state}")


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

