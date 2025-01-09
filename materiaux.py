from machine import Machine

SECURITY_STOCK = 1000 # Stock de sécurité
ORDER_BATCH = 3000 # Quantité à commander pour les matériaux
ROUND = 3 # Arrondi pour les temps de production (N chiffre(s) après la virgule)

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
        material1 = Material("Fer", 10000, 10)
        material2 = Material("Acier", 5000, 20)
        material3 = Material("Cuivre", 20000, 5)
        material4 = Material("Aluminium", 15000, 15)
        material5 = Material("Plastique", 30000, 2)
        material6 = Material("Verre", 12000, 3)

        # Liste des matériaux
        self.list_materials = []
        self.list_materials.append(material1)
        self.list_materials.append(material2)
        self.list_materials.append(material3)
        self.list_materials.append(material4)
        self.list_materials.append(material5)
        self.list_materials.append(material6)

        # Création de recettes avec les matériaux et les machines
        recipe1 = Recipes("Tournevis", ["Fer", "Plastique"], [1, 1], [self.USINE.machines[0], self.USINE.machines[1]])
        recipe2 = Recipes("Marteau", ["Fer", "Acier"], [2, 1], [self.USINE.machines[0], self.USINE.machines[2]])
        recipe3 = Recipes("Clou", ["Fer"], [1], [self.USINE.machines[1]])
        recipe4 = Recipes("Vis", ["Fer"], [1], [self.USINE.machines[0]])
        recipe5 = Recipes("Ecrou", ["Acier"], [1], [self.USINE.machines[2]])
        recipe6 = Recipes("Boulon", ["Acier"], [1], [self.USINE.machines[1], self.USINE.machines[2]])

        # Liste des recettes
        self.list_recipes = []
        self.list_recipes.append(recipe1)
        self.list_recipes.append(recipe2)
        self.list_recipes.append(recipe3)
        self.list_recipes.append(recipe4)
        self.list_recipes.append(recipe5)
        self.list_recipes.append(recipe6)

    # Affichage des matériaux
    def display_materials(self): 
        print("\nListe des matériaux : ")
        for i in range(len(self.list_materials)):
            print(self.list_materials[i].name, " : ", self.list_materials[i].quantity, "kg : ", self.list_materials[i].price,"€/kg")
        return self.list_materials

    # Affichage des recettes
    def display_recipes(self, arg):
        if arg == True:
            print("\nListe des recettes : ")
            for i in range(len(self.list_recipes)):
                print(self.list_recipes[i].name, " : ", self.list_recipes[i].component, " : ", self.list_recipes[i].quantity)
        return self.list_recipes

    # Vérification de la disponibilité des matériaux
    def available_material(self, material):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                print(self.list_materials[i].quantity,"élement(s) de", material, "sont disponibles")
                 
    def start_production(self, recipe, quantity):
        for i in range(len(self.list_recipes)):
            if self.list_recipes[i].name == recipe: 
                #Lacement de la production
                total_quantity = 0
                print("\nLa production de", recipe, "a commencé")
                for j in range(len(self.list_recipes[i].component)): # Parcours des composants de la recette
                    print("Consommation de ", self.list_recipes[i].quantity[j]*quantity, "élement(s) de", self.list_recipes[i].component[j]) # Consommation des matériaux
                    total_quantity += self.list_recipes[i].quantity[j]*quantity # Calcul de la quantité totale de matériaux

                    # Commande de matériaux si nécessaire
                    index = 0 # Index pour situer les matériaux dans la liste
                    for material in self.list_materials:
                        
                        if material.name == self.list_recipes[i].component[j]: # Vérification de l'existence du matériel
                            if material.quantity < SECURITY_STOCK: # Vérification du stock de sécurité
                                self.order_materials(self.list_recipes[i].component[j], ORDER_BATCH) # Commande de matériaux
                                print("Commande de", ORDER_BATCH, "élement(s) de ", self.list_recipes[i].component[j], "passée") 

                            # Ne doit pas arriver en raison du stock de sécurité
                            if self.list_recipes[i].quantity[j]*quantity > material.quantity: # Vérification de la disponibilité des matériaux
                                print("Il n'y a pas assez de", self.list_recipes[i].component[j],"pour produire", recipe)
                                break
                     
                    
                            # Consommation des matériaux
                            self.list_materials[index].quantity -= self.list_recipes[i].quantity[j]*quantity
                            print("Le stock de", self.list_recipes[i].component[j], "est de",self.list_materials[index].quantity,"élement(s) après consommation")
                        index += 1
                
                # Passage sur les autres machines + Temps de production totale de la recette
                total_time = 0
                for machine in range(0,len(self.list_recipes[i].usedmachines)): # Parcours des machines
                    print("Passage sur", self.list_recipes[i].usedmachines[machine].name, ":", self.list_recipes[i].usedmachines[machine].type)
                    if self.list_recipes[i].usedmachines[machine].state == "stopped": # Vérification de l'état de la machine
                        print("La machine", self.list_recipes[i].usedmachines[machine].name, "est arrêtée")
                        while(1) :
                            # Arret de la machine et mise en pause du programme
                            pass
                    if self.list_recipes[i].usedmachines[machine].state == "maintenance":
                        print("La machine", self.list_recipes[i].usedmachines[machine].name, "est en maintenance")
                        while(1) :
                            # Maintenance de la machine et mise en pause du programme
                            pass
                            
                    if total_time == 0:
                        print("Détail calcul :")
                    print(self.list_recipes[i].usedmachines[machine].cycle_time,"/",self.list_recipes[i].usedmachines[machine].speed/100,"x",total_quantity)
                    total_time += self.list_recipes[i].usedmachines[machine].cycle_time / ((self.list_recipes[i].usedmachines[machine].speed)/100) * total_quantity # Calcul du temps de production
                    
                
                print("La production de", recipe, "prend", round(total_time, ROUND), "secondes")
                
                print("La production de ", quantity, recipe, "(s) est terminée")
                break
        
        else:
            print("La recette", recipe, "n'existe pas")
    
    def order_materials(self, material, quantity):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                self.list_materials[i].quantity += quantity
                print("Commande de", quantity, "élement(s) de", material, "passée")
                break
        else:
            print("Le matériel", material, "n'existe pas")