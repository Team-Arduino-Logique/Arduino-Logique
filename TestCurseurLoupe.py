import tkinter as tk
import os

# Fonction pour changer le curseur lorsqu'il entre dans la zone
def on_enter(event, canvas, cursor_type):
    canvas.config(cursor=cursor_type)

# Fonction pour réinitialiser le curseur lorsqu'il sort de la zone
def on_leave(event):
    event.widget.config(cursor="")

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Curseur personnalisé de loupe")

# Création du canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Définir le chemin du curseur personnalisé
cursor_path = "loupe.xbm"

# Vérifier si le fichier existe
if not os.path.isfile(cursor_path):
    raise FileNotFoundError(f"Le fichier {cursor_path} n'existe pas")

# Définir un curseur personnalisé
custom_cursor = f"@{cursor_path} black white"

try:
    canvas.config(cursor=custom_cursor)
except tk.TclError as e:
    print(f"Erreur : {e}")

# Dessiner une zone (rectangle) sur le canvas
zone = canvas.create_rectangle(100, 100, 300, 200, fill="lightblue")

# Associer les événements d'entrée et de sortie de la souris à la zone
canvas.tag_bind(zone, "<Enter>", lambda event, can=canvas, cursor_type=custom_cursor: on_enter(event, can, cursor_type))
canvas.tag_bind(zone, "<Leave>", on_leave)

# Boucle principale de l'interface Tkinter
root.mainloop()
