import tkinter as tk
from PIL import Image, ImageTk

# Fonction pour suivre la souris
def follow_mouse(event):
    # Déplacer l'image de loupe avec la souris
    canvas.coords(image_id, event.x, event.y)

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Curseur de loupe simulé")

# Création du canvas
canvas = tk.Canvas(root, width=1500, height=800, bg="white")
canvas.pack()
canvas.config(cursor="")
# Charger l'image de loupe
#loupe_image = Image.open("Icones/CleAnglaise_32.png")
#loupe_image = loupe_image.resize((32, 32), Image.ANTIALIAS)
#loupe_photo = ImageTk.PhotoImage(file="Icones/CleAnglaise_32.png")
loupe_photo = ImageTk.PhotoImage(file="Icones/Cadenas_48.png")

# Afficher l'image de loupe sur le canvas
image_id = canvas.create_image(200, 150, image=loupe_photo)

# Lier le mouvement de la souris à la fonction follow_mouse
canvas.bind("<Motion>", follow_mouse)

# Boucle principale de l'interface Tkinter
root.mainloop()
