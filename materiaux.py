from machine import Machine

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
        material1 = Material("Iron", 1000, 10)
        material2 = Material("Steel", 500, 20)
        material3 = Material("Copper", 2000, 5)
        material4 = Material("Aluminium", 1500, 15)
        material5 = Material("Plastic", 3000, 2)
        material6 = Material("Glass", 1000, 3)

        # Liste des matériaux
        self.list_materials = []
        self.list_materials.append(material1)
        self.list_materials.append(material2)
        self.list_materials.append(material3)
        self.list_materials.append(material4)
        self.list_materials.append(material5)
        self.list_materials.append(material6)

        # Création de recettes avec les matériaux et les machines
        recipe1 = Recipes("Screwdriver", ["Iron", "Plastic"], [1, 1], [self.USINE.machines[0], self.USINE.machines[1]])
        recipe2 = Recipes("Hammer", ["Iron", "Steel"], [2, 1], [self.USINE.machines[0], self.USINE.machines[2]])
        recipe3 = Recipes("Nail", ["Iron"], [1], [self.USINE.machines[1]])
        recipe4 = Recipes("Screw", ["Iron"], [1], [self.USINE.machines[0]])
        recipe5 = Recipes("Nut", ["Steel"], [1], [self.USINE.machines[2]])
        recipe6 = Recipes("Bolt", ["Steel"], [1], [self.USINE.machines[1], self.USINE.machines[2]])

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

    # Affichage des recettes
    def display_recipes(self):
        print("\nListe des recettes : ")
        for i in range(len(self.list_recipes)):
            print(self.list_recipes[i].name, " : ", self.list_recipes[i].component, " : ", self.list_recipes[i].quantity)

    # Vérification de la disponibilité des matériaux
    def available_material(self, material):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                print(self.list_materials[i].quantity," élement(s) de ", material, " sont disponibles")
                 
    def start_production(self, recipe, quantity):
        for i in range(len(self.list_recipes)):
            if self.list_recipes[i].name == recipe:
                #Lacement de la production
                total_quantity = 0
                print("\nLa production de ", recipe, " a commencé")
                for j in range(len(self.list_recipes[i].component)): # Parcours des composants de la recette
                    print("Consommation de ", self.list_recipes[i].quantity[j]*quantity, " élement(s) de ", self.list_recipes[i].component[j]) # Consommation des matériaux
                    total_quantity += self.list_recipes[i].quantity[j]*quantity # Calcul de la quantité totale de matériaux
                    if self.list_recipes[i].quantity[j]*quantity > self.list_materials[j].quantity: # Vérification de la disponibilité des matériaux
                        print("Il n'y a pas assez de ", self.list_recipes[i].component[j]," pour produire ", recipe) 
                        return False
                    
                    # Consommation des matériaux
                    for k in range(len(self.list_materials)): 
                        if self.list_materials[k].name == self.list_recipes[i].component[j]:
                            self.list_materials[k].quantity -= self.list_recipes[i].quantity[j]*quantity
                            print("Il reste ", self.list_materials[k].quantity, " élement(s) de ", self.list_materials[k].name)
                
                # Passage sur les autres machines
                for i in range(len(self.list_recipes[i].usedmachines)): # Parcours des machines
                    print("Passage sur", self.list_recipes[i].usedmachines[i].name, ":", self.list_recipes[i].usedmachines[i].type)
                
                # Temps de production totale de la recette
                total_time = 0
                for i in range(len(self.list_recipes[i].usedmachines)):
                    total_time += self.list_recipes[i].usedmachines[i].cycle_time*(self.list_recipes[i].usedmachines[i].speed/100)*total_quantity
                print("La production de ", recipe, " prend ", total_time, " secondes")

                print("La production de ",quantity, recipe, "(s) est terminée")
                break
        else:
            print("La recette ", recipe, " n'existe pas")
    