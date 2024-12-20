class Material:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


class Recipes:
    def __init__(self, name, composition,quantity):
        self.name = name #nom du produit
        self.composition = [] #composition du produit
        self.quantity = [] #quantité de chaque composant

        #création du dictionnaire de composition
        self.composition = {"name" : name, "composition" : [] , "quantity" : []}

        #ajout des composants et de leur quantité
        for i in range(len(composition)):
            self.composition["composition"].append(composition[i])
            self.composition["quantity"].append(quantity[i])



