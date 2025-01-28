import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random



class DashboardApp:
    def __init__(self, USINE, ORDER, GESTION):
        self.usine = USINE
        self.order = ORDER
        self.gestion = GESTION
        self.root = tk.Tk()
        self.root.title("Tableau de Bord de Production")
        self.root.geometry("1300x800")

        # Zone pour afficher les informations des machines
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.info_label = ttk.Label(self.info_frame, text="Informations des Machines:")
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
        self.root.after(500, self.simulate_data_update)

        # Lancement de la production
        #self.order.production_loop(self.usine)

        # Mis à jour des graphiques
        self.simulate_data_update()
        self.root.mainloop()
        

    def simulate_data_update(self):
        # Simuler des données aléatoires
        machines = self.usine.machines
        materials = self.gestion.display_materials(False)

        self.update_info_display(self.usine)
        self.update_capacity_chart(self.usine, self.order)
        self.update_stock_chart(materials)
        self.update_random_chart()

        # Planifier la prochaine mise à jour
        self.root.after(5000, self.simulate_data_update)

    def update_info_display(self, usine):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"[STATE] : 'NAME' > CAPACITY (%) > SPEED (%) > CYCLE TIME (item/sec)\n")
        for machine in usine.machines:
            self.info_text.insert(tk.END, f"[{machine.state}] : '{machine.name}' > {self.order.machine_capacity(self.usine, machine.name, False)}% > {machine.speed}% > {machine.cycle_time}sec\n")

    def update_capacity_chart(self, usine, order):
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
        material_names = [material.name for material in materials]
        quantities = [material.quantity for material in materials]

        self.axes[1].clear()
        self.axes[1].bar(material_names, quantities, color='palegreen')
        self.axes[1].set_title('Quantité des matériaux')
        self.axes[1].set_xlabel('Matériaux')
        self.axes[1].set_ylabel('Quantité (kg)')
        self.axes[1].grid(axis='y', linestyle='--', alpha=0.7)
        self.canvases[1].draw()

    def update_random_chart(self):
        # Exemple de graphique aléatoire
        data = [random.uniform(0, 100) for _ in range(10)]
        self.axes[2].clear()
        self.axes[2].plot(data, color='violet')
        self.axes[2].set_title('Graphique Aléatoire')
        self.axes[2].set_xlabel('Temps')
        self.axes[2].set_ylabel('Valeur')
        self.axes[2].grid(axis='y', linestyle='--', alpha=0.7)
        self.canvases[2].draw()

