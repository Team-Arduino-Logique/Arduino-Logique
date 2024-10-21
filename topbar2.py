# topbar2.py

import tkinter as tk
from tkinter import messagebox, colorchooser
import os

class TopBar2:
    def __init__(self, parent):
        """
        Initializes the secondary top bar.

        Parameters:
        - parent (tk.Frame): The parent frame to attach the top bar to.
        """
        self.parent = parent
        self.selected_color = "#479dff"  # Default connection color
        self.images = {}  # Dictionary to hold PhotoImage references
        self.icon_size = 24  # Desired icon size in pixels
        self.buttons = {}   # Dictionary to hold button references
        self.active_button = None  # Currently active button
        self.create_topbar()

    def create_topbar(self):
        """
        Creates the secondary top bar with specified buttons and a color chooser.
        """
        # Create the top bar frame
        self.topbar_frame = tk.Frame(self.parent, bg="#505050", height=40, bd=0, highlightthickness=0)
        self.topbar_frame.pack(fill=tk.X)

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
            path = os.path.join("icones", f"{name}.png")
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

        Parameters:
        - action_name (str): The name of the action/button.
        """
        # If there's an active button that's not the one clicked, deactivate it
        if self.active_button and self.active_button != action_name:
            self.deactivate_button(self.active_button)

        # Toggle the clicked button's active state
        if self.active_button == action_name:
            # If already active, deactivate it
            self.deactivate_button(action_name)
            self.active_button = None
        else:
            # Activate the clicked button
            self.activate_button(action_name)
            self.active_button = action_name

        # Example actions based on button
        if action_name == "Connection":
            # Handle Connection button action
            print("Connection mode activated.")
        elif action_name == "Delete":
            # Handle Delete button action
            print("Delete mode activated.")
        elif action_name == "Power":
            # Handle Power button action
            print("Power mode activated.")
        elif action_name == "Input":
            # Handle Input button action
            print("Input mode activated.")
        elif action_name == "Output":
            # Handle Output button action
            print("Output mode activated.")

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
