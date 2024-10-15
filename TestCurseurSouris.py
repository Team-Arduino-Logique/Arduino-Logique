import tkinter as tk

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Curseur personnalisé")

# Création du canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Définir un curseur personnalisé
custom_cursor = "@custom_cursor.xbm white black"
canvas.config(cursor=custom_cursor)

# Boucle principale de l'interface Tkinter
root.mainloop()
