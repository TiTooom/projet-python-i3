# Récapitulatif du projet par rapport au sujet en PDF :

## 1. Initialisation de l'usine

Usine : contient les informations générales (nom, localisation, capacité de stockage).
- fichier "usine.py", classe "Factory" puis instance dans main x1

Machine : a des attributs tels que type, débit maximal, temps de cycle, et état (actif, en panne, en 
maintenance).
- fichier "machine.py", classe "Machine" puis instance dans main x3

Matériaux : inclut nom, quantité disponible, et coût.
- fichier "materiaux.py", classe "Material" puis instance dans classe "Gestion" x6

## 2. Gestion des recettes et production

Définir des recettes sous forme de dictionnaires (exemple : Aluminium -> Fourchette nécessite 5 unités 
d'Aluminium).
- fichier "materiaux.py", classe "Recipe" puis instance dans classe "Gestion" x6 

Implémenter une fonction pour :
Vérifier la disponibilité des matériaux.
- fichier "materiaux.py", classe "Gestion", fonction "available_material" -> vérifie la disponibilité des matériaux

Déclencher le processus de production.
- fichier "materiaux.py", classe "Gestion", fonction "start_production" -> déclenche la production d'une recette

Simuler le temps requis en fonction des machines disponibles.
- fichier "materiaux.py", classe "Gestion", fonction "start_production" (fonction générale incluant plusieurs processus)

## 3. Gestion des flux et des machines

Ajouter un mécanisme de file d'attente pour les matières premières à transformer.
- fichier "commandes.py", définition d'un carnet de commande qui va être envoyé en production [A COMPLETER]

Simuler le fonctionnement de plusieurs machines, en prenant en compte :
Le nombre de machines nécessaires pour une recette.
- fichier "materiaux.py", classe "Recipe", définitions des machines à utiliser pour chaque recette (stockées dans la liste usedmachines[]) 

Le temps de traitement.
- fichier "materiaux.py", classe "Gestion", fonction "start_production" 

Mettre en pause la production si une machine est en panne ou en maintenance.
- fichier "materiaux.py", classe "Gestion", fonction "start_production" 

## 4. Détection et gestion des anomalies

Créer une fonction pour détecter des anomalies courantes, telles que :
Pannes de machines : simulation aléatoire.
- fichier "alea.py", classe "Alea", fonction "launch_random_event" -> déclenche une panne aléatoire avec un délai avant réparation

Manque de matériaux : message d’alerte. 
- fichier "materiaux.py", classe "Gestion", fonction "start_production" 
-> vérifie si le stock de sécurité est dépassé
-> commande des matériaux si nécessaire (fonction "order_materials") avec un lot de commande

Dépassement de capacité : déclenchement d’un état critique.
- [A FAIRE]

Intégrer un journal des anomalies (log des incidents).
- fichier "alea.py", classe "Alea", fonction "launch_random_event" -> écriture de l'incident dans un fichier log

## 5. Visualisation et rapports