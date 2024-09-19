import tkinter as tk
from tkinter import font
from breadboard import Breadboard
from component_sketch import ComponentSketcher
from dataComponent import ComponentData


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


def on_mouse_wheel(event, p_canvas: tk.Canvas, p_board: Breadboard, p_board_x: int, p_board_y: int, p_model: list):
    """
    Handles zooming using the mouse scroll wheel.
    Parameters:
    event (tk.Event): The mouse wheel event.
    p_canvas (tk.Canvas): The canvas on which the board is drawn.
    p_board (Breadboard): The breadboard object to be redrawn.
    p_board_x (int): The x-coordinate of the board's position.
    p_board_y (int): The y-coordinate of the board's position.
    p_model (list): The model data for the circuit.
    """
    scale = 10.0  # Default zoom scale
    if event.delta > 0:  # Scroll up
        scale += 1.0
    else:  # Scroll down
        scale -= 1.0
    zoom(p_canvas, scale, p_board, p_board_x, p_board_y, p_model)


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

    # Add mouse wheel zoom event
    canvas.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas, board, 50, 10, model))

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
