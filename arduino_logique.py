"""
ArduinoLogique.py
Main module for the ArduinoLogique program. This module provides a graphical interface for 
simulating logic circuits using Tkinter. It includes functionality to initialize a canvas, 
draw a breadboard, and zoom in and out on the circuit diagram.
Functions:
    zoom(p_canvas: tk.Canvas, p_scale: float, x_board: int, y_board: int) -> None

"""

import tkinter as tk
from tkinter import font
from breadboard import Breadboard
from component_sketch import ComponentSketcher
from dataComponent import ComponentData
from dataCDLT import current_dict_circuit

def zoom(
    p_canvas: tk.Canvas, p_scale: float, p_board: Breadboard, p_board_x: int, p_board_y: int, p_model: list
) -> None:
    """
    Adjusts the zoom level of the given canvas by scaling the board and redrawing it.
    Parameters:
    p_canvas (tk.Canvas): The canvas on which the board is drawn.
    p_scale (float): The scale factor to apply to the board.
    p_board_x (int): The x-coordinate of the board's position.
    p_board_y (int): The y-coordinate of the board's position.
    p_model (list): The model data for the circuit.
    Returns:
    None
    """
    p_canvas.delete("all")
    p_board = Breadboard(p_canvas)
    p_board.fill_matrix_1260_pts()
    p_board.circuit(p_board_x, p_board_y, scale=int(p_scale) / 10.0, model=p_model)

if __name__ == "__main__":
    # Create main window
    win = tk.Tk()
    win.title("Laboratoire virtuel de circuit logique - GIF-1002")

    # Create the canvas (surface to draw on)
    canvas = tk.Canvas(win, width=1500, height=900)
    canvas.pack()

    board = Breadboard(canvas)
    board.fill_matrix_1260_pts()

    component_data = ComponentData(ComponentSketcher(canvas))
    model = component_data.circuitTest
    zoom(canvas, 10.0, board, 50, 10, model)

    # **Wait for the components to be drawn by processing events**
    win.update_idletasks()

    # Print current_dict_circuit to (je debug ici)
    print("Current Circuit Components:")
    for comp_id, comp_data in current_dict_circuit.items():
        print(f"ID: {comp_id}, Position: {comp_data.get('XY')}")

    # essai de mouvement

    chip_id = "_chip_1"

    if chip_id in current_dict_circuit:
        new_x, new_y = 200, 150

        current_x, current_y = current_dict_circuit[chip_id]["XY"]

        # Calculate the difference
        dx = new_x - current_x
        dy = new_y - current_y

        for tag in current_dict_circuit[chip_id]["tags"]:
            canvas.move(tag, dx, dy)

        current_dict_circuit[chip_id]["XY"] = (new_x, new_y)

        print(f"Moved chip {chip_id} to new position: ({new_x}, {new_y})")
    else:
        print(f"Chip ID {chip_id} not found in current_dict_circuit.")

    # Create a slider or other UI elements as needed
    h_slider = tk.Scale(
        win,
        from_=10,
        to=30,
        orient="horizontal",
        command=lambda scale: zoom(canvas, float(scale), board, 50, 10, model),
    )
    h_slider.pack(fill="x", padx=10, pady=10)

    firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=15)

    win.mainloop()
