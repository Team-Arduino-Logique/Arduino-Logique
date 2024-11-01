import tkinter as tk
from tkinter import colorchooser

class MyApp:
    def __init__(self, root):
        self.icon_size = 20  # Taille de l'icône du bouton
        self.selected_color = "#ff0000"  # Couleur par défaut
        self.create_color_chooser(root)

    def choose_color(self):
        """Ouvre une boîte de dialogue pour choisir une couleur."""
        color_code = colorchooser.askcolor(title="Choisissez une couleur")
        if color_code[1]:  # Si une couleur est choisie
            self.selected_color = color_code[1]
            self.color_button.config(bg=self.selected_color)

    def create_color_chooser(self, parent_frame):
        """Crée un bouton pour choisir une couleur."""
        square_size = self.icon_size

        # Configurer le bouton avec une taille explicite en pixels (via `Canvas`)
        self.color_button = tk.Button(
            parent_frame,
            text="  ",  # Ajout d'un espace pour mieux gérer la taille sur macOS
            bg=self.selected_color,
            relief="raised",
            bd=1,
            command=self.choose_color
        )
        self.color_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Forcer la mise à jour du style pour macOS
        self.color_button.update_idletasks()

# Créer la fenêtre principale
root = tk.Tk()
app = MyApp(root)
root.mainloop()
