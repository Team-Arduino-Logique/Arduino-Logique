import tkinter as tk

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25):
    # Top left arc
    canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, style=tk.ARC)
    # Top right arc
    canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, style=tk.ARC)
    # Bottom right arc
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, style=tk.ARC)
    # Bottom left arc
    canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, style=tk.ARC)

    # Top side
    canvas.create_line(x1 + radius, y1, x2 - radius, y1)
    # Right side
    canvas.create_line(x2, y1 + radius, x2, y2 - radius)
    # Bottom side
    canvas.create_line(x1 + radius, y2, x2 - radius, y2)
    # Left side
    canvas.create_line(x1, y1 + radius, x1, y2 - radius)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Dessiner des formes géométriques")

# Créer un canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Dessiner un rectangle arrondi
create_rounded_rectangle(canvas, 50, 50, 200, 100, radius=20)

# Dessiner un demi-disque plein
canvas.create_arc(250, 50, 350, 150, start=0, extent=180, fill="red")

# Dessiner un disque plein
canvas.create_oval(250, 250, 350, 350, fill="green")

# Lancer la boucle principale
root.mainloop()
