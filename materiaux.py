from machine import Machine

class Material:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


class Recipes:
    def __init__(self, name, component,quantity):
        self.name = name #nom du produit
        self.component = [] #composition du produit
        self.quantity = [] #quantité de chaque composant

        #création du dictionnaire de composition
        self.composition = {"name" : name, "composition" : component , "quantity" : quantity}

        #ajout des composants et de leur quantité
        for i in range(len(component)):
            self.component.append(component[i])
            self.quantity.append(quantity[i])
        
class Gestion:
    def __init__(self):
        self.MACHINE = Machine()

        # Liste de quelques matériaux
        material1 = Material("Iron", 1000, 10)
        material2 = Material("Steel", 500, 20)
        material3 = Material("Copper", 2000, 5)
        material4 = Material("Aluminium", 1500, 15)
        material5 = Material("Plastic", 3000, 2)
        material6 = Material("Glass", 1000, 3)

        self.list_materials = []
        self.list_materials.append(material1)
        self.list_materials.append(material2)
        self.list_materials.append(material3)
        self.list_materials.append(material4)
        self.list_materials.append(material5)
        self.list_materials.append(material6)

        # Création de recettes
        recipe1 = Recipes("Screwdriver", ["Iron", "Plastic"], [1, 1])
        recipe2 = Recipes("Hammer", ["Iron", "Steel"], [2, 1])
        recipe3 = Recipes("Nail", ["Iron"], [1])
        recipe4 = Recipes("Screw", ["Iron"], [1])
        recipe5 = Recipes("Nut", ["Steel"], [1])
        recipe6 = Recipes("Bolt", ["Steel"], [1])

        self.list_recipes = []
        self.list_recipes.append(recipe1)
        self.list_recipes.append(recipe2)
        self.list_recipes.append(recipe3)
        self.list_recipes.append(recipe4)
        self.list_recipes.append(recipe5)
        self.list_recipes.append(recipe6)

    # Affichage des matériaux
    def display_materials(self): 
        print("Liste des matériaux : ")
        for i in range(len(self.list_materials)):
            print(self.list_materials[i].name, " : ", self.list_materials[i].quantity, " : ", self.list_materials[i].price)

    # Affichage des recettes
    def display_recipes(self):
        print("Liste des recettes : ")
        for i in range(len(self.list_recipes)):
            print(self.list_recipes[i].name, " : ", self.list_recipes[i].component, " : ", self.list_recipes[i].quantity)

    # Vérification de la disponibilité des matériaux
    def available_material(self, material):
        for i in range(len(self.list_materials)):
            if self.list_materials[i].name == material:
                print(self.list_materials[i].quantity," élement(s) de ", material, " sont disponibles")
                 
    def start_production(self, recipe):
        for i in range(len(self.list_recipes)):
            if self.list_recipes[i].name == recipe:
                print("La production de ", recipe, " a commencé")
                print("Passage sur", self.MACHINE.machine1.name, ":", self.MACHINE.machine1.type)
                for j in range(len(self.list_recipes[i].component)):
                    print("Consommation de ", self.list_recipes[i].quantity[j], " élement(s) de ", self.list_recipes[i].component[j])
                    for k in range(len(self.list_materials)):
                        if self.list_materials[k].name == self.list_recipes[i].component[j]:
                            self.list_materials[k].quantity -= self.list_recipes[i].quantity[j]
                            print("Il reste ", self.list_materials[k].quantity, " élement(s) de ", self.list_materials[k].name)
                print("Passage sur", self.MACHINE.machine2.name, ":", self.MACHINE.machine2.type)
                print("Passage sur", self.MACHINE.machine3.name, ":", self.MACHINE.machine3.type)
                print("La production de ", recipe, " est terminée")
                break
        else:
            print("La recette ", recipe, " n'existe pas")
    