import tkinter as tk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Text widget sur Canvas")

# Créer un Canvas
canvas = tk.Canvas(root, width=400, height=300, bg="lightgray")
canvas.pack()

# Créer un widget Text
text_widget = tk.Text(root, height=5, width=30)

# Placer le Text sur le Canvas à la position (50, 50)
canvas.create_window(100, 100, window=text_widget)

# Insérer du texte dans le widget Text
text_widget.insert("1.0", "Ceci est un widget Text sur un Canvas.")

# Lancer la boucle Tkinter
root.mainloop()
