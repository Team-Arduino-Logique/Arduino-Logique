"""
ArduinoLogique.py
Main module for the ArduinoLogique program. This module provides a graphical interface for 
simulating logic circuits using Tkinter. It includes functionality to initialize a canvas, 
draw a breadboard, etc.
"""

from pathlib import Path
import tkinter as tk
from tkinter import font
from breadboard import Breadboard
from component_sketch import ComponentSketcher
from menus import Menus
from sidebar import Sidebar
from toolbar import Toolbar
from utils import resource_path


def main():
    """
    Main function for the ArduinoLogique program. This function initializes the main window,
    creates the canvas, toolbar, sidebar, and menus, and draws the initial circuit diagram.
    """
    # Creating main window
    win = tk.Tk()
    win.title("Laboratoire virtuel de circuit logique - GIF-1002")
    win.geometry("1700x800")  # Initial window size
    win.resizable(False, False)  # Disabling window resizing
    win.configure(bg="#333333")  # Setting consistent background color

    # Configuring grid layout for the main window
    win.grid_rowconfigure(0, weight=0)  # Menu bar
    win.grid_rowconfigure(1, weight=0)  # Secondary toolbar
    win.grid_rowconfigure(2, weight=1)  # Canvas and sidebar
    win.grid_rowconfigure(3, weight=0)  # Slider
    win.grid_columnconfigure(0, weight=0)  # Sidebar
    win.grid_columnconfigure(1, weight=1)  # Canvas

    # Creating the canvas in row=2, column=1
    canvas = tk.Canvas(win, bg="#626262", highlightthickness=0, bd=0)
    canvas.grid(row=2, column=1, sticky="nsew")

    # Create a single instance of ComponentSketcher
    sketcher = ComponentSketcher(canvas)
    sketcher.id_origins["xyOrigin"] = (50, 10)
    # Initializing the breadboard and components
    board = Breadboard(canvas, sketcher)
    board.fill_matrix_1260_pts()

    # Creating the toolbar instance
    toolbar = Toolbar(parent=win, canvas=canvas, sketcher=sketcher, current_dict_circuit=sketcher.current_dict_circuit)
    # Placing the secondary top bar in row=1, column=1 (spanning only the canvas area)
    toolbar.topbar_frame.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 0))

    # Set initial scale factor
    initial_scale = 1.0  # Equivalent to 10.0 / 10.0
    sketcher.scale_factor = initial_scale

    # Draw the circuit
    board.draw_blank_board_model(50, 10)

    # Creating the Sidebar instance after canvas, board, sketcher, component_data are defined
    sidebar = Sidebar(
        parent=win,
        chip_images_path=Path(resource_path("Assets/chips")).resolve(),
        canvas=canvas,
        sketcher=sketcher,
        current_dict_circuit=sketcher.current_dict_circuit,
        toolbar=toolbar,
    )

    def refresh_sidebar():
        sidebar.refresh()
        win.after(5000, refresh_sidebar)

    # Start the periodic refresh
    refresh_sidebar()

    # Creating the Menus instance with proper references
    menus = Menus(
        parent=win,
        canvas=canvas,
        board=board,
        current_dict_circuit=sketcher.current_dict_circuit,
    )
    # Placing the menu_bar in row=0, spanning both columns
    menus.menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Setting default font for all widgets
    default_font = font.Font(family="Arial", size=10)
    win.option_add("*Font", default_font)

    # board.draw_matrix_points(scale=1) # for debugging purposes

    win.mainloop()


if __name__ == "__main__":
    main()
