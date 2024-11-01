import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

def ouvrir():
    messagebox.showinfo("Ouvrir", "Ouvrir le fichier sélectionné.")

def renommer():
    messagebox.showinfo("Renommer", "Renommer le fichier sélectionné.")

def supprimer():
    messagebox.showinfo("Supprimer", "Placer dans la corbeille.")

def etiquetter(couleur):
    messagebox.showinfo("Étiquette", f"Étiquette {couleur} appliquée.")

def afficher_menu(event):
    """Affiche le menu contextuel à la position du clic."""
    menu.post(event.x_root, event.y_root)

def creer_image_cercle(couleur, taille=20):
    """Crée une image en mémoire avec un cercle coloré."""
    image = Image.new("RGBA", (taille, taille), (0, 0, 0, 0))  # Image transparente
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, taille, taille), fill=couleur)  # Dessine un cercle
    return ImageTk.PhotoImage(image)

# Fenêtre principale
root = tk.Tk()
root.geometry("300x200")
root.title("Menu Contextuel avec Formes")

# Créer un menu contextuel
menu = tk.Menu(root, tearoff=0)

# Ajouter les options au menu avec des icônes (formes)
menu.add_command(label="Ouvrir", command=ouvrir)
menu.add_command(label="Renommer", command=renommer)
menu.add_separator()
menu.add_command(label="Placer dans la corbeille", command=supprimer)

# Sous-menu avec des couleurs et formes associées
sous_menu = tk.Menu(menu, tearoff=0)

# Couleurs et icônes associées
couleurs = {
    "Rouge": "#FF0000",
    "Orange": "#FFA500",
    "Jaune": "#FFFF00",
    "Vert": "#00FF00",
    "Bleu": "#0000FF",
    "Violet": "#800080",
    "Gris": "#808080"
}

# Créer des icônes circulaires pour chaque couleur
icones = {}
for couleur, code in couleurs.items():
    icones[couleur] = creer_image_cercle(code)  # Générer l'image du cercle
    sous_menu.add_command(
        label=couleur, 
        image=icones[couleur], 
        compound=tk.LEFT,  # Affiche l'icône à gauche du texte
        command=lambda c=couleur: etiquetter(c)
    )

# Ajouter le sous-menu au menu principal
menu.add_cascade(label="Étiquettes", menu=sous_menu)

# Lier un clic droit pour afficher le menu
root.bind("<Button-3>", afficher_menu)  # Clic droit sur Windows/Linux/macOS
root.bind("<Control-Button-1>", afficher_menu)  # Clic gauche + Ctrl sur macOS

# Boucle principale
root.mainloop()
