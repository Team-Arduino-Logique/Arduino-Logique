import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def create_semi_transparent_image(width, height, color, alpha):
    # Créer une image RGBA (avec un canal alpha)
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    
    # Créer un dessin sur cette image
    draw = ImageDraw.Draw(image)
    
    # Dessiner un rectangle semi-transparent
    draw.rectangle([0, 0, width, height], fill=color + (alpha,))
    
    return image

def move_image(event):
    # Déplacer l'image en suivant la souris
    canvas.coords(image_on_canvas, event.x, event.y)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Forme semi-transparente sur un Canvas")

image_path = "Icones/Fd_plaquette.png"  # Remplacez par le chemin de votre image
pil_image = Image.open(image_path)

# Convertir l'image PIL en un objet compatible avec Tkinter
tk_image = ImageTk.PhotoImage(pil_image)


# Création du canvas
#canvas = tk.Canvas(root, width=400, height=400)
canvas = tk.Canvas(root, width=pil_image.width, height=pil_image.height)
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
# Création d'une image semi-transparente avec Pillow
semi_transparent_image = create_semi_transparent_image(100, 100, (255, 0, 0), 128)  # Rectangle rouge avec alpha 128 (semi-transparent)

# Convertir l'image pour Tkinter
tk_image = ImageTk.PhotoImage(semi_transparent_image)

# Afficher l'image sur le canvas
#image_on_canvas = canvas.create_image(200, 200, image=tk_image, anchor=tk.CENTER)

# Lier le mouvement de la souris pour déplacer l'image
#canvas.bind("<B1-Motion>", move_image)

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
