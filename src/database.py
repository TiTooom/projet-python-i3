# Base de données partagées entre les différents fichier
'''
Base de données éphémères pour stocker les informations des machines, des aléas et des stocks le temps
de la simulation. Il y aurait possibilité de prolonger cette base de données pour stocker les informations de la simulation et pouvoir la continuer plus tard.
'''

db_alea = {"name": [], "machine": [], "type": [], "message": [], "duration": [], "state": []}
db_stock = {"component": [], "quantity": [], "reason": []}