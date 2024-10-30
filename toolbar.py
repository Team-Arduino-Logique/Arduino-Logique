# toolbar.py

import tkinter as tk
from tkinter import messagebox, colorchooser
import os
from dataCDLT import matrix1260pts, id_origins, current_dict_circuit

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
        self.wire_start_point = None
        self.wire_start_col_line = None
        self.cursor_circle_id = None
        self.create_topbar()
        self.canvas.bind("<Motion>", self.canvas_follow_mouse, add='+')
        self.canvas.bind("<Button-1>", self.canvas_click, add='+')
        self.canvas.bind("<Button-3>", self.cancel_wire_placement, add='+')

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
        for name in icon_names:
            path = os.path.join("icons", f"{name}.png")
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
                messagebox.showerror("Image Load Error", f"Failed to load {path}. Ensure the file exists and is a valid PNG image.")
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
                pady=2
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
                pady=2
            )
        btn.pack(side=tk.LEFT, padx=10, pady=2)  # Minimal spacing between buttons
        self.buttons[action] = btn  # Store button reference

    def create_color_chooser(self, parent_frame):
        """
        Creates a color chooser button next to the Delete button.

        Parameters:
        - parent_frame (tk.Frame): The frame to place the color chooser in.
        """
        square_size = self.icon_size
        self.color_button = tk.Button(
            parent_frame,
            bg=self.selected_color,
            width=2,
            height=1,
            relief="raised",
            bd=1,
            command=self.choose_color
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
            # Here you can add logic to apply the selected color to new connections

    def button_action(self, action_name):
        """
        Defines the action to perform when a button is clicked.
        """
        # If there's an active button that's not the one clicked, deactivate it
        if self.active_button and self.active_button != action_name:
            self.deactivate_button(self.active_button)

        # Toggle the clicked button's active state
        if self.active_button == action_name:
            # If already active, deactivate it
            self.deactivate_button(action_name)
            self.active_button = None
            if action_name == "Connection":
                self.deactivate_wire_placement_mode()
        else:
            # Activate the clicked button
            self.activate_button(action_name)
            self.active_button = action_name
            if action_name == "Connection":
                self.activate_wire_placement_mode()
            else:
                self.deactivate_wire_placement_mode()

        # elif action_name == "Delete":
        #     # Handle Delete button action
        #     print("Delete mode activated.")
        # elif action_name == "Power":
        #     # Handle Power button action
        #     print("Power mode activated.")
        # elif action_name == "Input":
        #     # Handle Input button action
        #     print("Input mode activated.")
        # elif action_name == "Output":
        #     # Handle Output button action
        #     print("Output mode activated.")

    def activate_button(self, action_name):
        """
        Activates the specified button by changing its background color.

        Parameters:
        - action_name (str): The name of the action/button to activate.
        """
        btn = self.buttons.get(action_name)
        if btn:
            btn.configure(bg="#707070")  # Active background color

    def deactivate_button(self, action_name):
        """
        Deactivates the specified button by resetting its background color.

        Parameters:
        - action_name (str): The name of the action/button to deactivate.
        """
        btn = self.buttons.get(action_name)
        if btn:
            btn.configure(bg="#505050")  # Inactive background color


    def create_cursor_circle(self):
        """
        Creates a circle that follows the mouse cursor.
        """
        if self.cursor_circle_id is None:
            self.cursor_circle_id = self.canvas.create_oval(0, 0, 10, 10, fill='grey', outline='')
            self.canvas.tag_raise(self.cursor_circle_id)

    def remove_cursor_circle(self):
        """
        Removes the cursor-following circle.
        """
        if self.cursor_circle_id is not None:
            self.canvas.delete(self.cursor_circle_id)
            self.cursor_circle_id = None  # Set back to None instead of deleting

    def canvas_follow_mouse(self, event):
        """
        Moves the cursor-following circle to the mouse position.
        """
        if not self.wire_placement_active or self.cursor_circle_id is None:
            return
        x, y = event.x, event.y
        self.canvas.coords(self.cursor_circle_id, x - 5, y - 5, x + 5, y + 5)

    def canvas_click(self, event):
        """
        Handles mouse clicks during wire placement.
        """
        if not self.wire_placement_active:
            return
    
        x, y = event.x, event.y
        # Find the nearest hole
        nearest_point, (col, line) = self.sketcher.find_nearest_grid_point(x, y, matrix1260pts)
        # Adjust for origin if necessary
        xO, yO = id_origins.get("xyOrigin", (0, 0))
        adjusted_x, adjusted_y = nearest_point[0] , nearest_point[1]
        if self.wire_start_point is None:
            # First click
            self.wire_start_point = (adjusted_x, adjusted_y)
            self.wire_start_col_line = (col, line)
            # Draw a small temporary circle at the nearest hole
            self.canvas.create_oval(
                adjusted_x + xO , adjusted_y + yO,
                adjusted_x + xO + 6, adjusted_y + yO + 6,
                fill='blue', outline='', tags='wire_temp_circle'
            )
        else:
            # Second click
            # Remove the temporary circle
            self.canvas.delete('wire_temp_circle')
            # Draw the wire from wire_start_point to nearest_point
            color_hex = self.selected_color
            color_rgb = self.hex_to_rgb(color_hex)
            # Create wire model
            wire_model = [
                (
                    self.sketcher.drawWire, 
                    1, 
                    {
                        "color": color_rgb, 
                        "XY": [
                            (self.wire_start_point[0], self.wire_start_point[1], adjusted_x, adjusted_y)
                        ],
                        "coords": [
                            (self.wire_start_col_line[0], self.wire_start_col_line[1], col, line)
                        ],
                        "matrix": matrix1260pts
                    }
                )
            ]
            # Call circuit() with the wire model
            x_origin, y_origin = id_origins.get("xyOrigin", (0, 0))
            self.sketcher.circuit(x_origin, y_origin, model=wire_model)
            # Reset wire_start_point
            self.wire_start_point = None
            self.wire_start_col_line = None


    def activate_wire_placement_mode(self):
        """
        Activates wire placement mode.
        """
        self.wire_placement_active = True
        self.canvas.config(cursor='none')
        self.wire_start_point = None
        self.wire_start_col_line = None
        if self.cursor_circle_id is None:
            self.create_cursor_circle()

    def deactivate_wire_placement_mode(self):
        """
        Deactivates wire placement mode.
        """
        self.wire_placement_active = False
        self.canvas.config(cursor='')
        self.remove_cursor_circle()
        self.wire_start_point = None
        self.wire_start_col_line = None
        self.canvas.delete('wire_temp_circle')

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

    def hex_to_rgb(self, hex_color):
        """
        Converts a hex color string to an RGB tuple.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))