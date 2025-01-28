import time
import random

from alea import Alea

SECURITY_STOCK = 10000 # Stock de sécurité
BATCH_ORDER = 7000 # Quantité à commander pour les matériaux
ROUND_SEC = 3 # Arrondi pour les temps de production (N chiffre(s) après la virgule)
ROUND_MIN = 3 # Arrondi pour les temps de production (N chiffre(s) après la virgule)
TIME_SPEED = 1 # Accéleration virtuelle du temps de production

class Material:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


class Recipes:
    def __init__(self, name, component,quantity, usedmachines):
        self.name = name #nom du produit
        self.component = [] #composition du produit
        self.quantity = [] #quantité de chaque composant
        self.usedmachines = usedmachines #machines utilisées pour la production

        #création du dictionnaire de composition
        self.composition = {"name" : name, "composition" : component , "quantity" : quantity}

        #ajout des composants et de leur quantité
        for i in range(len(component)):
            self.component.append(component[i])
            self.quantity.append(quantity[i])
        
class Gestion:
    def __init__(self, usine):

        # Récupération de l'usine pour la gestion des matériaux
        self.USINE = usine

        # Liste de quelques matériaux
        material1 = Material("Fer", 100000, 10)
        material2 = Material("Acier", 50000, 20)
        material3 = Material("Cuivre", 200000, 5)
        material4 = Material("Aluminium", 150000, 15)
        material5 = Material("Plastique", 300000, 2)
        material6 = Material("Verre", 120000, 3)

        # Liste des matériaux
        self.list_materials = []
        self.list_materials.append(material1)
        self.list_materials.append(material2)
        self.list_materials.append(material3)
        self.list_materials.append(material4)
        self.list_materials.append(material5)
        self.list_materials.append(material6)

        # Création de recettes avec les matériaux et les machines
        recipe1 = Recipes("Couteau", ["Fer", "Plastique"], [1, 1], [self.USINE.machines[0], self.USINE.machines[1]])
        recipe2 = Recipes("Fourchette", ["Fer", "Acier"], [2, 1], [self.USINE.machines[0], self.USINE.machines[2]])
        recipe3 = Recipes("Cuillère", ["Fer"], [1], [self.USINE.machines[1]])
        recipe4 = Recipes("Spatule", ["Fer"], [1], [self.USINE.machines[0]])
        recipe5 = Recipes("Louche", ["Acier"], [1], [self.USINE.machines[2]])
        recipe6 = Recipes("Pelle à tarte", ["Acier"], [1], [self.USINE.machines[1], self.USINE.machines[2]])

        # Liste des recettes
        self.list_recipes = []
        self.list_recipes.append(recipe1)
        self.list_recipes.append(recipe2)
        self.list_recipes.append(recipe3)
        self.list_recipes.append(recipe4)
        self.list_recipes.append(recipe5)
        self.list_recipes.append(recipe6)

    # Affichage des matériaux
    def display_materials(self, print_materials): 
        
        if print_materials == True:
            print("\nListe des matériaux : ")
            for i in range(len(self.list_materials)):
                print(self.list_materials[i].name, " : ", self.list_materials[i].quantity, "kg : ", self.list_materials[i].price,"€/kg")
        return self.list_materials

    # Affichage des recettes
    def display_recipes(self, print_recipes):
        if print_recipes == True:
            print("\nListe des recettes : ")
            for i in range(len(self.list_recipes)):
                print(self.list_recipes[i].name, " : ", self.list_recipes[i].component, " : ", self.list_recipes[i].quantity)
        return self.list_recipes

    # Vérification de la disponibilité des matériaux
    def available_material(self, material):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                print(self.list_materials[i].quantity,"élement(s) de", material, "sont disponibles")
                 
    def start_production(self, recipe, quantity, machine_filter,print_production, print_simulation):

        for i in range(len(self.list_recipes)):

            # Vérification de l'existence de la recette
            if self.list_recipes[i].name == recipe: 
                #Lacement de la production
                total_quantity = 0
                if print_production == True:
                    print("\nLa production de", recipe, "a commencé")
                for j in range(len(self.list_recipes[i].component)): # Parcours des composants de la recette
                    if print_production == True:
                        print("Consommation de ", self.list_recipes[i].quantity[j]*quantity, "élement(s) de", self.list_recipes[i].component[j]) # Consommation des matériaux
                    total_quantity += self.list_recipes[i].quantity[j]*quantity # Calcul de la quantité totale de matériaux

                    # Commande de matériaux si nécessaire
                    index = 0 # Index pour situer les matériaux dans la liste
                    for material in self.list_materials:
                        
                        # Commande de stock pour entretenir le stock de sécurité
                        if material.name == self.list_recipes[i].component[j]: # Vérification de l'existence du matériel
                            if material.quantity < SECURITY_STOCK and material.quantity >= 0: # Vérification du stock de sécurité
                                self.order_materials(self.list_recipes[i].component[j], BATCH_ORDER) # Commande de matériaux
                                if print_production == True:
                                    print("Commande de", BATCH_ORDER, "élement(s) de", self.list_recipes[i].component[j], "passée pour entretenir le stock de sécurité") 

                            # commande en grosse quantité pour fournir les grosses commandes et met fin à la production de la recette
                            if self.list_recipes[i].quantity[j]*quantity > material.quantity: # Vérification de la disponibilité des matériaux
                                if print_production == True:
                                    print("Il n'y a pas assez de", self.list_recipes[i].component[j],"pour produire", recipe)
                                    self.order_materials(self.list_recipes[i].component[j], -(-self.list_recipes[i].quantity[j]*quantity // BATCH_ORDER) * BATCH_ORDER) # Arrondi à l'entier positif supérieur
                                    print("Commande de", -(-self.list_recipes[i].quantity[j]*quantity // BATCH_ORDER) * BATCH_ORDER, "élement(s) de", self.list_recipes[i].component[j], "passée pour réaliser la commande plus tard.")
                                return 0
                     
                    
                            # Consommation des matériaux
                            if print_production == True: #Permet de ne pas retirer dans le stock et juste faire les calculs
                                self.list_materials[index].quantity -= self.list_recipes[i].quantity[j]*quantity
                            if print_production == True:
                                print("Le stock de", self.list_recipes[i].component[j], "est de",self.list_materials[index].quantity,"élement(s) après consommation")
                        index += 1
                
                # Passage sur les autres machines + Temps de production totale de la recette
                total_time = 0
                for machine in range(0,len(self.list_recipes[i].usedmachines)): # Parcours des machines
                    
                    if machine_filter == self.list_recipes[i].usedmachines[machine].name or machine_filter == "all":
                        if print_production == True:
                            print("Passage sur", self.list_recipes[i].usedmachines[machine].name, ":", self.list_recipes[i].usedmachines[machine].type)
                            
                        
                        # Si la machine est arrêtée
                        if self.list_recipes[i].usedmachines[machine].state == "stopped": # Vérification de l'état de la machine
                            if print_production == True:
                                print("La machine", self.list_recipes[i].usedmachines[machine].name, "est arrêtée")
                            while(self.list_recipes[i].usedmachines[machine] == "stopped") :
                                # Arret de la machine et mise en pause du programme
                                pass
                        
                        # Si la machine est en maintenance
                        if self.list_recipes[i].usedmachines[machine].state == "maintenance":
                            if print_production == True:
                                print("La machine", self.list_recipes[i].usedmachines[machine].name, "est en maintenance")
                            while(self.list_recipes[i].usedmachines[machine] == "maintenance") :    
                                # Maintenance de la machine et mise en pause du programme
                                pass
                                
                        # Calcul du temps de production
                        if total_time == 0:
                            if print_production == True:
                                print("Détail du calcul par machine:")
                        if print_production == True:
                            print(self.list_recipes[i].usedmachines[machine].cycle_time,"/",self.list_recipes[i].usedmachines[machine].speed/100,"x",total_quantity)
                        total_time += self.list_recipes[i].usedmachines[machine].cycle_time / ((self.list_recipes[i].usedmachines[machine].speed)/100) * total_quantity # Calcul du temps de production
                    
                
                    

                # Fin de la production
                if print_production == True:
                    print("La production de", recipe, "prend", round(total_time, ROUND_SEC), "secondes ou", round(total_time/60, ROUND_MIN), "minutes")

                if print_simulation == True:
                    # Simulation du passage sur les machines
                    for total in range(0,total_quantity):
                        

                        # Probabilité d'un aléa
                        proba = random.randint(0,100)
                        if proba == 1:
                            Alea.launch_random_event(self.USINE)

                        for machine in range(0,len(self.list_recipes[i].usedmachines)):
                            print("[",total,"] Passage sur", self.list_recipes[i].usedmachines[machine].name, ":", self.list_recipes[i].usedmachines[machine].type)
                            time.sleep(self.list_recipes[i].usedmachines[machine].cycle_time / TIME_SPEED)
                        if print_production == True:
                            print("Production de 1",recipe, "terminée.")
                



                if print_production == True:
                    print("La production de",quantity, recipe, "(s) est terminée")
                return total_time
        
        else:
            print("La recette", recipe, "n'existe pas")
    
    def order_materials(self, material, quantity):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                self.list_materials[i].quantity += quantity
                #print("Commande de", quantity, "élement(s) de", material, "passée")
                break
        else:
            print("Le matériel", material, "n'existe pas")