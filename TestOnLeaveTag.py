import tkinter as tk

def on_leave(event):
    # Action à réaliser quand la souris quitte la zone du carré
    print("La souris a quitté la zone des carrés!")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Carré imbriqué avec onLeave global")

# Création du canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Création du carré extérieur
outer_square = canvas.create_rectangle(50, 50, 200, 200, outline="blue",fill="blue", tags="square_tag")

# Création du carré intérieur
inner_square = canvas.create_rectangle(100, 100, 150, 150, outline="green",fill="green", tags="square_tag")

# Liaison de l'événement "onLeave" au tag commun
canvas.tag_bind("square_tag", "<Leave>", on_leave)

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
