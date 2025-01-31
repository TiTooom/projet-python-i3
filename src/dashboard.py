import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

import database

TIME_SPEED = 4000 # Vitesse de simulation graphique (attention : plus la valeur est basse, plus le dashboard met de temps à s'afficher)




class DashboardApp:
    def __init__(self, USINE, ORDER, GESTION):
        
        # Récupération des données
        self.usine = USINE
        self.order = ORDER
        self.gestion = GESTION

        # Permet de fermer les commandes quand elles sont toutes traitées
        self.show = 1

        # Suivi des données de la database
        self.index_stock = 0
        self.index_alea = 0

        # Récupération des commandes
        self.list_order = self.order.get_order()

        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Tableau de Bord de Production")
        self.root.geometry("1300x800")

        # Zone pour afficher les informations des machines
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.info_label = ttk.Label(self.info_frame, text="Informations des Machines :")
        self.info_label.pack(side=tk.TOP, padx=10, pady=10)

        self.info_text = tk.Text(self.info_frame, height=10, width=80)
        self.info_text.pack(side=tk.TOP, padx=10, pady=10)

        # Zone pour les graphiques
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Initialiser les graphiques avec une hauteur augmentée
        self.figures = [Figure(figsize=(4, 4), dpi=100) for _ in range(3)]
        self.axes = [fig.add_subplot(111) for fig in self.figures]
        self.canvases = [FigureCanvasTkAgg(fig, master=self.graph_frame) for fig in self.figures]

        for i, canvas in enumerate(self.canvases):
            canvas.get_tk_widget().grid(row=0, column=i, sticky="nsew")

        # Configurer la grille pour que les colonnes aient le même espace
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(1, weight=1)
        self.graph_frame.grid_columnconfigure(2, weight=1)

        # Simuler l'envoi de données toutes les 5 secondes
        self.root.after(TIME_SPEED, self.simulate_data_update)

        # Mis à jour des graphiques
        self.simulate_data_update()

        # Lancer la boucle principale
        self.root.mainloop()
        
    def simulate_data_update(self):
        # Récupérer la liste des matériaux
        materials = self.gestion.display_materials(False)

        # Mettre à jour les graphiques
        self.update_info_display(self.usine)
        self.update_capacity_chart(self.usine, self.order)
        self.update_stock_chart(materials)
        self.update_production_order()

        # Planifier la prochaine mise à jour
        self.root.after(TIME_SPEED, self.simulate_data_update)

    def update_info_display(self, usine):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"[STATE] : 'NAME' : CAPACITY (%) : SPEED (%) : CYCLE TIME (sec/item)\n")
        for machine in usine.machines:
            self.info_text.insert(tk.END, f"[{machine.state}] : '{machine.name}' : {self.order.machine_capacity(self.usine, machine.name, False)} % : {machine.speed} % : {machine.cycle_time} sec/item\n")
        
        # Affichage des machines en surcharge
        for machine in usine.machines:
            if self.order.machine_capacity(self.usine, machine.name, False) > 100:
                self.info_text.insert(tk.END, f"[WARNING] Machine '{machine.name}' en surcharge : {self.order.machine_capacity(self.usine, machine.name, False)}%\n")

        # Affichage des informations de la ligne si la liste n'est pas vide
        if database.db_stock and self.index_stock < len(database.db_stock['component']):
            self.info_text.insert(tk.END, f"\n Commande de {database.db_stock['quantity'][self.index_stock]} '{database.db_stock['component'][self.index_stock]}' : {database.db_stock['reason'][self.index_stock]}\n")
            self.index_stock += 1

        if database.db_alea and self.index_alea < len(database.db_alea['name']):
            self.info_text.insert(tk.END, f"\n[WARNING] : {database.db_alea['name'][self.index_alea]} : {database.db_alea['message'][self.index_alea]}\n")
            self.index_alea += 1

        

    def update_capacity_chart(self, usine, order):
       
       # Récupérer les taux de charge des machines
        taux_charge = []
        name_machines = []
        for machine in usine.machines:
            name_machines.append(machine.name)
            taux_charge.append(order.machine_capacity(usine, machine.name, False))

        self.axes[0].clear()
        self.axes[0].bar(name_machines, taux_charge, color='mediumaquamarine')
        self.axes[0].set_title('Taux de charge des machines')
        self.axes[0].set_xlabel('Machines')
        self.axes[0].set_ylabel('Taux de charge (%)')
        self.axes[0].grid(axis='y', linestyle='--', alpha=0.7)
        self.canvases[0].draw()

    def update_stock_chart(self, materials):
        # Récupérer les noms et les quantités des matériaux
        material_names = [material.name for material in materials]
        quantities = [material.quantity for material in materials]

        # Mettre à jour le graphique
        self.axes[1].clear()
        self.axes[1].bar(material_names, quantities, color='palegreen')
        self.axes[1].set_title('Quantité des matériaux')
        self.axes[1].set_xlabel('Matériaux')
        self.axes[1].set_ylabel('Quantité (kg)')
        self.axes[1].grid(axis='y', linestyle='--', alpha=0.7)
        self.canvases[1].draw()

    def update_production_order(self):
        
        # Vérifier si toutes les commandes ont été traitées
        if not self.list_order["Recipe"] and self.show == 1:
            print("\nToutes les commandes ont été traitées.")
            for i in range(0, len(self.usine.machines)):
                self.usine.machines[i].state = "break"
            self.show = 2
            return self.usine.machines
        
        # Empeche la recherche de commande quand la liste est vide
        if self.show == 2:
            return self.usine.machines

        # Sauvegarde des données de production
        if not hasattr(self, 'produced_data'):
            self.produced_data = {'name': [], 'quantity': []}


        # Prendre le premier élément de la liste
        recipe = self.list_order["Recipe"][0]
        name = self.list_order["Recipe"].pop(0).name
        quantity = self.list_order["Quantity"].pop(0)

        # Sauvegarde des données et continuer de les afficher sur le graphique
        self.produced_data['name'].append(name)
        self.produced_data['quantity'].append(quantity)

        # Lancement réel production avec calcul et maj stock
        self.gestion.start_production(recipe, quantity, "all", True, "capacity")
        time.sleep(3)

        # Mise à jour du graphique
        self.axes[2].clear()
        self.axes[2].bar(self.produced_data['name'], self.produced_data['quantity'], color='skyblue')
        self.axes[2].set_title('Quantité élements produits')
        self.axes[2].set_xlabel('Recettes')
        self.axes[2].set_ylabel('élemnents')
        self.axes[2].grid(axis='y', linestyle='--', alpha=0.7)
        self.canvases[2].draw()

