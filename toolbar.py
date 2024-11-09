# toolbar.py

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, colorchooser
import os
from dataCDLT import matrix1260pts, id_origins, current_dict_circuit, INPUT, OUTPUT, FREE, USED, matrix1260pts
from component_sketch import ComponentSketcher


class Toolbar:
    def __init__(self, parent, canvas, board, sketcher):
        self.parent = parent
        self.canvas = canvas
        self.board = board
        self.sketcher = sketcher
        self.selected_color = "#479dff"
        self.images = {}
        self.icon_size = 24
        self.buttons = {}
        self.active_button = None
        self.wire_placement_active = False
        self.pinIO_placement_active = False
        self.pinIO_type = None  # Will be set to 'Input' or 'Output' during placement
        self.wire_start_point = None
        self.wire_start_col_line = None
        self.cursor_indicator_id = None
        self.wire_id = None  # To track the current wire being drawn
        self.create_topbar()
        self.canvas.bind("<Motion>", self.canvas_follow_mouse, add="+")
        self.canvas.bind("<Button-1>", self.canvas_click, add="+")
        self.canvas.bind("<Button-3>", self.cancel_placement, add="+")

    def create_topbar(self):
        """
        Creates the secondary top bar with specified buttons and a color chooser.
        """
        # Create the top bar frame
        self.topbar_frame = tk.Frame(self.parent, bg="#505050", height=40, bd=0, highlightthickness=0)

        # Create left and right subframes
        self.left_frame = tk.Frame(self.topbar_frame, bg="#505050")
        self.left_frame.pack(side=tk.LEFT, padx=5, pady=5)

        self.right_frame = tk.Frame(self.topbar_frame, bg="#505050")
        self.right_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        # Load images
        self.load_images()

        # Create buttons in the left frame
        self.create_button("Connection", self.left_frame)
        self.create_button("Power", self.left_frame)
        self.create_button("Input", self.left_frame)
        self.create_button("Output", self.left_frame)

        # Create the color chooser and Delete button in the right frame
        self.create_color_chooser(self.right_frame)
        self.create_button("Delete", self.right_frame)

    def load_images(self):
        """
        Loads PNG images from the 'icons' folder, scales them, and stores them in the images dictionary.
        """
        icon_names = ["connection", "power", "input", "output", "delete"]
        icons_folder = Path("assets/icons").resolve()

        for name in icon_names:
            path = os.path.join(icons_folder, f"{name}.png")
            try:
                image = tk.PhotoImage(file=path)
                # Calculate the scaling factor based on original image size and desired icon_size
                original_width = image.width()
                original_height = image.height()
                scale_factor = max(original_width, original_height) // self.icon_size
                if scale_factor > 1:
                    image = image.subsample(scale_factor, scale_factor)
                self.images[name] = image
            except tk.TclError:
                messagebox.showerror(
                    "Image Load Error", f"Failed to load {path}. Ensure the file exists and is a valid PNG image."
                )
                self.images[name] = None  # Fallback if image fails to load

    def create_button(self, action, parent_frame):
        """
        Helper method to create a button in the specified frame with an icon.

        Parameters:
        - action (str): The action name corresponding to the button.
        - parent_frame (tk.Frame): The frame to place the button in.
        """
        image = self.images.get(action.lower())
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
            btn.image = image  # Keep a reference to prevent garbage collection
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

    def create_color_chooser(self, parent_frame):
        """
        Creates a color chooser button next to the Delete button.
        """
        square_size = self.icon_size
        self.color_button = tk.Button(
            parent_frame, bg=self.selected_color, width=2, height=1, relief="raised", bd=1, command=self.choose_color
        )
        self.color_button.pack(side=tk.LEFT, padx=2, pady=2)

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
            # Here you can add logic to apply the selected color to new connections

    def button_action(self, action_name):
        """
        Defines the action to perform when a button is clicked.
        """
        # If there's an active button that's not the one clicked, deactivate it
        if self.active_button and self.active_button != action_name:
            self.deactivate_button(self.active_button)
            self.deactivate_mode(self.active_button)

        # Toggle the clicked button's active state
        if self.active_button == action_name:
            # If already active, deactivate it
            self.deactivate_button(action_name)
            self.active_button = None
            self.deactivate_mode(action_name)
        else:
            # Activate the clicked button
            self.activate_button(action_name)
            self.active_button = action_name
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
        self.deactivate_wire_placement_mode()
        self.deactivate_pinIO_placement_mode()

        if action_name == "Connection":
            self.activate_wire_placement_mode()
        elif action_name in ["Input", "Output"]:
            self.activate_pinIO_placement_mode(action_name)

    def deactivate_mode(self, action_name):
        """
        Deactivates the mode associated with the action_name.
        """
        if action_name == "Connection":
            self.deactivate_wire_placement_mode()
        elif action_name in ["Input", "Output"]:
            self.deactivate_pinIO_placement_mode()

    def activate_wire_placement_mode(self):
        """
        Activates wire placement mode.
        """
        self.wire_placement_active = True
        self.canvas.config(cursor="none")
        self.wire_start_point = None
        self.wire_start_col_line = None
        if self.cursor_indicator_id is None:
            self.create_cursor_indicator()

    def deactivate_wire_placement_mode(self):
        """
        Deactivates wire placement mode.
        """
        self.wire_placement_active = False
        self.canvas.config(cursor="")
        self.remove_cursor_indicator()
        self.wire_start_point = None
        self.wire_start_col_line = None
        self.canvas.delete("wire_temp_circle")

    def activate_pinIO_placement_mode(self, pin_type):
        """
        Activates PinIO placement mode for the specified pin type (Input or Output).
        """
        self.pinIO_placement_active = True
        self.pinIO_type = pin_type  # Store the type for use during placement
        self.canvas.config(cursor="none")
        if self.cursor_indicator_id is None:
            self.create_cursor_indicator(pin_type)

    def deactivate_pinIO_placement_mode(self):
        """
        Deactivates PinIO placement mode.
        """
        self.pinIO_placement_active = False
        self.pinIO_type = None
        self.canvas.config(cursor="")
        self.remove_cursor_indicator()

    def create_cursor_indicator(self, pin_type=None):
        """
        Creates a cursor indicator that follows the mouse position.
        """
        if self.cursor_indicator_id is None:
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
        if not (self.wire_placement_active or self.pinIO_placement_active) or self.cursor_indicator_id is None:
            return
        x, y = event.x, event.y
        x_min, y_min = id_origins["xyOrigin"]
        x_max, y_max = id_origins["bottomLimit"]
        if x > x_min and x < x_max and y > y_min and y < y_max:
            nearest_point, (col, line) = self.sketcher.find_nearest_grid_point(x, y, matrix1260pts)
            x, y = nearest_point[0], nearest_point[1]
            if self.wire_placement_active and self.wire_start_point and matrix1260pts[f"{col},{line}"]["state"] == FREE:

                coord = current_dict_circuit[self.wire_id]["coord"]
                matrix1260pts[f"{coord[0][2]},{coord[0][3]}"]["state"] = FREE
                color = self.hex_to_rgb(self.selected_color)
                coord = [(coord[0][0], coord[0][1], col, line)]
                model_wire = [
                    (
                        self.sketcher.drawWire,
                        1,
                        {"id": self.wire_id, "color": color, "coord": coord, "matrix": matrix1260pts},
                    )
                ]
                xO, yO = id_origins.get("xyOrigin", (0, 0))
                self.sketcher.circuit(xO, yO, model=model_wire)

        # Move the cursor indicator
        self.canvas.coords(self.cursor_indicator_id, x + x_min - 5, y + y_min - 5, x + x_min + 5, y + y_min + 5)

    def canvas_click(self, event):
        """
        Handles mouse clicks during placement modes.
        """
        x, y = event.x, event.y
        x_min, y_min = id_origins["xyOrigin"]
        x_max, y_max = id_origins["bottomLimit"]
        if x < x_min or x > x_max or y < y_min or y > y_max:
            return  # Click is outside valid area

        nearest_point, (col, line) = self.sketcher.find_nearest_grid_point(x, y, matrix=matrix1260pts)
        xO, yO = id_origins.get("xyOrigin", (0, 0))

        if self.wire_placement_active:
            # Wire placement logic
            adjusted_x, adjusted_y = nearest_point[0], nearest_point[1]
            if self.wire_start_point is None:

                if matrix1260pts[f"{col},{line}"]["state"] == FREE:

                    color = self.hex_to_rgb(self.selected_color)
                    coord = [(col, line, col, line)]
                    model_wire = [
                        (self.sketcher.drawWire, 1, {"color": color, "coord": coord, "matrix": matrix1260pts})
                    ]
                    self.sketcher.circuit(xO, yO, model=model_wire)
                    self.wire_id = current_dict_circuit["last_id"]
                    self.wire_start_point = (adjusted_x, adjusted_y)
                    self.wire_start_col_line = (col, line)
            else:
                # Finalize the wire

                self.wire_start_point = None
                self.wire_start_col_line = None
                print("Wire placement completed.")

        elif self.pinIO_placement_active and matrix1260pts[f"{col},{line}"]["state"] == FREE:

            # PinIO placement logic
            color = self.selected_color
            type_const = INPUT if self.pinIO_type == "Input" else OUTPUT
            model_pinIO = [
                (
                    self.sketcher.drawPinIO,
                    1,
                    {"color": color, "type": type_const, "coord": [(col, line)], "matrix": matrix1260pts},
                )
            ]
            self.sketcher.circuit(xO, yO, model=model_pinIO)
            # Optionally deactivate after placement
            # self.cancel_pinIO_placement()

    def cancel_placement(self, event=None):
        """
        Cancels any active placement mode (wire or pinIO), untoggles the active button, and resets the state.
        """
        if self.wire_placement_active:
            self.cancel_wire_placement(event)
        elif self.pinIO_placement_active:
            self.cancel_pinIO_placement(event)

    def cancel_wire_placement(self, event=None):
        """
        Cancels the wire placement, untoggles the Connection button, and resets the state.
        """
        if not self.wire_placement_active:
            return
        # Deactivate the Connection button
        self.deactivate_button("Connection")
        self.active_button = None
        # Deactivate wire placement mode
        self.deactivate_wire_placement_mode()
        print("Wire placement canceled.")

    def cancel_pinIO_placement(self, event=None):
        """
        Cancels the PinIO placement, untoggles the Input/Output button, and resets the state.
        """
        if not self.pinIO_placement_active:
            return
        # Deactivate the active button
        self.deactivate_button(self.active_button)
        self.active_button = None
        # Deactivate pinIO placement mode
        self.deactivate_pinIO_placement_mode()
        print(f"{self.pinIO_type} placement canceled.")

    def hex_to_rgb(self, hex_color):
        """
        Converts a hex color string to an RGB tuple.
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
