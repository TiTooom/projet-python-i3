import tkinter as tk
from PIL import Image, ImageTk

class App:


    def afficher_images(self,fenetre, chemin_images):
        """Afficher des images dans une fenêtre Tkinter."""
        try:
            images = []
            for chemin in chemin_images:
                # Ouvrir l'image avec PIL (Pillow)
                image = Image.open(chemin)
                # Redimensionner les images pour une meilleure présentation (optionnel)
                image = image.resize((200, 200), Image.LANCZOS)  # Ajuster la taille selon vos besoins
                # Convertir l'image PIL en format Tkinter
                photo = ImageTk.PhotoImage(image)
                images.append(photo)

            # Créer des labels pour afficher les images
            labels = []
            for photo in images:
                label = tk.Label(fenetre, image=photo)
                label.pack(side=tk.LEFT, padx=10) # Aligner à gauche avec un espacement horizontal
                labels.append(label)

            # Garder une référence aux images pour éviter le garbage collection
            fenetre.images = images  # Important pour éviter que les images disparaissent

        except FileNotFoundError:
            print("Erreur : Au moins une image n'a pas été trouvée.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    @staticmethod
    def set_up():
    
        fenetre = tk.Tk()
        fenetre.title("Fenêtre de simulation")

        # Chemins des images à afficher
        chemins = ["assets/PM1.png", "assets/PM2.png", "assets/PM3.png"]

        app = App()
        app.afficher_images(fenetre, chemins)

        # Définir la taille de la fenêtre
        fenetre.geometry("800x600")  # Ajustez la taille selon vos besoins
        

        fenetre.mainloop()