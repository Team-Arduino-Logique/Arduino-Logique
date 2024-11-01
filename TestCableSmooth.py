import tkinter as tk

def dessiner_cable(canvas, points, couleur="#0d6efd", contour="#000000", epaisseur=4):
    """
    Dessine un câble courbé avec un contour.
    
    Parameters:
    - canvas (tk.Canvas): Le canvas où dessiner.
    - points (list): Liste des points (x, y) formant la ligne.
    - couleur (str): Couleur principale du câble.
    - contour (str): Couleur du contour.
    - epaisseur (int): Épaisseur de la ligne principale.
    """
    # Dessiner le "contour" (ligne plus épaisse)
    canvas.create_line(points, fill=contour, width=epaisseur + 2)

    # Dessiner la ligne principale par-dessus
    canvas.create_line(points, fill=couleur, width=epaisseur) # , splinesteps=2

# Créer la fenêtre principale
root = tk.Tk()
root.geometry("600x400")
root.title("Câble Courbé avec Contour")

# Créer un canvas pour dessiner
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Définir des points pour le câble courbé
points = [
    50, 200,   # Point de départ
    250, 480,  # Point intermédiaire 1
    300, 120,  # Point intermédiaire 2
    550, 120  # Point intermédiaire 3
    #550, 200   # Point final
]

# Dessiner le câble courbé avec contour
dessiner_cable(canvas, points, couleur="#0d6efd", contour="#000000", epaisseur=4)

# Lancer la boucle principale
root.mainloop()
