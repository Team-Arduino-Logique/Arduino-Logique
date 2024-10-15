import tkinter as tk
import platform

root = tk.Tk()

# Vérifier le nom de la plateforme
print(f"Plateforme : {platform.system()}")

# Vérifier l'option du display en cas de backend X11
display_info = root.tk.call('tk', 'windowingsystem')
print(f"Système de fenêtre Tkinter : {display_info}")

print(f"Tcl version : {root.tk.call('info', 'patchlevel')}")

root.destroy()
