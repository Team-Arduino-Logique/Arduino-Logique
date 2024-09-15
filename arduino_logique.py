"""
ArduinoLogique.py
This module provides a graphical interface for simulating logic circuits using Tkinter.
It includes functionality to initialize a canvas, draw a breadboard, and zoom in and out
on the circuit diagram.
Functions:
    zoom(p_canvas: tk.Canvas, p_scale: float, x_board: int, y_board: int) -> None

"""

import tkinter as tk
from tkinter import font
import breadboard as board


def zoom(p_canvas: tk.Canvas, p_scale: float, p_board_x: int, p_board_y: int) -> None:
    """
    Adjusts the zoom level of the given canvas by scaling the board and redrawing it.
    Parameters:
    p_canvas (tk.Canvas): The canvas on which the board is drawn.
    p_scale (float): The scale factor to apply to the board.
    p_board_x (int): The x-coordinate of the board's position.
    p_board_y (int): The y-coordinate of the board's position.
    Returns:
    None
    """
    p_canvas.delete("all")
    board.init(p_canvas)
    board.fillMatrix1260pts()
    board.circuit(p_canvas, p_board_x, p_board_y, scale=int(p_scale) / 10.0, model=board.circuitTest)


if __name__ == "__main__":
    # Create main window
    win = tk.Tk()
    win.title("Laboratoire virtuel de circuit logique - GIF-1002")

    # Create the canvas (surface to draw on)
    canvas = tk.Canvas(win, width=1500, height=900)
    canvas.pack()

    board_x, board_y = 50, 10

    board.init(canvas)
    board.fillMatrix1260pts()

    new_cable = [
        (
            board.drawWire,
            1,
            {
                "id": "pwire_1",
                "color": (255, 0, 0, 255),
                "mode": board.AUTO,
                "coords": [(1, 5, 3, 2)],
                "matrice": board.matrix1260pts,
            },
        )
    ]
    move_pkg = [(board.drawChip, 1, {"id": "_chip_5", "XY": (500, 161.5)})]
    SCALE = 10.0
    zoom(canvas, SCALE, board_x, board_y)

    h_slider = tk.Scale(win, from_=10, to=30, orient="horizontal", command=zoom)
    h_slider.pack(fill="x", padx=10, pady=10)

    firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=15)

    win.mainloop()
