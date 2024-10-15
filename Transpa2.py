import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageGrab

def capture_background(canvas, x1, y1, x2, y2):
    # Convertir les coordonnées canvas en coordonnées de l'écran
    x1 = canvas.winfo_rootx() + x1
    y1 = canvas.winfo_rooty() + y1
    x2 = canvas.winfo_rootx() + x2
    y2 = canvas.winfo_rooty() + y2
    
    # Capturer la zone spécifiée directement à partir de l'écran
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    return image

def create_semi_transparent_shape(background, shape_color, alpha):
    # Appliquer un effet de transparence sur l'image capturée
    overlay = Image.new('RGBA', background.size, shape_color + (alpha,))
    background = Image.alpha_composite(background.convert('RGBA'), overlay)
    
    return background

def move_shape(event):
    # Déplacer l'image en suivant la souris
    x1, y1 = event.x - 50, event.y - 50
    x2, y2 = event.x + 50, event.y + 50
    
    # Capturer l'arrière-plan sous la zone où la forme sera dessinée
    background = capture_background(canvas, x1, y1, x2, y2)
    
    # Créer une forme semi-transparente en superposant sur l'arrière-plan
    semi_transparent_shape = create_semi_transparent_shape(background, (255, 0, 0), 128)
    
    # Convertir en image Tkinter
    tk_image = ImageTk.PhotoImage(semi_transparent_shape)
    
    # Mettre à jour l'image sur le canvas
    canvas.itemconfig(image_on_canvas, image=tk_image)
    canvas.coords(image_on_canvas, x1, y1)
    canvas.image = tk_image  # Prévenir la suppression de l'image par le garbage collector

# Création de la fenêtre principale
root = tk.Tk()
root.title("Forme semi-transparente sur fond complexe")

# Création du canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Dessiner des formes sur le canvas pour créer un fond complexe
canvas.create_rectangle(50, 50, 200, 200, fill="blue", outline="")
canvas.create_oval(150, 150, 300, 300, fill="green", outline="")
canvas.create_line(0, 0, 400, 400, fill="black", width=5)
canvas.create_text(200, 50, text="Canvas Complex", font=("Helvetica", 16), fill="purple")

# Créer une image vierge sur le canvas (qui sera mise à jour plus tard)
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW)

# Lier le mouvement de la souris pour déplacer la forme
canvas.bind("<B1-Motion>", move_shape)

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
