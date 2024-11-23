"""
This module defines the Sidebar class, which is responsible for creating and managing a sidebar in a 
Tkinter GUI application. The sidebar displays available chips as selectable buttons, provides a search 
bar to filter chips, and includes a button to manage components.
"""

from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, font
import os
from typing import Callable, Tuple
import subprocess
import sys
from idlelib.tooltip import Hovertip  # type: ignore
from toolbar import Toolbar
from component_sketch import ComponentSketcher
from dataCDLT import FREE, USED
from object_model.circuit_object_model import Chip, get_all_available_chips, get_chip_modification_times


@dataclass
class SidebarGrid:
    """
    A class to represent the grid layout of the sidebar.
    Attributes:
        - columns (int): The number of columns in the grid.
        - visible_rows (int): The number of rows visible without scrolling.
        - grid_capacity (int): The total number of slots visible.
    """

    columns: int
    visible_rows: int
    grid_capacity: int


class Sidebar:
    """
    A class to represent a sidebar in a Tkinter GUI application.
    Attributes:
        - chip_images_path: The path to the directory containing chip images.
        - canvas: The canvas where the chips are placed.
        - sketcher: The component sketcher object.
        - available_chips_and_imgs: A list of tuples containing available chips and their images.
        - chip_name_to_index: A dictionary mapping chip names to their index in the available chips list.
        - search_entry: The search bar entry widget.
        - chips_inner_frame: The frame inside the canvas for chip buttons.
        - sidebar_grid: An instance of the SidebarGrid class.
        - selected_chip_name: The name of the selected chip.
        - chip_cursor_image: The image of the chip cursor.
        - saved_bindings: A dictionary of saved event bindings.
    """

    def __init__(
        self, parent, current_dict_circuit, toolbar: Toolbar, chip_images_path="chips", canvas=None, sketcher=None
    ) -> None:
        """
        Initializes the sidebar.
        Parameters:
            - parent: The parent widget.
            - chip_images_path (str): The path to the directory containing chip images.
            - canvas: The canvas where the chips are placed.
            - sketcher: The component sketcher object.
        """
        self.initialize_chip_data(current_dict_circuit, chip_images_path)
        self.chip_images_path = chip_images_path
        self.canvas: tk.Canvas = canvas
        self.sketcher: ComponentSketcher = sketcher
        self.toolbar = toolbar

        self.selected_chip_name = None
        self.chip_cursor_image = None
        self.saved_bindings: dict[str, Callable] = {}

        # Creating the sidebar frame
        sidebar_frame = tk.Frame(parent, bg="#333333", width=275, bd=0, highlightthickness=0)
        sidebar_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        sidebar_frame.grid_propagate(False)  # Preventing frame from resizing

        # Configuring grid weights for the sidebar
        sidebar_frame.grid_rowconfigure(0, weight=0)  # Search bar
        sidebar_frame.grid_rowconfigure(1, weight=0)  # Chips label
        sidebar_frame.grid_rowconfigure(2, weight=8)  # Chips area (80%)
        sidebar_frame.grid_rowconfigure(3, weight=0)  # Manage button
        sidebar_frame.grid_columnconfigure(0, weight=1)

        self.sidebar_grid = SidebarGrid(columns=2, visible_rows=12, grid_capacity=24)

        # Creating sidebar components
        self.create_search_bar(sidebar_frame)
        self.create_chips_area(sidebar_frame)
        self.create_manage_button(sidebar_frame)

        self.chip_files_mtimes = get_chip_modification_times()

    def initialize_chip_data(self, current_dict_circuit, chip_images_path) -> None:
        """
        Initializes the chip data for the sidebar.
        """
        self.current_dict_circuit = current_dict_circuit
        images = self.load_chip_images(chip_images_path)
        self.available_chips_and_imgs: list[Tuple[Chip, tk.PhotoImage | None]] = [
            (chip, images.get(chip.package_name)) for chip in get_all_available_chips().values()
        ]
        # Sort the chips based on the number after 'HC' in their chip_type
        self.available_chips_and_imgs.sort(key=lambda chip_img: int(chip_img[0].chip_type.split("HC")[-1]))

        # Create a reverse lookup dictionary for chip names to their index in the list
        self.chip_name_to_index = {
            chip.chip_type: index for index, (chip, _) in enumerate(self.available_chips_and_imgs)
        }

    def load_chip_images(self, img_path) -> dict[str, tk.PhotoImage]:
        """
        Loads chip images from the specified directory and scales them down.
        """
        images_dict: dict[str, tk.PhotoImage] = {}

        if not os.path.isdir(img_path):
            messagebox.showerror("Error", f"Chip images directory '{img_path}' not found.")
            return images_dict

        supported_formats = (".png", ".gif", ".ppm", ".pgm")
        for filename in os.listdir(img_path):
            if filename.lower().endswith(supported_formats):
                image_path = os.path.join(img_path, filename)
                try:
                    img = tk.PhotoImage(file=image_path)
                    # Scaling down the image using subsample
                    # For example, if images are 150x150 and we want ~30x30, using subsample(5, 5)
                    scaled_img = img.subsample(5, 5)  # Further increased scaling factor
                    img_name = os.path.splitext(filename)[0]
                    images_dict[img_name] = scaled_img
                    print(f"Loaded and scaled chip image: {filename}")
                except (tk.TclError, FileNotFoundError) as e:
                    print(f"Error loading image '{filename}': {e}")
                    messagebox.showwarning("Image Load Error", f"Failed to load '{filename}'.")
        return images_dict

    def create_search_bar(self, sidebar_frame):
        """
        Creates the search bar at the top of the sidebar.
        """
        # Frame for search components
        search_frame = tk.Frame(sidebar_frame, bg="#333333")
        search_frame.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="we")

        # Search label
        search_label = tk.Label(
            search_frame, text="Search Chips", bg="#333333", fg="#479dff", font=("Arial", 10, "bold")
        )
        search_label.pack(anchor="w")

        # Search entry
        self.search_entry = tk.Entry(
            search_frame, font=("Arial", 10), bg="#444444", fg="white", insertbackground="#479dff", relief="flat"
        )
        self.search_entry.pack(fill="x", pady=(2, 0))
        self.search_entry.bind("<KeyRelease>", self.on_search)

    def create_chips_area(self, sidebar_frame):
        """
        Creates the area where chip images are displayed as selectable buttons.
        Implements a scrollable grid with empty slots.
        """
        # Frame for chips label
        chips_label_frame = tk.Frame(sidebar_frame, bg="#333333")
        chips_label_frame.grid(row=1, column=0, padx=10, pady=(5, 2), sticky="w")

        # Chips label
        chips_label = tk.Label(
            chips_label_frame, text="Available Chips", bg="#333333", fg="#479dff", font=("Arial", 10, "bold")
        )
        chips_label.pack(anchor="w")

        # Creating a canvas for chips with a vertical scrollbar
        canvas_chips = tk.Canvas(sidebar_frame, bg="#333333", highlightthickness=0, bd=0)
        canvas_chips.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Adding a scrollbar to the canvas
        scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=canvas_chips.yview)
        scrollbar.grid(row=2, column=0, sticky="nse")

        canvas_chips.configure(yscrollcommand=scrollbar.set)

        # Creating a frame inside the canvas to hold chip buttons
        self.chips_inner_frame = tk.Frame(canvas_chips, bg="#333333")
        canvas_chips.create_window((0, 0), window=self.chips_inner_frame, anchor="nw")

        # Binding the configure event to update the scrollregion
        self.chips_inner_frame.bind(
            "<Configure>", lambda event: canvas_chips.configure(scrollregion=canvas_chips.bbox("all"))
        )

        # Defining grid properties
        self.sidebar_grid.columns = 2  # Number of columns in the grid
        self.sidebar_grid.visible_rows = 12  # Number of rows visible without scrolling
        self.sidebar_grid.grid_capacity = (
            self.sidebar_grid.columns * self.sidebar_grid.visible_rows
        )  # Total slots visible

        # Displaying chips
        self.display_chips(self.available_chips_and_imgs)

    def display_chips(self, chips: list[Tuple[Chip, tk.PhotoImage]]):
        """
        Displays chip buttons in the chips_inner_frame.
        """
        # Clearing existing chips
        for widget in self.chips_inner_frame.winfo_children():
            widget.destroy()

        display_chips = chips
        fira_code_font = font.Font(family="FiraCode-Bold.ttf", size=12)

        # Displaying existing chips
        for index, (chip, chip_image) in enumerate(display_chips):
            row = index // self.sidebar_grid.columns
            col = index % self.sidebar_grid.columns
            btn = tk.Button(
                self.chips_inner_frame,
                image=chip_image,
                text=chip.chip_type,
                compound="center",
                font=fira_code_font,
                fg="white",  # Set text color to white
                bg="#333333",
                activebackground="#479dff",
                relief="flat",
                command=self.create_select_chip_command(chip.chip_type),
                width=100,  # Fixed width to match image size
                height=60,  # Fixed height to match image size
                borderwidth=0,
                highlightthickness=0,
                padx=10
            )
            btn.grid(row=row, column=col, padx=0, pady=0)
            Hovertip(btn, chip.description, 500)  # Adding tooltip with chip name

            def enter_effect(_, b=btn):
                b.configure(bg="#479dff")

            def leave_effect(_, b=btn):
                b.configure(bg="#333333")

            # Binding hover effects
            btn.bind("<Enter>", enter_effect, add="+")
            btn.bind("<Leave>", leave_effect, add="+")

    def create_select_chip_command(self, chip_type: str) -> Callable:
        """
        Creates a command for selecting a chip.
        """
        return lambda: self.select_chip(chip_type)

    def create_manage_button(self, sidebar_frame):
        """
        Creates the 'Manage Components' button at the bottom of the sidebar without an icon.
        """
        manage_button = tk.Button(
            sidebar_frame,
            text="Manage Components",
            bg="#333333",  # Matching the sidebar's background to simulate transparency
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            borderwidth=0,
            command=self.manage_components,
            highlightthickness=0,
        )
        manage_button.grid(row=3, column=0, padx=0, pady=0, sticky="we")

    def select_chip(self, chip_name):
        """
        Handler for selecting a chip.
        """
        # Cancel any ongoing chip placement
        self.cancel_chip_placement()
        self.toolbar.deactivate_button("all")
        self.toolbar.deactivate_mode("all")

        # Set the new selected chip
        self.selected_chip_name = chip_name
        self.start_chip_placement(chip_name)

    def start_chip_placement(self, chip_name):
        """
        Initiates the chip placement process by changing the cursor to the chip image.
        """
        # Get the chip image
        chip_data = next((chip for chip in self.available_chips_and_imgs if chip[0].chip_type == chip_name), None)
        if not chip_data:
            print("Error", f"Chip '{chip_name}' not found.")
            return

        self.chip_cursor_image = chip_data[1]

        # Keep a reference to the image to prevent garbage collection
        self.canvas.chip_cursor_image = self.chip_cursor_image

        # Hide the default cursor
        self.canvas.config(cursor="none")

        # Bind events to the canvas
        # Save the current bindings
        self.saved_bindings = {
            "<Motion>": self.canvas.bind("<Motion>"),
            "<Button-1>": self.canvas.bind("<Button-1>"),
            "<Button-3>": self.canvas.bind("<Button-3>"),
        }
        self.canvas.bind("<Motion>", self.canvas_on_mouse_move, add="+")
        self.canvas.bind("<Button-1>", self.canvas_on_click, add="+")
        self.canvas.bind("<Button-3>", self.cancel_chip_placement, add="+")  # Bind right-click to cancel

        print(f"Started placement for chip: {chip_name}")

    def cancel_chip_placement(self, _=None):
        """
        Cancels the current chip placement process.
        """
        if self.selected_chip_name:
            # Remove the cursor-following image if it exists
            if hasattr(self.canvas, "chip_cursor_id"):
                self.canvas.delete(self.canvas.chip_cursor_id)
                del self.canvas.chip_cursor_id

            # Reset the cursor to default
            self.canvas.config(cursor="")

            # Unbind the placement-related events
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")  # Unbind right-click if bound
            # Restore the saved bindings
            for evt, handler in self.saved_bindings.items():
                self.canvas.bind(evt, handler)

            # Reset the selected chip
            self.selected_chip_name = None
            self.chip_cursor_image = None

            print("Chip placement canceled.")

    def canvas_on_mouse_move(self, event):
        """
        Handles the mouse movement over the canvas to make the chip follow the cursor.
        """
        # Get the cursor position
        x, y = event.x, event.y

        # Create the chip cursor image if it doesn't exist
        if not hasattr(self.canvas, "chip_cursor_id"):
            self.canvas.chip_cursor_id = self.canvas.create_image(x, y, image=self.chip_cursor_image, anchor="nw")
        else:
            # Move the existing chip cursor image
            self.canvas.coords(self.canvas.chip_cursor_id, x, y)

        # Bring the cursor image to the front
        self.canvas.tag_raise(self.canvas.chip_cursor_id)

    def canvas_on_click(self, event):
        """
        Handles the mouse click on the canvas to place the chip on the breadboard.
        """
        # Get the cursor position
        x, y = event.x, event.y

        # Place the chip on the breadboard at the cursor position
        self.place_chip_at(x, y, self.selected_chip_name)

        # Remove the cursor-following image
        if hasattr(self.canvas, "chip_cursor_id"):
            self.canvas.delete(self.canvas.chip_cursor_id)
            del self.canvas.chip_cursor_id

        # Reset the cursor
        self.canvas.config(cursor="")

        # Unbind the placement-related events
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")  # Unbind right-click
        # Restore the saved bindings
        for evt, handler in self.saved_bindings.items():
            self.canvas.bind(evt, handler)

        # Reset the selected chip
        print(f"Chip {self.selected_chip_name} placed.")
        self.selected_chip_name = None
        self.chip_cursor_image = None

    def place_chip_at(self, x, y, chip_name):
        """
        Places the selected chip on the breadboard at the nearest grid point.
        """
        # Find the nearest grid point
        (nearest_x, nearest_y), (column, line) = self.sketcher.find_nearest_grid(x, y, matrix=self.sketcher.matrix)
        print(f"Nearest grid point: {nearest_x}, {nearest_y}, Column: {column}, Line: {line}")

        if column is None or line is None:
            messagebox.showerror("Placement Error", "No grid point found nearby.")
            return

        try:
            chip_dict = self.available_chips_and_imgs[self.chip_name_to_index[chip_name]][0].to_generic_dict()
            if chip_dict["type"] != chip_name:  # Sanity check
                raise IndexError()
        except IndexError as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Unknown chip: {chip_name}")
            return

        chip_dict["internalFunc"] = self.sketcher.internal_func
        chip_dict["open"] = 0
        chip_dict["logicFunction"] = self.sketcher.draw_symb(chip_dict["logicFunctionName"])

        chip_model = [
            (
                self.sketcher.draw_chip,
                1,
                chip_dict,
            )
        ]

        # Draw the chip at the calculated exact position
        pin_x, pin_y = self.sketcher.xy_chip2pin(nearest_x, nearest_y)
        pin_count = chip_model[0][2]["pinCount"]
        half_pin_count = pin_count // 2

        max_column = column + half_pin_count - 1
        if max_column > 63:
            # Not enough space, prevent placement and look for the nearest snap point on the left
            print("Not enough space to place the chip here.")
            self.cancel_chip_placement()
            return

        # Check if new holes are free
        holes_available = True
        occupied_holes = []
        for i in range(half_pin_count):
            # Top row (line 7 or 21)
            hole_id_top = f"{column + i},{line}"
            # Bottom row (line 6 or 20)
            hole_id_bottom = f"{column + i},{line + 1}"

            hole_top = self.sketcher.matrix.get(hole_id_top)
            hole_bottom = self.sketcher.matrix.get(hole_id_bottom)

            if hole_top["state"] != FREE or hole_bottom["state"] != FREE:
                holes_available = False
                break

            occupied_holes.extend([hole_id_top, hole_id_bottom])

        if not holes_available:
            print("Holes are occupied. Cannot place the chip here.")
            self.cancel_chip_placement()
            return

        # Mark new holes as used
        for hole_id in occupied_holes:
            self.sketcher.matrix[hole_id]["state"] = USED
        model_chip = [(chip_model, 1, {"XY": (nearest_x, nearest_y), "pinUL_XY": (pin_x, pin_y)})]
        self.sketcher.circuit(nearest_x, nearest_y, scale=self.sketcher.scale_factor, model=model_chip)
        print(f"Chip {chip_name} placed at ({column}, {line}).")

        # Update the self.current_dict_circuit with the new chip
        chip_keys = [key for key in self.current_dict_circuit if key.startswith("_chip")]
        if chip_keys:
            last_chip_key = chip_keys[-1]  # Get the last key in sorted order
            added_chip_params = self.current_dict_circuit[last_chip_key]
            print("Last chip parameter:", added_chip_params)
            added_chip_params["occupied_holes"] = occupied_holes
        else:
            # delete the chip
            print("need to delete the added chip")

    def manage_components(self):
        """
        Handler for the 'Manage Components' button.
        """
        path = Path("Components").resolve()
        if os.name == "nt":  # For Windows
            try:
                os.startfile(path)
            except AttributeError:
                pass
        elif os.name == "posix":  # For macOS and Linux  # type: ignore
            with subprocess.Popen(["open", path] if sys.platform == "darwin" else ["xdg-open", path]):
                pass
        else:
            messagebox.showerror("Error", "Unsupported operating system.")

    def on_search(self, _):
        """
        Filters the displayed chips based on the search query.
        """
        query = self.search_entry.get().lower()
        if not query:
            filtered_chips = self.available_chips_and_imgs
        else:
            filtered_chips = [
                chip_data
                for chip_data in self.available_chips_and_imgs
                if query in chip_data[0].chip_type.lower()
                or query in chip_data[0].package_name.lower()
                or query in chip_data[0].description.lower()
                or any(query in func.__class__.__name__.lower() for func in chip_data[0].functions)
            ]
        self.display_chips(filtered_chips)

    def refresh(self):
        """
        Refreshes the sidebar with updated chip data.
        """
        current_mtimes = get_chip_modification_times()
        if current_mtimes != self.chip_files_mtimes:
            self.chip_files_mtimes = current_mtimes
            self.initialize_chip_data(self.current_dict_circuit, self.chip_images_path)
            self.on_search(None)
            print("Sidebar refreshed with updated chips.")
        #else: 
            #print("No changes detected. Sidebar not refreshed.")
