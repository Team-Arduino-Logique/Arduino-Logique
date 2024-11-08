# sidebar.py

import tkinter as tk
from tkinter import messagebox, font
import os
from typing import Tuple
from component_sketch import ComponentSketcher
from dataCDLT import matrix1260pts, id_origins, FREE, USED, current_dict_circuit
from object_model.circuit_object_model import Chip, get_all_available_chips


class Tooltip:
    """Simple tooltip implementation doesn't work now, I need to figure out why."""

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
            tw, text=self.text, justify="left", background="#ffffff", relief="solid", borderwidth=1, font=("Arial", 10)
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


class Sidebar:
    def __init__(
        self, parent, chip_images_path="chips", canvas=None, board=None, sketcher=None, component_data=None
    ) -> None:
        """
        Initializes the sidebar.
        """
        self.parent = parent

        images = self.load_chip_images(chip_images_path)
        self.available_chips_and_imgs: dict[str, Tuple[Chip, tk.PhotoImage | None]] = {
            name: (chip, images.get(chip.package_name)) for name, chip in get_all_available_chips().items()
        }

        self.canvas = canvas
        self.board = board
        self.sketcher: ComponentSketcher = sketcher
        self.component_data = component_data
        self.selected_chip_name = None
        self.chip_cursor_image = None

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
                except Exception as e:
                    print(f"Error loading image '{filename}': {e}")
                    messagebox.showwarning("Image Load Error", f"Failed to load '{filename}'.")
        return images_dict

    def create_search_bar(self):
        """
        Creates the search bar at the top of the sidebar.
        """
        # Frame for search components
        search_frame = tk.Frame(self.sidebar_frame, bg="#333333")
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
            chips_label_frame, text="Available Chips", bg="#333333", fg="#479dff", font=("Arial", 10, "bold")
        )
        chips_label.pack(anchor="w")

        # Creating a canvas for chips with a vertical scrollbar
        self.canvas_chips = tk.Canvas(self.sidebar_frame, bg="#333333", highlightthickness=0, bd=0)
        self.canvas_chips.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Adding a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.canvas_chips.yview)
        scrollbar.grid(row=2, column=0, sticky="nse")

        self.canvas_chips.configure(yscrollcommand=scrollbar.set)

        # Creating a frame inside the canvas to hold chip buttons
        self.chips_inner_frame = tk.Frame(self.canvas_chips, bg="#333333")
        self.canvas_chips.create_window((0, 0), window=self.chips_inner_frame, anchor="nw")

        # Binding the configure event to update the scrollregion
        self.chips_inner_frame.bind(
            "<Configure>", lambda event: self.canvas_chips.configure(scrollregion=self.canvas_chips.bbox("all"))
        )

        # Defining grid properties
        self.columns = 2  # Number of columns in the grid
        self.visible_rows = 12  # Number of rows visible without scrolling
        self.grid_capacity = self.columns * self.visible_rows  # Total slots visible

        # Displaying chips
        self.display_chips(self.available_chips_and_imgs)

    def display_chips(self, chips: dict[str, Tuple[Chip, tk.PhotoImage]]):
        """
        Displays chip buttons in the chips_inner_frame.
        """
        # Clearing existing chips
        for widget in self.chips_inner_frame.winfo_children():
            widget.destroy()

        # Calculating the number of slots based on grid_capacity
        total_slots = self.grid_capacity

        # Limiting the number of chips displayed to grid_capacity for initial display
        # display_chips = chips[:total_slots]
        display_chips = chips.items()
        firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=12)
        # Displaying existing chips
        for index, (chip_name, (_, chip_image)) in enumerate(display_chips):
            row = index // self.columns
            col = index % self.columns
            btn = tk.Button(
                self.chips_inner_frame,
                image=chip_image,
                text=chip_name,
                compound="top",
                font=firaCodeFont,
                fg="white",  # Set text color to white
                bg="#333333",
                activebackground="#479dff",
                relief="flat",
                command=lambda name=chip_name: self.select_chip(name),
                width=100,  # Fixed width to match image size
                height=60,  # Fixed height to match image size
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            Tooltip(btn, chip_name)  # Adding tooltip with chip name

            # Binding hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#479dff"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#333333"))



    def create_manage_button(self):
        """
        Creates the 'Manage Components' button at the bottom of the sidebar without an icon.
        """
        manage_button = tk.Button(
            self.sidebar_frame,
            text="Manage Components",
            bg="#333333",  # Matching the sidebar's background to simulate transparency
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            borderwidth=0,
            command=self.manage_components,
        )
        manage_button.grid(row=3, column=0, padx=10, pady=5, sticky="we")

    def select_chip(self, chip_name):
        """
        Handler for selecting a chip.
        """
        # Cancel any ongoing chip placement
        self.cancel_chip_placement()

        # Set the new selected chip
        self.selected_chip_name = chip_name
        self.start_chip_placement(chip_name)

    def start_chip_placement(self, chip_name):
        """
        Initiates the chip placement process by changing the cursor to the chip image.
        """
        # Get the chip image
        self.chip_cursor_image = self.available_chips_and_imgs.get(chip_name)[1]

        # Keep a reference to the image to prevent garbage collection
        self.canvas.chip_cursor_image = self.chip_cursor_image

        # Hide the default cursor
        self.canvas.config(cursor="none")

        # Bind events to the canvas
        self.canvas.bind("<Motion>", self.canvas_on_mouse_move)
        self.canvas.bind("<Button-1>", self.canvas_on_click)
        self.canvas.bind("<Button-3>", self.cancel_chip_placement)  # Bind right-click to cancel

        print(f"Started placement for chip: {chip_name}")

    def cancel_chip_placement(self, event=None):
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

        # Reset the selected chip
        print(f"Chip {self.selected_chip_name} placed.")
        self.selected_chip_name = None
        self.chip_cursor_image = None

    def place_chip_at(self, x, y, chip_name):
        """
        Places the selected chip on the breadboard at the nearest grid point.
        """
        # Find the nearest grid point
        (nearest_x, nearest_y), (column, line) = self.sketcher.find_nearest_grid(x, y, matrix=matrix1260pts)
        print(f"Nearest grid point: {nearest_x}, {nearest_y}, Column: {column}, Line: {line}")

        if column is None or line is None:
            messagebox.showerror("Placement Error", "No grid point found nearby.")
            return

        # Adjust for scaling and origin
        scale = self.sketcher.scale_factor
        xO, yO = id_origins["xyOrigin"]

        # # Use goXY to get the exact position
        # exact_x, exact_y = self.sketcher.goXY(
        #     xO,
        #     yO,
        #     scale=scale,
        #     width=-1,
        #     column=column,
        #     line=line
        # )

        available_chips = get_all_available_chips()  # FIXME valeur devrait être chargée au démarrage

        try:
            chip_dict = available_chips.get(chip_name).to_generic_dict()
        except AttributeError as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Unknown chip: {chip_name}")
            return

        chip_dict["internalFunc"] = self.sketcher.internalFunc
        chip_dict["open"] = 0
        chip_dict["logicFunction"] = self.sketcher.drawSymb(chip_dict["logicFunctionName"])

        chip_model = [
            (
                self.sketcher.drawChip,
                1,
                chip_dict,
            )
        ]

        if chip_model:
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

                hole_top = matrix1260pts.get(hole_id_top)
                hole_bottom = matrix1260pts.get(hole_id_bottom)

                if hole_top["etat"] != FREE or hole_bottom["etat"] != FREE:
                    holes_available = False
                    break
                else:
                    occupied_holes.extend([hole_id_top, hole_id_bottom])

            if not holes_available:
                print("Holes are occupied. Cannot place the chip here.")
                self.cancel_chip_placement()
                return

            else:
                # Mark new holes as used
                for hole_id in occupied_holes:
                    matrix1260pts[hole_id]["etat"] = USED
                model_chip = [(chip_model, 1, {"XY": (nearest_x, nearest_y), "pinUL_XY": (pin_x, pin_y)})]
                self.sketcher.circuit(nearest_x, nearest_y, scale=scale, model=model_chip)
                print(f"Chip {chip_name} placed at ({column}, {line}).")

                # Update the current_dict_circuit with the new chip
                chip_keys = [key for key in current_dict_circuit.keys() if key.startswith("_chip")]
                if chip_keys:
                    last_chip_key = chip_keys[-1]  # Get the last key in sorted order
                    added_chip_params = current_dict_circuit[last_chip_key]
                    print("Last chip parameter:", added_chip_params)
                    added_chip_params["occupied_holes"] = occupied_holes
                else:
                    # delete the chip
                    print("need to delete the added chip")

    def manage_components(self):
        """
        Handler for the 'Manage Components' button.
        """
        messagebox.showinfo("Manage Components", "Manage Components functionality not implemented yet.")

    def on_search(self, event):
        """
        Filters the displayed chips based on the search query.
        """
        query = self.search_entry.get().lower()
        if not query:
            filtered_chips = self.available_chips_and_imgs
        else:
            filtered_chips = {
                name: chip_data
                for name, chip_data in self.available_chips_and_imgs.items()
                if query in name.lower()
                or query in chip_data[0].package_name.lower()
                or any(query in func.__class__.__name__.lower() for func in chip_data[0].functions)
            }
        self.display_chips(filtered_chips)
