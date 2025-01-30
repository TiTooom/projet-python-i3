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



   
    def find_recipe(self, recipe, print_production):
        for i in range(len(self.list_recipes)):
            if self.list_recipes[i].name == recipe.name:
                if print_production == True:
                    print("\nLa recette", recipe.name, "existe")
                return self.list_recipes[i]
        else:
            if print_production == True:
                print("\nLa recette", recipe.name, "n'existe pas")
            return 0
        
    def calculate_total_quantity(self, recipe, quantity, print_production):
        # Si la recette existe
        if self.find_recipe(recipe, False) != 0:
            total_quantity = 0 # Initialisation de la quantité totale
            
            for i in range(len(recipe.component)): # Parcours des composants de la recette
                if print_production == True:
                    print("Consommation de ", recipe.quantity[i] * quantity, "élement(s) de", recipe.component[i]) # Consommation des matériaux
                total_quantity += recipe.quantity[i] * quantity # Calcul de la quantité totale de matériaux
            return total_quantity

    def stock_management(self, recipe, quantity, print_production):
        
        # Vérification de l'existence du materiaux
        for i in range(len(recipe.component)): # Défilement des composants de la recette
            for j in range(len(self.list_materials)): # Défilement des matériaux du stock
                if recipe.component[i] == self.list_materials[j].name: # Le composant existe dans le stock
                    
                    # Si la quantité de matériaux est insuffisante mais supérieure à 0 > Commande automatique de matériaux
                    if self.list_materials[j].quantity < SECURITY_STOCK and self.list_materials[j].quantity >= 0: # Vérification du stock de sécurité
                        self.order_materials(recipe.component[i], BATCH_ORDER) # Commande de matériaux
                        if print_production == True:
                            print("Commande de", BATCH_ORDER, "élement(s) de", recipe.component[i], "passée pour entretenir le stock de sécurité") 
    
                    # Si la commande exige plus que disponible dans le stock > Commande automatique de matériaux (en quantité suffisante)
                    if recipe.quantity[i] * quantity > self.list_materials[j].quantity:
                        if print_production == True:
                            print("Il n'y a pas assez de", recipe.component[i],"pour produire", recipe.name)
                        self.order_materials(recipe.component[i], -(-recipe.quantity[i] * quantity // BATCH_ORDER) * BATCH_ORDER) # Arrondi à l'entier positif supérieur
                        if print_production == True:
                            print("Commande de", -(-recipe.quantity[i] * quantity // BATCH_ORDER) * BATCH_ORDER, "élement(s) de", recipe.component[i], "passée pour réaliser la commande plus tard.")
                        return 0
                
    def materials_consumption(self, recipe, quantity, print_production):
        # La recette est en prodcution et les matériaux sont consommés
        for i in range(len(recipe.component)): # Défilement des composants de la recette
            for j in range(len(self.list_materials)): # Défilement des matériaux du stock
                if recipe.component[i] == self.list_materials[j].name: # Le composant existe dans le stock
                    self.list_materials[j].quantity -= recipe.quantity[i] * quantity # Consommation des matériaux
                    if print_production == True:
                        print("Le stock de", recipe.component[i], "est de",self.list_materials[j].quantity,"élement(s) après consommation")
                    break
        return self.list_materials
    
    def calculate_production_time(self, recipe, quantity, print_production, machine_filter):
        total_time = 0 # Initialisation du temps de production
        total_quantity = self.calculate_total_quantity(recipe, quantity, False) # Calcul de la quantité totale de matériaux
        
        if print_production == True:
            print("Production de", recipe.name, ":", total_quantity, "élement(s)")

        
        for i in range(len(recipe.usedmachines)): # Défilement des machines utilisées pour la recette
            # Si la machine est sélectionnée ou si toutes les machines sont sélectionnées
            if machine_filter == recipe.usedmachines[i].name or machine_filter == "all":
            
                if print_production == True:
                    print("Passage sur", recipe.usedmachines[i].name, ":", recipe.usedmachines[i].type)
        
                # Si la machine est arrêtée
                if recipe.usedmachines[i].state == "stopped": # Vérification de l'état de la machine
                    if print_production == True:
                        print("La machine", recipe.usedmachines[i].name, "est arrêtée")
                    while(recipe.usedmachines[i] == "stopped") :
                        # Arret de la machine et mise en pause du programme
                        pass
                
                # Si la machine est en maintenance
                if recipe.usedmachines[i].state == "maintenance":
                    if print_production == True:
                        print("La machine", recipe.usedmachines[i].name, "est en maintenance")
                    while(recipe.usedmachines[i] == "maintenance") :    
                        # Maintenance de la machine et mise en pause du programme
                        pass
                        
                # Calcul du temps de production
                if total_time == 0: 
                    if print_production == True:
                        print("Détail du calcul par machine:")
                if print_production == True:
                    print(recipe.usedmachines[i].cycle_time,"/",recipe.usedmachines[i].speed / 100,"x",total_quantity)
                total_time += recipe.usedmachines[i].cycle_time / ((recipe.usedmachines[i].speed) / 100) * total_quantity # Calcul du temps de production
                # Fin de la production
                if print_production == True:
                    print("La production de", recipe.name, "prend", round(total_time, ROUND_SEC), "secondes ou", round(total_time/60, ROUND_MIN), "minutes")

        return total_time

    def order_materials(self, material, quantity, print_production):  
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                self.list_materials[i].quantity += quantity
                if print_production == True:
                    print("Commande de", quantity, "élement(s) de", material, "passée")
                break
        else:
            if print_production == True:
                print("Le matériel", material, "n'existe pas")


    def start_production(self, recipe, quantity, machine_filter, print_production):
        
        self.find_recipe(recipe, print_production) # Vérification de l'existence de la recette
        self.stock_management(recipe, quantity, print_production) # Gestion du stock de matériaux
        self.materials_consumption(recipe, quantity, print_production) # Consommation des matériaux
        capacity = self.calculate_production_time(recipe, quantity, print_production, machine_filter) # Calcul du temps de production
        return capacity