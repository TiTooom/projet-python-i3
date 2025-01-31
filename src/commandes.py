# Fichier contenant le carnet de commande de l'usine
from materiaux import Gestion

WORKING_TIME = 8 * 3600 # 8h de travail en secondes

class Order:
    def __init__(self,usine):
        
        self.recipes = Gestion(usine).display_recipes(False)
        
        # Création d un dictionnaire de commande
        self.order = {"Recipe": [self.recipes[0], self.recipes[1], self.recipes[2], self.recipes[3], self.recipes[4], self.recipes[5]], 
                      "Quantity": [3500, 4100, 3200, 5400, 3900, 7200]} #
       
        # Affichage du carnet de commande
        print("\nListe des commandes : ")
        for i in range(len(self.order["Recipe"])):
            print(self.order["Recipe"][i].name, " : ", self.order["Quantity"][i], " pièces")
        
    # Récupération de la commande
    def get_order(self):
        return self.order

    # Calcul de la capacité de la machine
    def machine_capacity(self, usine, machine_filter, print_capacity):
        # Reset de la charge (s)
        load = 0

        for i in range(len(self.order["Recipe"])):
            load += Gestion(usine).start_production(self.order["Recipe"][i], self.order["Quantity"][i], machine_filter, False, "capacity") # false permet d'uniquement utiliser le calcul
                
        # Capacité totale de la machine
        capacity = WORKING_TIME

        if print_capacity == True:
            print("\nCharge totale de",machine_filter,": ", round(load,2), " secondes")  
            print("Capacité totale de",machine_filter,": ", round(capacity,2), " secondes")
            print("Taux de charge de",machine_filter,": ", round(load/capacity*100, 2), "%") 

        return round(load/capacity*100, 2)

    # Calcul de la surcharge
    def overload(self,usine):

        # Récupération du taux de charge le plus fort
        for index in range(0,len(usine.machines)):
            val = self.machine_capacity(usine, usine.machines[index].name, False)
            if (index+1) <= len(usine.machines)-1:
                if self.machine_capacity(usine, usine.machines[index+1].name, False) > val :
                    val = self.machine_capacity(usine, usine.machines[index+1].name, False)
                    name_overload = usine.machines[index+1].name

        # Récupération des taux de charge  > 100%
        stock_overload = []
        for index in range(0,len(usine.machines)):
            val = self.machine_capacity(usine, usine.machines[index].name, False)
            name_overload = usine.machines[index].name
            if val > 100:
                if usine.machines[index].name != name_overload:
                    stock_overload.append(usine.machines[index].name)
                    print("\nLa machine :", usine.machines[index].name, "est en surcharge avec un taux de charge de ", val, "%")
        
        
        print("\nLa machine :", name_overload, "est la plus surchagée avec un taux de charge de ", val, "%")
        return stock_overload, name_overload
    
    # Calcul du goulot d'étranglement
    def bottleneck(self,usine):
        # Récupération du taux de charge le plus fort
        for index in range(0,len(usine.machines)):
            val = usine.machines[index].speed * usine.machines[index].cycle_time / 100 # Vitesse de la machine * temps de cycle
            name_bottleneck = usine.machines[index].name
            if (index+1) <= len(usine.machines)-1: # Vérification de la fin de la liste
                if usine.machines[index+1].speed * usine.machines[index+1].cycle_time / 100 < val : # Si machine suivante plus lente
                    val = usine.machines[index+1].speed * usine.machines[index+1].cycle_time / 100 # Machine suivante devient le goulot
                    name_bottleneck = usine.machines[index+1].name 

        print("\nLa machine :", name_bottleneck, "est le goulot d'étranglement une efficacité de", round(val,2), "par opération")

        return name_bottleneck



        
        

                


        
