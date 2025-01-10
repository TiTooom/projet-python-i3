# Fichier contenant le carnet de commande de l'usine
from materiaux import Recipes
from materiaux import Gestion

WORKING_TIME = 8 * 3600 # 8h de travail en secondes

class Order:
    def __init__(self,usine):
        self.recipes = Gestion(usine).display_recipes(False)
        
        # Création d un dictionnaire de commande
        self.order = {"Recipe": [self.recipes[0], self.recipes[1], self.recipes[2], self.recipes[3], self.recipes[4], self.recipes[5]], 
                      "Quantity": [35000, 41000, 32000, 54000, 39000, 72000]} # 
                      
        # Affichage du carnet de commande
        print("\nListe des commandes : ")
        for i in range(len(self.order["Recipe"])):
            print(self.order["Recipe"][i].name, " : ", self.order["Quantity"][i], " pièces")

    def machine_capacity(self, usine): # Calcul de la capacité et de la charge de chaque machine sur le carnert de commande
        # Reset de la charge (s)
        load = 0

        for i in range(len(self.order["Recipe"])):
            load += Gestion(usine).start_production(self.order["Recipe"][i].name, self.order["Quantity"][i], False) # false permet d'uniquement utiliser le calcul
                
        # Capacité totale des machines
        capacity = len(usine.machines) * WORKING_TIME

        print("\nCharge totale des machines : ", load, " secondes")  
        print("Capacité totale des machines : ", capacity, " secondes")
        print("Taux de charge des machines : ", round(load/capacity*100, 2), "%")    
        

                


        
