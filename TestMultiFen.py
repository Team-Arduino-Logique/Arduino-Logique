import tkinter as tk
from tkinter import Toplevel

def ouvrir_nouvelle_fenetre():
    global nouvelle_fenetre
    
    # Crée une nouvelle fenêtre
    nouvelle_fenetre = Toplevel()
    nouvelle_fenetre.title("Nouvelle fenêtre")
    
    # Ajouter un label dans la nouvelle fenêtre
    label = tk.Label(nouvelle_fenetre, text="Ceci est une nouvelle fenêtre")
    label.pack(pady=20)
    
    # Définir un événement quand cette fenêtre prend le focus
    nouvelle_fenetre.bind("<FocusIn>", lambda event: fenetre_principale.lift())

# Créer la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("Fenêtre principale")

# Ajouter un bouton pour ouvrir une nouvelle fenêtre
bouton = tk.Button(fenetre_principale, text="Ouvrir une nouvelle fenêtre", command=ouvrir_nouvelle_fenetre)
bouton.pack(pady=20)

# Définir un événement quand la fenêtre principale prend le focus
fenetre_principale.bind("<FocusIn>", lambda event: nouvelle_fenetre.lift())
#fenetre_principale.bind("<FocusOut>", lambda event: fenetre_principale.after(100, lambda: fenetre_principale.tk.call('wm', 'attributes', fenetre_principale._w, '-topmost', '0')))

# Lancer la boucle principale de l'application
fenetre_principale.mainloop()
