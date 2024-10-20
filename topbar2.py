# topbar2.py

import tkinter as tk
from tkinter import messagebox

class TopBar2:
    def __init__(self, parent):
        """
        Initializes the secondary top bar.

        Parameters:
        - parent (tk.Frame): The parent frame to attach the top bar to.
        """
        self.parent = parent
        self.create_topbar()

    def create_topbar(self):
        """
        Creates the secondary top bar with specified buttons.
        """
        # Create the top bar frame
        self.topbar_frame = tk.Frame(self.parent, bg="#505050", height=40, bd=0, highlightthickness=0)
        # Do not use pack; main application will manage placement with grid

        # Configure grid layout within the top bar
        self.topbar_frame.grid_propagate(False)  # Prevent frame from resizing based on its contents
        for i in range(6):
            self.topbar_frame.grid_columnconfigure(i, weight=1)

        # Create buttons on the left
        self.create_button("Connection", 0)
        self.create_button("Power", 1)
        self.create_button("Input", 2)
        self.create_button("Output", 3)

        # Create the Delete button on the right
        self.create_button("Delete", 5, anchor="e")


    def create_button(self, text, column, anchor="w"):
        """
        Helper method to create a button in the top bar.

        Parameters:
        - text (str): The text to display on the button.
        - column (int): The grid column to place the button in.
        - anchor (str): Alignment of the button within the cell.
        """
        btn = tk.Button(
            self.topbar_frame,
            text=text,
            bg="#479dff",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            command=lambda: self.button_action(text)
        )
        # padding between buttons
        btn.grid(row=0, column=column, padx=0.3, pady=5, sticky=anchor)

    def button_action(self, action_name):
        """
        Defines the action to perform when a button is clicked.

        Parameters:
        - action_name (str): The name of the action/button.
        """
        messagebox.showinfo("Button Clicked", f"{action_name} button clicked.")
        # I will split this into multiple functions when I create png icons for each button
