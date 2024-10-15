import tkinter as tk

def onReturnBack(event):
    # Empêche la suppression du prompt
    if terminal.index(tk.INSERT) == prompt_index:
        return "break"  # Empêche la suppression du prompt
    
def onUpDown(event):
    return "break"

def on_return(event):
    global prompt_index
    # Récupérer la commande tapée par l'utilisateur (le texte après le prompt)
    command = terminal.get(prompt_index, tk.END).strip()

    # Afficher la commande saisie et un nouveau prompt sur une nouvelle ligne
    terminal.insert(tk.END, f"\n> ")
    
    # Mettre à jour l'index du prompt
    
    prompt_index = terminal.index(tk.INSERT)

    return "break"  # Empêche l'ajout automatique d'un saut de ligne par défaut

# Créer la fenêtre principale
win = tk.Tk()
win.title("Terminal avec Prompt")

# Créer un widget Text
terminal = tk.Text(win, height=15, width=80, font=("Courier", 14))
terminal.pack()

# Ajouter le premier prompt
terminal.insert(tk.END, "> ")
prompt_index = terminal.index(tk.INSERT)  # Sauvegarder l'index du prompt

# Empêcher l'effacement du prompt en bloquant la touche Backspace
#terminal.bind("<Key>", on_key)

terminal.bind("<Left>", onReturnBack)
terminal.bind("<BackSpace>", onReturnBack)

terminal.bind("<Up>", onUpDown)
terminal.bind("<Down>", onUpDown)

# Ajouter la gestion de la touche Entrée pour traiter les commandes
terminal.bind("<Return>", on_return)

# Mettre le focus sur le widget Text pour saisir directement
terminal.focus()

win.mainloop()
