# Fichier contenant le carnet de commande de l'usine
from materiaux import Recipes
from materiaux import Gestion

class Order:
    def __init__(self,usine):
        self.recipes = Gestion(usine).display_recipes(False)
        
        # Création d un dictionnaire de commande
        self.order = {"Recipe": [self.recipes[0], self.recipes[1], self.recipes[2], self.recipes[3], self.recipes[4], self.recipes[5]], 
                      "Quantity": [54545, 54545, 54545, 54545, 54545, 54545]} # ~ <24h de production à 0.2sec près
                      
        # Affichage du carnet de commande
        print("\nListe des commandes : ")
        for i in range(len(self.order["Recipe"])):
            print(self.order["Recipe"][i].name, " : ", self.order["Quantity"][i], " pièces")

        
