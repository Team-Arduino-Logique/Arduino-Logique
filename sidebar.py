# sidebar.py

import tkinter as tk
from tkinter import messagebox
import os

class Tooltip: # the tooltip is the popup that appears when we hover over a chip
    """Simple tooltip implementation without external libraries."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        # Position the tooltip near the widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, 
            text=self.text, 
            justify='left',
            background="#ffffff", 
            relief='solid', 
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

class Sidebar:
    def __init__(self, parent, chip_images_path="chips"):
        """
        Initializes the sidebar.

        Parameters:
        - parent (tk.Frame): The parent frame to attach the sidebar to.
        - chip_images_path (str): Path to the directory containing chip images.
        """
        self.parent = parent
        self.chip_images_path = chip_images_path
        self.chip_images = []
        self.load_chip_images()

        # Creating the sidebar frame
        self.sidebar_frame = tk.Frame(self.parent, bg="#333333", width=250, bd=0, highlightthickness=0)
        self.sidebar_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_propagate(False)  # Preventing frame from resizing

        # Configuring grid weights for the sidebar
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Search bar
        self.sidebar_frame.grid_rowconfigure(1, weight=0)  # Chips label
        self.sidebar_frame.grid_rowconfigure(2, weight=8)  # Chips area (80%)
        self.sidebar_frame.grid_rowconfigure(3, weight=0)  # Manage button
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Creating sidebar components
        self.create_search_bar()
        self.create_chips_area()
        self.create_manage_button()

    def load_chip_images(self):
        """
        Loads chip images from the specified directory and scales them down.
        """
        if not os.path.isdir(self.chip_images_path):
            messagebox.showerror("Error", f"Chip images directory '{self.chip_images_path}' not found.")
            return

        supported_formats = ('.png', '.gif', '.ppm', '.pgm')
        for filename in os.listdir(self.chip_images_path):
            if filename.lower().endswith(supported_formats):
                image_path = os.path.join(self.chip_images_path, filename)
                try:
                    img = tk.PhotoImage(file=image_path)
                    # Scaling down the image using subsample
                    # For example, if images are 150x150 and we want ~30x30, using subsample(5, 5)
                    scaled_img = img.subsample(5, 5)  # Further increased scaling factor
                    self.chip_images.append((filename, scaled_img))
                    print(f"Loaded and scaled chip image: {filename}")
                except Exception as e:
                    print(f"Error loading image '{filename}': {e}")
                    messagebox.showwarning("Image Load Error", f"Failed to load '{filename}'.")

    def create_search_bar(self):
        """
        Creates the search bar at the top of the sidebar.
        """
        # Frame for search components
        search_frame = tk.Frame(self.sidebar_frame, bg="#333333")
        search_frame.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="we")

        # Search label
        search_label = tk.Label(
            search_frame,
            text="Search Chips",
            bg="#333333",
            fg="#479dff",
            font=("Arial", 10, "bold")
        )
        search_label.pack(anchor="w")

        # Search entry
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 10),
            bg="#444444",
            fg="white",
            insertbackground="#479dff",
            relief="flat"
        )
        self.search_entry.pack(fill="x", pady=(2, 0))
        self.search_entry.bind("<KeyRelease>", self.on_search)

    def create_chips_area(self):
        """
        Creates the area where chip images are displayed as selectable buttons.
        Implements a scrollable grid with empty slots.
        """
        # Frame for chips label
        chips_label_frame = tk.Frame(self.sidebar_frame, bg="#333333")
        chips_label_frame.grid(row=1, column=0, padx=10, pady=(5, 2), sticky="w")

        # Chips label
        chips_label = tk.Label(
            chips_label_frame,
            text="Available Chips",
            bg="#333333",
            fg="#479dff",
            font=("Arial", 10, "bold")
        )
        chips_label.pack(anchor="w")

        # Creating a canvas for chips with a vertical scrollbar
        self.canvas = tk.Canvas(self.sidebar_frame, bg="#333333", highlightthickness=0, bd=0)
        self.canvas.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Adding a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=2, column=0, sticky='nse')  # Positioned on the right side

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Creating a frame inside the canvas to hold chip buttons
        self.chips_inner_frame = tk.Frame(self.canvas, bg="#333333")
        self.canvas.create_window((0, 0), window=self.chips_inner_frame, anchor="nw")

        # Binding the configure event to update the scrollregion
        self.chips_inner_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Defining grid properties
        self.columns = 2  # Number of columns in the grid
        self.visible_rows = 4  # Number of rows visible without scrolling
        self.grid_capacity = self.columns * self.visible_rows  # Total slots visible

        # Displaying chips
        self.display_chips(self.chip_images)

    def display_chips(self, chips):
        """
        Displays chip buttons in the chips_inner_frame.

        Parameters:
        - chips (list): List of tuples containing chip name and PhotoImage.
        """
        # Clearing existing chips
        for widget in self.chips_inner_frame.winfo_children():
            widget.destroy()

        # Calculating the number of slots based on grid_capacity
        total_slots = self.grid_capacity

        # Limiting the number of chips displayed to grid_capacity for initial display
        display_chips = chips[:total_slots]

        # Displaying existing chips
        for index, (chip_name, chip_image) in enumerate(display_chips):
            row = index // self.columns
            col = index % self.columns
            btn = tk.Button(
                self.chips_inner_frame,
                image=chip_image,
                bg="#333333",
                activebackground="#479dff",
                relief="flat",
                command=lambda name=chip_name: self.select_chip(name),
                width=30,   # Fixed width to match image size
                height=30   # Fixed height to match image size
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            Tooltip(btn, chip_name)  # Adding tooltip with chip name

            # Binding hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#479dff"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#333333"))

        # Filling remaining slots with empty frames to maintain grid layout
        remaining_slots = total_slots - len(display_chips)
        for i in range(remaining_slots):
            row = (len(display_chips) + i) // self.columns
            col = (len(display_chips) + i) % self.columns
            empty_frame = tk.Frame(
                self.chips_inner_frame,
                width=30,  # Fixed size to match chip buttons
                height=30,
                bg="#333333",
                relief="flat"
            )
            empty_frame.grid_propagate(False)  # Preventing frame from resizing
            empty_frame.grid(row=row, column=col, padx=1, pady=1)

    def create_manage_button(self):
        """
        Creates the 'Manage Components' button at the bottom of the sidebar without an icon.
        """
        manage_button = tk.Button( # the button is invisible for now we can change this later
            self.sidebar_frame,
            text="Manage Components",
            bg="#333333",  # Matching the sidebar's background to simulate transparency
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            borderwidth=0,
            command=self.manage_components
        )
        manage_button.grid(row=3, column=0, padx=10, pady=5, sticky="we")

    def select_chip(self, chip_name):
        """
        Handler for selecting a chip.

        Parameters:
        - chip_name (str): The name of the selected chip.
        """
        messagebox.showinfo("Chip Selected", f"Selected Chip: {chip_name}")
        # I thought about making the chip selected appear in the mouse cursor, will be done later if agreed upon

    def manage_components(self):
        """
        Handler for the 'Manage Components' button.
        """
        messagebox.showinfo("Manage Components", "Manage Components functionality not implemented yet.")

    def on_search(self, event):
        """
        Filters the displayed chips based on the search query.

        Parameters:
        - event (tk.Event): The event object.
        """
        query = self.search_entry.get().lower()
        if not query:
            filtered_chips = self.chip_images
        else:
            filtered_chips = [
                (name, img) for name, img in self.chip_images
                if query in name.lower()
            ]
        self.display_chips(filtered_chips)
