import tkinter as tk

def suivre_fenetre_principale(event):
    # Récupère les coordonnées de la fenêtre principale
    x = fenetre_principale.winfo_x()
    y = fenetre_principale.winfo_y()
    
    # Met à jour la position de la deuxième fenêtre (10 pixels en dessous de la première)
    fenetre_secondaire.geometry(f"+{x}+{y + fenetre_principale.winfo_height() + 10}")

# Créer la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("Fenêtre principale")
fenetre_principale.geometry("300x200+100+100")

# Créer la deuxième fenêtre
fenetre_secondaire = tk.Toplevel()
fenetre_secondaire.title("Fenêtre secondaire")
fenetre_secondaire.geometry("300x200+100+310")  # Position 10 pixels sous la fenêtre principale

# Ajouter un label dans chaque fenêtre
label1 = tk.Label(fenetre_principale, text="Fenêtre principale")
label1.pack(pady=20)

label2 = tk.Label(fenetre_secondaire, text="Fenêtre secondaire")
label2.pack(pady=20)

# Lier l'événement de déplacement/redimensionnement de la fenêtre principale
fenetre_principale.bind("<Configure>", suivre_fenetre_principale)

# Lancer la boucle principale de l'application
fenetre_principale.mainloop()
