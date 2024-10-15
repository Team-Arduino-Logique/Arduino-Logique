import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def create_glass_effect_rectangle(canvas, x1, y1, x2, y2, color, alpha):
    """
    Create a rectangle with a glass effect using PIL and Tkinter.
    :param canvas: The canvas to draw on.
    :param x1: The x-coordinate of the top-left corner.
    :param y1: The y-coordinate of the top-left corner.
    :param x2: The x-coordinate of the bottom-right corner.
    :param y2: The y-coordinate of the bottom-right corner.
    :param color: The base color of the rectangle.
    :param alpha: The alpha level (0.0 to 1.0) for transparency.
    """
    width = x2 - x1
    height = y2 - y1

    # Create an image with transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the rectangle with the specified color and transparency
    r, g, b = canvas.winfo_rgb(color)
    r, g, b = r // 256, g // 256, b // 256
    for i in range(100):
        alpha_step = int(alpha * (i / 100) * 255)
        color_step = (r, g, b, alpha_step)
        draw.rectangle([0, i * height // 100, width, (i + 1) * height // 100], fill=color_step)

    # Convert to Tkinter-compatible image
    tk_image = ImageTk.PhotoImage(image)
    
    # Create a label to hold the image and place it on the canvas
    label = tk.Label(canvas, image=tk_image, borderwidth=0)
    label.image = tk_image
    label.place(x=x1, y=y1)

# Create the main window
root = tk.Tk()
root.title("Transparent Glass Effect Rectangle")

# Create a Canvas widget
canvas = tk.Canvas(root, width=400, height=400,bg="red")
canvas.pack()

# Create a rectangle with a glass effect
create_glass_effect_rectangle(canvas, 50, 50, 350, 350, 'blue', 0.3)

# Run the Tkinter main loop
root.mainloop()
