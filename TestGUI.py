import tkinter as tk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Dessiner des formes géométriques")

def on_button1_click():
    print("Button 1 clicked")
    
def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    canvas.create_polygon(points, **kwargs, smooth=True)

    # Draw four arcs for corners
    canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, style=tk.ARC, **kwargs)
    canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, style=tk.ARC, **kwargs)
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, style=tk.ARC, **kwargs)
    canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, style=tk.ARC, **kwargs)


# Créer un canvas
canvas = tk.Canvas(root, width=1200, height=800)
canvas.pack()

# Dessiner un rectangle
#canvas.create_rectangle(50, 50, 1050, 350, fill="#F5F5DC")
draw_rounded_rectangle(canvas, 50, 50, 1050, 350, 15, outline="#F5F5DC", fill="#F5F5DC")

button1 = tk.Button(root, text="Button 1", command=on_button1_click)
button1.pack(pady=10)
interSpace = 15
space= 9
xD, yD=100, 100
for y in range(10):
    if y == 5: yD+=2*interSpace+2*space//3
    for x in range(63):
        # Dessiner un demi-disque plein
        #canvas.create_arc(100+x*24, 100, 112+x*24, 112, start=0, extent=180, fill="#c0c0c0", outline="#c0c0c0")
        #canvas.create_arc(100+x*24, 100, 112+x*24, 112, start=180, extent=0, fill="#e6e6e6", outline="#e6e6e6")

        canvas.create_polygon(xD+x*interSpace, yD+space+y*interSpace, xD+x*interSpace, yD+y*interSpace, xD+space+x*interSpace, yD+y*interSpace, fill='#c0c0c0', outline='#c0c0c0')
        canvas.create_polygon(xD+x*interSpace, yD+space+y*interSpace, xD+space+x*interSpace, yD+space+y*interSpace, xD+space+x*interSpace, yD+y*interSpace, fill='#f6f6f6', outline='#f6f6f6')
        canvas.create_rectangle(xD+space//3+x*interSpace, yD+space//3+y*interSpace, xD+2*space//3+x*interSpace,yD+2*space//3+y*interSpace,fill="#484848",outline="#484848")

    # Dessiner un disque plein
    #canvas.create_oval(104+x*24, 104, 108+x*24, 108, fill="#484848", outline="#484848")

#canvas.create_line(10,10,400,10)

# Lancer la boucle principale
root.mainloop()
