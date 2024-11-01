import tkinter as tk

def dessiner_segment(canvas, x1, y1, x2, y2, couleur="#000000", epaisseur=4):
    """Dessine un segment de droite entre deux points."""
    canvas.create_line(x1, y1, x2, y2, fill=couleur, width=epaisseur)

def dessiner_inflexion(canvas, x, y, rayon, couleur="#000000", epaisseur=4):
    """Dessine un arc arrondi à l'inflexion."""
    canvas.create_oval(
        x - rayon, y - rayon, x + rayon, y + rayon,
        outline=couleur, width=epaisseur
    )

def dessiner_cable(canvas, points, rayon=10, couleur="#0d6efd", epaisseur=4):
    """
    Dessine un câble avec des segments droits et des inflexions arrondies.
    
    Parameters:
    - canvas (tk.Canvas): Le canvas où dessiner.
    - points (list): Liste des points (x, y) formant le câble.
    - rayon (int): Rayon des inflexions arrondies.
    - couleur (str): Couleur du câble.
    - epaisseur (int): Épaisseur du câble.
    """
    # Dessiner les segments de droite
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        dessiner_segment(canvas, x1, y1, x2, y2, couleur, epaisseur)

    # Dessiner les inflexions arrondies aux points d'intersection
    for i in range(1, len(points) - 1):
        x, y = points[i]
        dessiner_inflexion(canvas, x, y, rayon, couleur, epaisseur)

# Créer la fenêtre principale
root = tk.Tk()
root.geometry("600x400")
root.title("Câble avec Inflexions Arrondies")

# Créer un canvas pour dessiner
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Liste des points formant le câble
points = [
    (50, 300),  # Point de départ
    (150, 200),  # Inflexion 1
    (300, 250),  # Inflexion 2
    (450, 150),  # Inflexion 3
    (550, 300)   # Point final
]

# Dessiner le câble avec segments et inflexions arrondies
dessiner_cable(canvas, points, rayon=10, couleur="#0d6efd", epaisseur=4)

# Lancer la boucle principale
root.mainloop()
