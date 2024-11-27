"""
This module defines the `Menus` class for creating a custom menu bar in a Tkinter application.
The menu bar includes options for file operations, controller selection, port configuration, and help documentation.
"""

from copy import deepcopy

from dataclasses import dataclass
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import subprocess
import platform
from typing import Callable
import serial.tools.list_ports  # type: ignore

from breadboard import Breadboard

from dataCDLT import INPUT, OUTPUT, USED, CLOCK

MICROCONTROLLER_PINS = {
    "Arduino Mega": {
        "input_pins": [22, 23, 24, 25, 26, 27, 28, 29],
        "output_pins": [32, 33, 34, 35, 36, 37],
        "clock_pin": 2,
    },
    "Arduino Uno": {
        "input_pins": [2, 3, 4, 5, 6, 7, 8, 9],
        "output_pins": [10, 11, 12, 13],
        "clock_pin": 2,
    },
    "Arduino Micro": {
        "input_pins": [2, 3, 4, 5, 6, 7, 8, 9],
        "output_pins": [10, 11, 12, 13],
        "clock_pin": 2,
    },
    "Arduino Mini": {
        "input_pins": [2, 3, 4, 5, 6, 7, 8, 9],
        "output_pins": [10, 11, 12, 13],
        "clock_pin": 2,
    },
    "STM32": {
        "input_pins": ["PA0", "PA1", "PA2", "PA3", "PB0", "PB1", "PB2", "PB3"],
        "output_pins": ["PC0", "PC1", "PC2", "PC3", "PC4", "PC5"],
        "clock_pin": "PA0",
    },
    "NodeMCU ESP8266": {
        "input_pins": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"],
        "output_pins": ["D0", "D1", "D2", "D3", "D4", "D5"],
        "clock_pin": "D2",
    },
    "NodeMCU ESP32": {
        "input_pins": [32, 33, 34, 35, 25, 26, 27, 14],
        "output_pins": [23, 22, 21, 19, 18, 5],
        "clock_pin": 2,
    },
}


@dataclass
class SerialPort:
    """Data class representing the info for a serial port."""

    com_port: str | None
    """The COM port to connect to."""
    baud_rate: int
    """The baud rate for the port."""
    timeout: int
    """The timeout for the port."""
    connection: serial.Serial | None
    """The serial connection object."""


class Menus:
    """
    Menus class for creating a custom menu bar in a Tkinter application.
    Attributes:
        parent (tk.Tk | tk.Frame): The main window or parent frame.
        canvas (tk.Canvas): The canvas widget for drawing circuits.
        board (Breadboard): The Breadboard instance.
        current_dict_circuit (dict): The current circuit data.
        com_port (str | None): The selected COM port.
    """

    def __init__(
        self,
        parent: tk.Tk | tk.Frame,
        canvas: tk.Canvas,
        board: Breadboard,
        current_dict_circuit: dict,
    ):
        """
        Initializes the custom menu bar.

        Parameters:
        - parent (tk.Tk or tk.Frame): The main window or parent frame.
        - canvas (tk.Canvas): The canvas widget for drawing circuits.
        - board (Breadboard): The Breadboard instance.
        """
        self.parent: tk.Tk | tk.Frame = parent
        """The main window or parent frame."""
        self.canvas: tk.Canvas = canvas
        """The canvas widget for drawing circuits."""
        self.board: Breadboard = board
        """The Breadboard instance."""
        self.current_dict_circuit: dict = current_dict_circuit
        """The current circuit data."""
        self.com_port: str | None = None
        """The selected COM port."""
        self.selected_microcontroller = None
        """The selected microcontroller."""

        self.menu_bar = tk.Frame(parent, bg="#333333")
        """The frame containing the menu bar buttons."""

        self.serial_port = SerialPort(None, 115200, 1, None)
        """The serial port configuration."""

        # Define menu items and their corresponding dropdown options
        menus = {
            "Fichier": ["Nouveau", "Ouvrir", "Enregistrer", "Quitter"],
            "Microcontrôleur": ["Choisir un microcontrôleur", "Table de correspondance", "Configurer le port série"],
            "Exporter": ["Vérifier", "Téléverser"],
            "Aide": ["Documentation", "À propos"],
        }

        menu_commands = {
            "Nouveau": self.new_file,
            "Ouvrir": self.open_file,
            "Enregistrer": self.save_file,
            "Quitter": self.parent.quit,
            "Configurer le port série": self.configure_ports,
            "Table de correspondance": self.show_correspondence_table,
            "Choisir un microcontrôleur": self.select_microcontroller,
            "Documentation": self.open_documentation,
            "À propos": self.about,
        }

        for menu_name, options in menus.items():
            self.create_menu(menu_name, options, menu_commands)

        # Display selected microcontroller label
        self.microcontroller_label = tk.Label(
            self.menu_bar,
            text="(Aucun microcontrôleur n'est choisi)",
            bg="#333333",
            fg="white",
            font=("FiraCode-Bold", 12),
        )
        self.microcontroller_label.pack(side="right", padx=10)

        # Bind to parent to close dropdowns when clicking outside
        self.parent.bind("<Button-1>", self.close_dropdown, add="+")
        self.canvas.bind("<Button-1>", self.close_dropdown, add="+")

    def select_microcontroller(self):
        """Handler for microcontroller selection."""
        # Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Choisir un microcontrôleur")

        # Set the size and position of the dialog
        dialog.geometry("300x150")

        # Create a label for the combobox
        label = tk.Label(dialog, text="Choisir:")
        label.pack(pady=10)
        available_microcontrollers = list(MICROCONTROLLER_PINS.keys())
        # Create a combobox with the options
        combobox = ttk.Combobox(dialog, values=available_microcontrollers)
        combobox.pack(pady=10)

        # Create a button to confirm the selection
        def confirm_selection():
            selected_option = combobox.get()
            print(f"Selected option: {selected_option}")
            self.selected_microcontroller = selected_option
            print(f"{selected_option} selected.")
            # Update the label text
            self.microcontroller_label.config(text=self.selected_microcontroller)
            dialog.destroy()

        confirm_button = tk.Button(dialog, text="Confirmer", command=confirm_selection)
        confirm_button.pack(pady=10)

    def show_correspondence_table(self):
        """Displays the correspondence table between pin_io objects and microcontroller pins in a table format."""
        if self.selected_microcontroller is None:
            messagebox.showwarning("Aucun microcontrôleur sélectionné", "Veuillez d'abord sélectionner un microcontrôleur.")
            return

        pin_mappings = MICROCONTROLLER_PINS.get(self.selected_microcontroller)
        if not pin_mappings:
            messagebox.showerror("Erreur", f"Aucun mappage de broches trouvé pour {self.selected_microcontroller}.")
            return

        input_pins = pin_mappings["input_pins"]
        output_pins = pin_mappings["output_pins"]

        # Gather pin_io objects from current_dict_circuit
        pin_ios = [value for key, value in self.current_dict_circuit.items() if key.startswith("_io_")]

        # Separate pin_ios into inputs, outputs, and clocks
        input_pin_ios = [pin for pin in pin_ios if pin["type"] == INPUT]
        output_pin_ios = [pin for pin in pin_ios if pin["type"] == OUTPUT]
        clock_pin_ios = [pin for pin in pin_ios if pin["type"] == CLOCK]

        # Ensure only one CLOCK type
        if len(clock_pin_ios) > 1:
            messagebox.showerror("Erreur d'horloge", "Une seule HORLOGE est autorisée.")
            return

        # Check pin counts
        if len(input_pin_ios) > len(input_pins):
            messagebox.showerror(
                "Trop d'entrées",
                f"Vous avez {len(input_pin_ios)} broches d'entrée, mais seulement "
                f"{len(input_pins)} broches d'entrée disponibles sur le microcontrôleur.",
            )
            return
        if len(output_pin_ios) > len(output_pins):
            messagebox.showerror(
                "Trop de sorties",
                f"Vous avez {len(output_pin_ios)} broches de sortie, mais seulement "
                f"{len(output_pins)} broches de sortie disponibles sur le microcontrôleur.",
            )
            return

        # Create a new window for the correspondence table
        table_window = tk.Toplevel(self.parent)
        table_window.title("Correspondence Table")
        table_window.geometry("500x350")

        # Create a Treeview widget for the table
        tree = ttk.Treeview(table_window, columns=("ID", "Type", "MCU Pin"), show="headings", height=15)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Define columns and headings
        tree.column("ID", anchor="center", width=120)
        tree.column("Type", anchor="center", width=120)
        tree.column("MCU Pin", anchor="center", width=120)
        tree.heading("ID", text="Pin IO ID")
        tree.heading("Type", text="Type")
        tree.heading("MCU Pin", text="MCU Pin")

        # Populate the table with input, output, and clock pin mappings
        for idx, pin_io in enumerate(input_pin_ios):
            mcu_pin = input_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "Input", mcu_pin))

        for idx, pin_io in enumerate(output_pin_ios):
            mcu_pin = output_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "Output", mcu_pin))

        if clock_pin_ios:
            clock_pin = pin_mappings["clock_pin"]
            pin_number = clock_pin_ios[0]["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "clk input", clock_pin))

        # Add a scrollbar if the list gets too long
        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Show the table in the new window
        table_window.transient(self.parent)  # Set to be on top of the parent window
        table_window.grab_set()  # Prevent interaction with the main window until closed
        table_window.mainloop()

    def create_menu(self, menu_name, options, menu_commands):
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
            command=lambda m=menu_name: self.toggle_dropdown(m),
            borderwidth=0,
            highlightthickness=0,
        )
        btn.pack(side="left")

        # Create the dropdown frame
        dropdown = tk.Frame(self.parent, bg="#333333", bd=1, relief="solid", width=250)

        # Calculate dropdown height based on number of options
        button_height = 30  # Approximate height of each dropdown button
        dropdown_height = button_height * len(options)
        dropdown.place(x=0, y=0, width=250, height=dropdown_height)  # Initial size based on options
        dropdown.place_forget()  # Hide initially

        def select_menu_item(option):
            """Wrapper function to close dropdown and execute the menu command."""
            self.close_dropdown(None)
            menu_commands.get(option, lambda: print(f"{option} selected"))()

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
                width=250,
                padx=20,
                pady=5,
                font=("FiraCode-Bold", 12),
                command=lambda o=option: select_menu_item(o),
                borderwidth=0,
                highlightthickness=0,
            )
            option_btn.pack(fill="both")

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
            if isinstance(child, tk.Button) and hasattr(child, "dropdown"):
                if child["text"] == menu_name:
                    if child.dropdown.winfo_ismapped():
                        child.dropdown.place_forget()
                    else:
                        # Position the dropdown below the button
                        btn_x = child.winfo_rootx() - self.parent.winfo_rootx()
                        btn_y = child.winfo_rooty() - self.parent.winfo_rooty() + child.winfo_height()
                        child.dropdown.place(x=btn_x, y=btn_y, width=250)
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
        if (
            event is None
            or not self.is_descendant(event.widget, self.menu_bar)
            and not any(
                self.is_descendant(event.widget, child.dropdown)
                for child in self.menu_bar.winfo_children()
                if isinstance(child, tk.Button) and hasattr(child, "dropdown")
            )
        ):
            for child in self.menu_bar.winfo_children():
                if isinstance(child, tk.Button) and hasattr(child, "dropdown"):
                    child.dropdown.place_forget()

    # Menu Handler Functions
    def new_file(self):
        """Handler for the 'New' menu item."""
        # Clear the canvas and reset the circuit
        self.board.sketcher.clear_board()
        self.board.fill_matrix_1260_pts()
        self.board.draw_blank_board_model()

        print("New file created.")
        messagebox.showinfo("Nouveau fichier", "Un nouveau circuit a été créé.")

    def open_file(self):
        """Handler for the 'Open' menu item."""
        print("Open File")
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    circuit_data = json.load(file)
                print(f"Circuit loaded from {file_path}")
                self.board.sketcher.clear_board()

                x_o, y_o = self.board.sketcher.id_origins["xyOrigin"]
                self.board.sketcher.circuit(x_o, y_o, model=[])

                battery_pos_wire_end = None
                battery_neg_wire_end = None

                for key, val in circuit_data.items():
                    if key == "_battery_pos_wire":
                        battery_pos_wire_end = val['end']
                    elif key == "_battery_neg_wire":
                        battery_neg_wire_end = val['end']

                self.board.draw_blank_board_model(
                    x_o,
                    y_o,
                    battery_pos_wire_end=battery_pos_wire_end,
                    battery_neg_wire_end=battery_neg_wire_end,
                )

                for key, val in circuit_data.items():
                    if "chip" in key:
                        self.load_chip(val)

                    elif "wire" in key and not key.startswith("_battery"):
                        self.load_wire(val)

                    elif "io" in key:
                        self.load_io(val)

                    else:

                        print(f"Unspecified component: {key}")
                messagebox.showinfo("Ouvrir un fichier", f"Circuit chargé depuis {file_path}")
            except Exception as e:
                print(f"Error loading file: {e}")
                messagebox.showerror("Erreur d'ouverture", f"Une erreur s'est produite lors de l'ouverture du fichier:\n{e}")
                raise e
        else:
            print("Open file cancelled.")

    def load_chip(self, chip_data):
        """Load a chip from the given chip_data."""
        x, y = chip_data["XY"]
        model_chip = [
            (
                self.board.sketcher.draw_chip,
                1,
                {
                    **chip_data,
                    "matrix": self.board.sketcher.matrix,
                },
            )
        ]
        self.board.sketcher.circuit(x, y, model=model_chip)
        new_chip_id = self.current_dict_circuit["last_id"]

        (_, _), (column, line) = self.board.sketcher.find_nearest_grid(x, y, matrix=self.board.sketcher.matrix)
        occupied_holes = []
        for i in range(chip_data["pinCount"] // 2):
            # Top row (line 7 or 21)
            hole_id_top = f"{column + i},{line}"
            # Bottom row (line 6 or 20)
            hole_id_bottom = f"{column + i},{line + 1}"
            occupied_holes.extend([hole_id_top, hole_id_bottom])
        self.current_dict_circuit[new_chip_id]["occupied_holes"] = occupied_holes

    def load_wire(self, wire_data):
        """Load a wire from the given wire_data."""
        x_o, y_o = self.board.sketcher.id_origins["xyOrigin"]
        model_wire = [
            (
                self.board.sketcher.draw_wire,
                1,
                {
                    **wire_data,
                    "matrix": self.board.sketcher.matrix,
                },
            )
        ]
        self.board.sketcher.circuit(x_o, y_o, model=model_wire)

    def load_io(self, io_data):
        """Load an input/output component from the given io_data."""
        x_o, y_o = self.board.sketcher.id_origins["xyOrigin"]
        model_io = [
            (
                self.board.sketcher.draw_pin_io,
                1,
                {
                    **io_data,
                    "matrix": self.board.sketcher.matrix,
                },
            )
        ]
        self.board.sketcher.circuit(x_o, y_o, model=model_io)

    def save_file(self):
        """Handler for the 'Save' menu item."""
        print("Save File")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                circuit_data = deepcopy(self.current_dict_circuit)

                circuit_data.pop("last_id", None)
                for key, comp_data in circuit_data.items():
                    comp_data.pop("id", None)
                    comp_data.pop("tags", None)
                    if "label" in comp_data:
                        comp_data["label"] = comp_data["type"]
                    if "wire" in key:
                        comp_data.pop("XY", None) # Remove XY, will be recalculated anyway
                    if key == "_battery":
                        comp_data.pop("battery_rect", None)
                # Save the data to a JSON file
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(circuit_data, file, indent=4)
                print(f"Circuit saved to {file_path}")
                messagebox.showinfo("Sauvegarde réussie", f"Circuit sauvegardé dans {file_path}")
            except (TypeError, KeyError) as e:
                print(f"Error saving file: {e}")
                messagebox.showerror("Erreur de sauvegarde", f"Une erreur s'est produite lors de la sauvegarde du fichier:\n{e}")
        else:
            print("Save file cancelled.")

    def configure_ports(self):
        """Handler for the 'Configure Ports' menu item."""
        print("Configure Ports")
        options = [comport.device for comport in serial.tools.list_ports.comports()]
        if len(options) == 0:
            message = "No COM ports available. Please connect a device and try again."
            print(message)
            messagebox.showwarning("Pas de ports COM", message)
        else:
            dialog = tk.Toplevel(self.parent)
            dialog.title("Configure Ports")

            dialog.geometry("300x150")

            label = tk.Label(dialog, text="Select an option:")
            label.pack(pady=10)
            combobox = ttk.Combobox(dialog, values=options)
            combobox.pack(pady=10)

            def confirm_selection():
                selected_option = combobox.get()
                print(f"Selected option: {selected_option}")
                self.serial_port.com_port = selected_option
                dialog.destroy()

            confirm_button = tk.Button(dialog, text="Confirm", command=confirm_selection)
            confirm_button.pack(pady=10)

    def open_documentation(self):
        """Handler for the 'Documentation' menu item."""
        file_path = os.path.join(os.path.dirname(__file__), "Assets", "ArduinoLogique_Document_utilisateur.pdf")
        if platform.system() == "Windows":
            subprocess.Popen(["start", file_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", file_path])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(["xdg-open", file_path])

    def about(self):
        """Handler for the 'About' menu item."""
        print("About this software")
        messagebox.showinfo("À propos", "ArduinoLogique v1.0\nSimulateur de circuits logiques")

    def open_port(self):
        """Handler for the 'Open Port' menu item."""
        try:
            self.serial_port.connection = serial.Serial(
                port=self.serial_port.com_port, baudrate=self.serial_port.baud_rate, timeout=self.serial_port.timeout
            )
            print(f"Port série {self.serial_port.com_port} ouvert avec succès.")
        except serial.SerialException as e:
            print(f"Erreur lors de l'ouverture du port {self.serial_port.com_port}: {e}")

    def send_data(self, data):
        """
        Send a string of data to the microcontroller through the serial port.
        """
        if self.serial_port.connection and self.serial_port.connection.is_open:
            try:
                # Convertir la chaîne en bytes et l'envoyer
                self.serial_port.connection.write(data.encode("utf-8"))
                print(f"Données envoyées: {data}")
            except serial.SerialException as e:
                print(f"Erreur lors de l'envoi des données: {e}")
        else:
            print("Le port série n'est pas ouvert. Impossible d'envoyer les données.")

    def close_port(self):
        """Close the serial port."""
        if self.serial_port.connection and self.serial_port.connection.is_open:
            self.serial_port.connection.close()
            print(f"Port série {self.serial_port.com_port} fermé.")
        else:
            print("Le port série est déjà fermé.")

    def download_script(self, script):
        """Upload the script to the microcontroller through the serial port."""
        self.open_port()
        self.send_data(script)
        self.close_port()
