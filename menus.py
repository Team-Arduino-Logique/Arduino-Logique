# Menus.py

import tkinter as tk
from tkinter import messagebox, filedialog
import json

class Menus:
    def __init__(self, parent, canvas, board, component_data, model, current_dict_circuit, zoom_function):
        """
        Initializes the custom menu bar.

        Parameters:
        - parent (tk.Tk or tk.Frame): The main window or parent frame.
        - canvas (tk.Canvas): The canvas widget for drawing circuits.
        - board (Breadboard): The Breadboard instance.
        - component_data (ComponentData): The ComponentData instance.
        - model (list): The model data for the circuit.
        - current_dict_circuit (dict): The current circuit data.
        - zoom_function (callable): The zoom function to adjust the canvas.
        """
        self.parent = parent
        self.canvas = canvas
        self.board = board
        self.component_data = component_data
        self.model = model
        self.current_dict_circuit = current_dict_circuit
        self.zoom = zoom_function

        # Create the menu bar frame (do not pack here)
        self.menu_bar = tk.Frame(parent, bg="#333333")

        # Define menu items and their corresponding dropdown options
        self.menus = {
            "File": ["New", "Open", "Save", "Exit"],
            "Controllers": ["Arduino", "ESP32"],
            "Ports": ["Configure Ports"],
            "Help": ["Documentation", "About"]
        }

        # Mapping menu labels to their handler functions
        self.menu_commands = {
            "New": self.new_file,
            "Open": self.open_file,
            "Save": self.save_file,
            "Exit": self.parent.quit,
            "Arduino": self.Arduino,
            "ESP32": self.ESP32,
            "Configure Ports": self.configure_ports,
            "Documentation": self.open_documentation,
            "About": self.about
        }

        # Create each menu button and its dropdown
        for menu_name, options in self.menus.items():
            self.create_menu(menu_name, options)

        # Bind to parent to close dropdowns when clicking outside
        self.parent.bind("<Button-1>", self.close_dropdown)

    def create_menu(self, menu_name, options):
        """
        Creates a menu button with a dropdown.

        Parameters:
        - menu_name (str): The name of the top-level menu (e.g., "File").
        - options (list): List of options under the menu.
        """
        # Create the menu button
        btn = tk.Button(
            self.menu_bar,
            text=menu_name,
            bg="#333333",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5,
            font=("FiraCode-Bold", 12),
            command=lambda m=menu_name: self.toggle_dropdown(m)
        )
        btn.pack(side="left")

        # Create the dropdown frame
        dropdown = tk.Frame(self.parent, bg="#333333", bd=1, relief="solid")

        # Calculate dropdown height based on number of options
        button_height = 30  # Approximate height of each dropdown button
        dropdown_height = button_height * len(options)
        dropdown.place(x=0, y=0, width=150, height=dropdown_height)  # Initial size based on options
        dropdown.place_forget()  # Hide initially

        # Populate the dropdown with menu options
        for option in options:
            option_btn = tk.Button(
                dropdown,
                text=option,
                bg="#333333",
                fg="white",
                activebackground="#444444",
                activeforeground="white",
                bd=0,
                anchor="w",
                padx=20,
                pady=5,
                font=("FiraCode-Bold", 12),
                command=self.menu_commands.get(option, lambda: print(f"{option} selected"))
            )
            option_btn.pack(fill="x")

        # Attach the dropdown to the button
        btn.dropdown = dropdown

    def toggle_dropdown(self, menu_name):
        """
        Toggles the visibility of the dropdown menu corresponding to the given menu name.
        Hides other dropdowns when one is opened.

        Parameters:
        - menu_name (str): The name of the menu to toggle.
        """
        for child in self.menu_bar.winfo_children():
            if isinstance(child, tk.Button) and hasattr(child, 'dropdown'):
                if child['text'] == menu_name:
                    if child.dropdown.winfo_ismapped():
                        child.dropdown.place_forget()
                    else:
                        # Position the dropdown below the button
                        btn_x = child.winfo_rootx() - self.parent.winfo_rootx()
                        btn_y = child.winfo_rooty() - self.parent.winfo_rooty() + child.winfo_height()
                        child.dropdown.place(x=btn_x, y=btn_y, width=150)
                        print(f"Opened dropdown for {menu_name}")
                        child.dropdown.lift()  # Ensure dropdown is on top
                else:
                    child.dropdown.place_forget()

    def is_descendant(self, widget, parent):
        """
        Checks if a widget is a descendant of a parent widget.

        Parameters:
        - widget (tk.Widget): The widget to check.
        - parent (tk.Widget): The parent widget.

        Returns:
        - bool: True if widget is a descendant of parent, else False.
        """
        while widget:
            if widget == parent:
                return True
            widget = widget.master
        return False

    def close_dropdown(self, event):
        """
        Closes all dropdown menus when clicking outside the menu bar or dropdowns.

        Parameters:
        - event (tk.Event): The event object.
        """
        if not self.is_descendant(event.widget, self.menu_bar) and not any(
            self.is_descendant(event.widget, child.dropdown) for child in self.menu_bar.winfo_children()
            if isinstance(child, tk.Button) and hasattr(child, 'dropdown')
        ):
            for child in self.menu_bar.winfo_children():
                if isinstance(child, tk.Button) and hasattr(child, 'dropdown'):
                    child.dropdown.place_forget()

    # Menu Handler Functions
    def new_file(self):
        """Handler for the 'New' menu item."""
        # Clear the canvas and reset the circuit
        self.canvas.delete("all")
        self.board.fill_matrix_1260_pts()
        self.component_data = ComponentData(ComponentSketcher(self.canvas))
        self.model = self.component_data.circuitTest
        self.zoom(self.canvas, 10.0, self.board, 50, 10, self.model)
        print("New file created.")
        messagebox.showinfo("New File", "A new circuit has been created.")

    def open_file(self):
        """Handler for the 'Open' menu item."""
        print("Open File")
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    circuit_data = json.load(file)
                print(f"Circuit loaded from {file_path}")
                # Update current_dict_circuit and redraw the circuit
                self.current_dict_circuit.clear()
                self.current_dict_circuit.update(circuit_data)
                self.zoom(self.canvas, 10.0, self.board, 50, 10, self.model)
                messagebox.showinfo("Open File", f"Circuit loaded from {file_path}")
            except Exception as e:
                print(f"Error loading file: {e}")
                messagebox.showerror("Open Error", f"An error occurred while opening the file:\n{e}")
        else:
            print("Open file cancelled.")

    def save_file(self):
        """Handler for the 'Save' menu item."""
        print("Save File")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Extract the circuit data from current_dict_circuit
                circuit_data = {
                    comp_id: {
                        "XY": comp_data.get("XY"),
                        "type": comp_data.get("type"),
                        "label": comp_data.get("label"),
                        "btnMenu": comp_data.get("btnMenu"),
                        # Add other necessary attributes
                    }
                    for comp_id, comp_data in self.current_dict_circuit.items()
                }
                # Save the data to a JSON file
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(circuit_data, file, indent=4)
                print(f"Circuit saved to {file_path}")
                messagebox.showinfo("Save Successful", f"Circuit saved to {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
                messagebox.showerror("Save Error", f"An error occurred while saving the file:\n{e}")
        else:
            print("Save file cancelled.")

    def Arduino(self):
        """Handler for the 'Arduino' menu item."""
        print("Arduino")
        messagebox.showinfo("Arduino", "Arduino choice functionality not implemented yet.")

    def ESP32(self):
        """Handler for the 'ESP32' menu item."""
        print("ESP32")
        messagebox.showinfo("ESP32", "ESP32 choice functionality not implemented yet.")

    def configure_ports(self):
        """Handler for the 'Configure Ports' menu item."""
        print("Configure Ports")
        messagebox.showinfo("Configure Ports", "Configure Ports functionality not implemented yet.")

    def open_documentation(self):
        """Handler for the 'Documentation' menu item."""
        print("Open Documentation")
        messagebox.showinfo("Documentation", "Documentation not available yet.")

    def about(self):
        """Handler for the 'About' menu item."""
        print("About this software")
        messagebox.showinfo("About", "ArduinoLogique v1.0\nSimulateur de circuits logiques")