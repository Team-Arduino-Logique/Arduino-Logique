import tkinter as tk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Curseur Personnalisé avec tkinter et XBM")

# Définir les chemins des fichiers XBM
cursor_xbm = "Icones/CleAnglaise_32.xbm"
mask_xbm = "Icones/CleAnglaise_32_mask.xbm"

# Configurer le curseur personnalisé pour la fenêtre principale
root.config(cursor="@{},{}".format(cursor_xbm, mask_xbm))

# Créer un widget Canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Ajouter du contenu au canevas (optionnel)
canvas.create_text(400, 300, text="Curseur personnalisé en action", font=("Arial", 24))

# Lancer l'application
root.mainloop()
