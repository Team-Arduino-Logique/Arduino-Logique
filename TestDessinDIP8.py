import tkinter as tk

def draw_dip8_chip(canvas, x, y, width, height):
    # Dessiner le corps de la puce
    chip_color = "#3e3e3e"  # Couleur gris métallisé
    canvas.create_rectangle(x, y, x + width, y + height, fill=chip_color, outline="black")
    
    # Dessiner les pattes de la puce
    pin_color = "#c0c0c0"  # Couleur argentée
    pin_width = 5
    pin_height = 20
    pin_spacing = (width - 8 * pin_width) / 7
    
    # Pattes du haut
    for i in range(4):
        pin_x = x + i * (pin_width + pin_spacing)
        canvas.create_rectangle(pin_x, y - pin_height, pin_x + pin_width, y, fill=pin_color, outline="black")
    
    # Pattes du bas
    for i in range(4):
        pin_x = x + i * (pin_width + pin_spacing)
        canvas.create_rectangle(pin_x, y + height, pin_x + pin_width, y + height + pin_height, fill=pin_color, outline="black")
    
    # Dessiner le repère de pin 1
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="white", outline="black")

def main():
    root = tk.Tk()
    root.title("DIP8 Chip Drawing")
    
    canvas = tk.Canvas(root, width=400, height=200, bg="white")
    canvas.pack()
    
    draw_dip8_chip(canvas, 150, 70, 100, 50)
    
    root.mainloop()

if __name__ == "__main__":
    main()
