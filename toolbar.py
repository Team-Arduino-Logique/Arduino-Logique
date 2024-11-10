"""
toolbar.py
This module defines the Toolbar class, which provides a graphical toolbar for an application using the Tkinter library.
The toolbar includes buttons for various actions (e.g., Connection, Power, Input, Output, Delete) and a color chooser
for selecting connection colors. The Toolbar class manages the state and behavior of these buttons and handles user
interactions for placing wires and pin_ios on a canvas.
"""

from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, colorchooser
import os
from component_sketch import ComponentSketcher
from dataCDLT import matrix1260pts, id_origins, INPUT, OUTPUT, FREE


@dataclass
class WirePlacementInfo:
    """
    A dataclass to store information about a wire being placed on the canvas.
    Attributes:
    - wire_id (int): The unique identifier for the wire.
    - start_point (tuple[int, int]): The starting point of the wire.
    - start_col_line (tuple[int, int]): The starting column and line of the wire.
    """

    wire_id: int
    start_point: tuple[int, int] | None
    start_col_line: tuple[int, int] | None


class Toolbar:
    """
    A class to create and manage a toolbar for an application.
    Attributes:

    """

    ICON_SIZE = 24

    def __init__(self, parent: tk.Tk, canvas: tk.Canvas, sketcher: ComponentSketcher, current_dict_circuit) -> None:
        self.canvas = canvas
        self.sketcher = sketcher
        self.current_dict_circuit = current_dict_circuit
        self.selected_color = "#479dff"
        self.buttons: dict[str, tk.Button] = {}
        self.tool_mode = None
        self.wire_info: WirePlacementInfo = WirePlacementInfo(0, None, None)
        self.cursor_indicator_id = None
        self.create_topbar(parent)
        self.canvas.bind("<Motion>", self.canvas_follow_mouse, add="+")
        self.canvas.bind("<Button-1>", self.canvas_click, add="+")
        self.canvas.bind("<Button-3>", self.cancel_placement, add="+")

    def create_topbar(self, parent: tk.Tk):
        """
        Creates the secondary top bar with specified buttons and a color chooser.
        """
        # Create the top bar frame
        self.topbar_frame = tk.Frame(parent, bg="#505050", height=40, bd=0, highlightthickness=0)

        # Create left and right subframes
        left_frame = tk.Frame(self.topbar_frame, bg="#505050")
        left_frame.pack(side=tk.LEFT, padx=5, pady=5)

        right_frame = tk.Frame(self.topbar_frame, bg="#505050")
        right_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        # Load images
        images = self.load_images()

        # Create buttons in the left frame
        self.create_button("Connection", left_frame, images)
        self.create_button("Power", left_frame, images)
        self.create_button("Input", left_frame, images)
        self.create_button("Output", left_frame, images)

        # Create the color chooser and Delete button in the right frame
        self.color_button = tk.Button(
            right_frame,
            bg=self.selected_color,
            width=2,
            height=1,
            relief="raised",
            bd=1,
            command=self.choose_color,
        )
        self.color_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.create_button("Delete", right_frame, images)

    def load_images(self) -> dict[str, tk.PhotoImage | None]:
        """
        Loads PNG images from the 'icons' folder, scales them, and stores them in the images dictionary.
        """
        icon_names = ["connection", "power", "input", "output", "delete"]
        icons_folder = Path("assets/icons").resolve()
        images: dict[str, tk.PhotoImage | None] = {}
        for name in icon_names:
            path = os.path.join(icons_folder, f"{name}.png")
            try:
                image = tk.PhotoImage(file=path)
                # Calculate the scaling factor based on original image size and desired icon_size
                original_width = image.width()
                original_height = image.height()
                scale_factor = max(original_width, original_height) // Toolbar.ICON_SIZE
                if scale_factor > 1:
                    image = image.subsample(scale_factor, scale_factor)
                images[name] = image
            except tk.TclError:
                messagebox.showerror(
                    "Image Load Error", f"Failed to load {path}. Ensure the file exists and is a valid PNG image."
                )
                images[name] = None  # Fallback if image fails to load

        return images

    def create_button(self, action: str, parent_frame: tk.Frame, images: dict[str, tk.PhotoImage | None]) -> None:
        """
        Helper method to create a button in the specified frame with an icon.

        Parameters:
        - action (str): The action name corresponding to the button.
        - parent_frame (tk.Frame): The frame to place the button in.
        """
        image = images.get(action.lower())
        if image:
            btn = tk.Button(
                parent_frame,
                image=image,
                bg="#505050",  # Inactive background
                activebackground="#707070",  # Active background (temporary visual on click)
                relief="flat",
                command=lambda: self.button_action(action),
                padx=2,
                pady=2,
            )
            # Keep a reference to prevent garbage collection
            btn.image = image  # type: ignore
        else:
            # Fallback button with text if image is not available
            btn = tk.Button(
                parent_frame,
                text=action,
                bg="#505050",  # Inactive background
                fg="white",
                activebackground="#707070",  # Active background
                activeforeground="white",
                font=("Arial", 9, "bold"),
                relief="flat",
                command=lambda: self.button_action(action),
                padx=2,
                pady=2,
            )
        btn.pack(side=tk.LEFT, padx=10, pady=2)  # Minimal spacing between buttons
        self.buttons[action] = btn  # Store button reference

    def choose_color(self):
        """
        Opens a color chooser dialog to select a connection color.
        """
        color_code = colorchooser.askcolor(title="Choose Connection Color", initialcolor=self.selected_color)
        if color_code[1]:
            self.selected_color = color_code[1]
            self.color_button.configure(bg=self.selected_color)
            if self.cursor_indicator_id:
                self.canvas.itemconfig(self.cursor_indicator_id, fill=self.selected_color)
            # Here y_originu can add logic to apply the selected color to new connections

    def button_action(self, action_name):
        """
        Defines the action to perform when a button is clicked.
        """
        # If there's an active button that's not the one clicked, deactivate it
        if self.tool_mode and self.tool_mode != action_name:
            self.deactivate_button(self.tool_mode)
            self.deactivate_mode(self.tool_mode)

        # Toggle the clicked button's active state
        if self.tool_mode == action_name:
            # If already active, deactivate it
            self.deactivate_button(action_name)
            self.tool_mode = None
            self.deactivate_mode(action_name)
        else:
            # Activate the clicked button
            self.activate_button(action_name)
            self.tool_mode = action_name
            self.activate_mode(action_name)

    def activate_button(self, action_name):
        """
        Activates the specified button by changing its background color.
        """
        btn = self.buttons.get(action_name)
        if btn:
            btn.configure(bg="#707070")  # Active background color

    def deactivate_button(self, action_name):
        """
        Deactivates the specified button by resetting its background color.
        """
        btn = self.buttons.get(action_name)
        if btn:
            btn.configure(bg="#505050")  # Inactive background color

    def activate_mode(self, action_name):
        """
        Activates the mode associated with the action_name.
        """
        # Deactivate other modes
        self.deactivate_mode("all")
        self.tool_mode = action_name
        if self.cursor_indicator_id is None:
            self.create_cursor_indicator(action_name)

        if action_name == "Connection":
            self.wire_info.start_point = None
            self.wire_info.start_col_line = None
        elif action_name == "Delete":
            self.sketcher.delete_mode_active = True

    def deactivate_mode(self, action_name):
        """
        Deactivates the mode associated with the action_name.
        """
        self.tool_mode = None
        self.canvas.config(cursor="")
        self.remove_cursor_indicator()

        if action_name in ("Connection", "all"):
            self.wire_info.start_point = None
            self.wire_info.start_col_line = None
            self.canvas.delete("wire_temp_circle")
        elif action_name in ("Delete", "all"):
            self.sketcher.delete_mode_active = False

    def create_cursor_indicator(self, action_name=None):
        """
        Creates a cursor indicator that follows the mouse position.
        """
        if action_name == "Delete":
            self.canvas.config(cursor="X_cursor")
        elif self.cursor_indicator_id is None:
            color = self.selected_color
            self.cursor_indicator_id = self.canvas.create_oval(0, 0, 10, 10, fill=color, outline="#000000")
            self.canvas.tag_raise(self.cursor_indicator_id)

    def remove_cursor_indicator(self):
        """
        Removes the cursor-following indicator.
        """
        if self.cursor_indicator_id is not None:
            self.canvas.delete(self.cursor_indicator_id)
            self.cursor_indicator_id = None  # Set back to None instead of deleting

    def canvas_follow_mouse(self, event):
        """
        Moves the cursor-following indicator to the mouse position.
        """
        if (self.tool_mode is None) or self.cursor_indicator_id is None:
            return
        x, y = event.x, event.y
        x_min, y_min = id_origins["xyOrigin"]
        x_max, y_max = id_origins["bottomLimit"]
        if x_min < x < x_max and y_min < y < y_max:
            (x, y), (col, line) = self.sketcher.find_nearest_grid_point(x, y, matrix1260pts)
            if (
                self.tool_mode == "Connection"
                and self.wire_info.start_point
                and matrix1260pts[f"{col},{line}"]["state"] == FREE
            ):

                coord = self.current_dict_circuit[self.wire_info.wire_id]["coord"]
                matrix1260pts[f"{coord[0][2]},{coord[0][3]}"]["state"] = FREE
                color = self.hex_to_rgb(self.selected_color)
                coord = [(coord[0][0], coord[0][1], col, line)]
                model_wire = [
                    (
                        self.sketcher.draw_wire,
                        1,
                        {"id": self.wire_info.wire_id, "color": color, "coord": coord, "matrix": matrix1260pts},
                    )
                ]
                x_origin, y_origin = id_origins.get("xyOrigin", (0, 0))
                self.sketcher.circuit(x_origin, y_origin, model=model_wire)

        # Move the cursor indicator
        self.canvas.coords(self.cursor_indicator_id, x + x_min - 0, y + y_min - 0, x + x_min + 10, y + y_min + 10)

    def canvas_click(self, event):
        """
        Handles mouse clicks during placement modes.
        """
        x, y = event.x, event.y
        x_origin, y_origin = id_origins.get("xyOrigin", (0, 0))
        x_max, y_max = id_origins["bottomLimit"]
        if x < x_origin or x > x_max or y < y_origin or y > y_max:
            return  # Click is outside valid area

        (adjusted_x, adjusted_y), (col, line) = self.sketcher.find_nearest_grid_point(x, y, matrix=matrix1260pts)

        if self.tool_mode == "Connection":
            # Wire placement logic
            if self.wire_info.start_point is None:
                if matrix1260pts[f"{col},{line}"]["state"] == FREE:
                    model_wire = [
                        (
                            self.sketcher.draw_wire,
                            1,
                            {
                                "color": self.hex_to_rgb(self.selected_color),
                                "coord": [(col, line, col, line)],
                                "matrix": matrix1260pts,
                            },
                        )
                    ]
                    self.sketcher.circuit(x_origin, y_origin, model=model_wire)
                    self.wire_info.wire_id = self.current_dict_circuit["last_id"]
                    self.wire_info.start_point = (adjusted_x, adjusted_y)
                    self.wire_info.start_col_line = (col, line)
            else:
                # Finalize the wire
                self.wire_info.start_point = None
                self.wire_info.start_col_line = None
                print("Wire placement completed.")

        elif self.tool_mode in ("Input", "Output") and matrix1260pts[f"{col},{line}"]["state"] == FREE:
            # pin_io placement logic
            type_const = INPUT if self.tool_mode == "Input" else OUTPUT
            model_pin_io = [
                (
                    self.sketcher.draw_pin_io,
                    1,
                    {"color": self.selected_color, "type": type_const, "coord": [(col, line)], "matrix": matrix1260pts},
                )
            ]
            self.sketcher.circuit(x_origin, y_origin, model=model_pin_io)
            # Optionally deactivate after placement
            # self.cancel_pin_io_placement()

    def cancel_placement(self, _=None):
        """
        Cancels any active placement mode (wire or pin_io), untoggles the active button, and resets the state.
        """
        self.deactivate_button(self.tool_mode)
        self.deactivate_mode(self.tool_mode)
        print(f"{self.tool_mode} placement canceled.")

    def hex_to_rgb(self, hex_color):
        """
        Converts a hex color string to an RGB tuple.
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
