import tkinter as tk
from tkinter import messagebox

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

# Création de la fenêtre principale
root = tk.Tk()
root.geometry("300x200")
root.title("Menu Contextuel")

# Création du menu contextuel
menu = tk.Menu(root, tearoff=0)

# Ajout des options au menu
menu.add_command(label="Ouvrir", command=ouvrir)
menu.add_command(label="Renommer", command=renommer)
menu.add_separator()
menu.add_command(label="Placer dans la corbeille", command=supprimer)

# Sous-menu pour les étiquettes de couleur
sous_menu = tk.Menu(menu, tearoff=0)
couleurs = ["Rouge", "Orange", "Jaune", "Vert", "Bleu", "Violet", "Gris"]
for couleur in couleurs:
    sous_menu.add_command(label=couleur, command=lambda c=couleur: etiquetter(c))

menu.add_cascade(label="Étiquettes", menu=sous_menu)

# Lier un clic droit à l'apparition du menu contextuel
root.bind("<Button-3>", afficher_menu)  # Clic droit sur Windows/macOS
root.bind("<Control-Button-1>", afficher_menu)  # Clic gauche + Ctrl sur macOS

# Boucle principale
root.mainloop()
