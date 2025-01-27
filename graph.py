import matplotlib.pyplot as plt

class Graph:

    def __init__(self):
        pass

    def capacity_chart(USINE, ORDER):
        taux_charge = []
        name_machines = []
        for i in range(len(USINE.machines)): # Stockage des noms des machines
            name_machines.append(USINE.machines[i].name)
        for i in range(len(USINE.machines)): # Stockage des taux de charge des machines
            taux_charge.append(ORDER.machine_capacity(USINE, USINE.machines[i].name, False))

        # Créer le diagramme en barres
        plt.figure(figsize=(10, 6))
        plt.bar(name_machines, taux_charge, color='skyblue')

        # Ajouter des titres et des étiquettes
        plt.title('Taux de charge des machines')
        plt.xlabel('Machines')
        plt.ylabel('Taux de charge (%)')

        # Ajouter une grille pour une meilleure lisibilité
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Afficher le diagramme
        plt.show()

    def stock_chart(list_materials):

        materials = []
        quantity = []
        for i in range(len(list_materials)):
            materials.append(list_materials[i].name)
            quantity.append(list_materials[i].quantity)

        # Créer le diagramme en barres
        plt.figure(figsize=(10, 6))
        plt.bar(materials, quantity, color='skyblue')

        # Ajouter des titres et des étiquettes
        plt.title('Quantité des matériaux')
        plt.xlabel('Matériaux')
        plt.ylabel('Quantité (kg)')

        # Ajouter une grille pour une meilleure lisibilité
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Afficher le diagramme
        plt.show()