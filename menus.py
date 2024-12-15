"""
This module defines the `Menus` class for creating a custom menu bar in a Tkinter application.
The menu bar includes options for file operations, controller selection, port configuration, and help documentation.
"""

from copy import deepcopy

from dataclasses import dataclass
import os
import tkinter as tk
import json
import subprocess
import platform
import serial.tools.list_ports  # type: ignore
import time

from breadboard import Breadboard
from component_sketch import ComponentSketcher
from dataCDLT import (
    HORIZONTAL,
    RIGHT,
    VERTICAL,
    VERTICAL_END_HORIZONTAL,
    LEFT,
    PERSO,
    NO,
    AUTO,
    FREE,
    USED,
    INPUT,
    OUTPUT,
    CLOCK,
)

if (os.name in ("posix", "darwin")) and "linux" not in platform.platform().lower():
    from tkinter import messagebox, filedialog, ttk
    from tkmacosx import Button  # type: ignore
else:
    from tkinter import Button, messagebox, filedialog, ttk

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

    def connect(self):
        """Open the serial connection."""
        try:
            self.connection = serial.Serial(port=self.com_port, 
                                            baudrate=self.baud_rate, 
                                            parity=serial.PARITY_NONE, 
                                            stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS,
                                            timeout=self.timeout)
            print(f"Serial port {self.com_port} opened successfully.")
        except serial.SerialException as e:
            print(f"Error opening port {self.com_port}: {e}")


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
        sketcher: ComponentSketcher,

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
        self.sketcher = sketcher

        self.script = ""
        
        self.selected_microcontroller =  "Arduino Mega"
        """The selected microcontroller."""

        self.menu_bar = tk.Frame(parent, bg="#333333")
        """The frame containing the menu bar buttons."""
 
        self.serial_port = SerialPort(None, 9600, 1, None)
        """The serial port configuration."""

        self.open_file_path: str | None = None
        """The file path for the current open file."""

        # Define menu items and their corresponding dropdown options
        menus = {
            "Fichier": ["Nouveau", "Ouvrir", "Enregistrer", "Enregistrer sous", "Quitter"],
            "Microcontrôleur": ["Choisir un microcontrôleur", "Table de correspondance", "Configurer le port série"],
            "Circuit": [
                "Vérifier",
                "Téléverser",
            ],
            "Aide": ["Documentation", "À propos"],
        }

        menu_commands = {
            "Nouveau": self.new_file,
            "Ouvrir": self.open_file,
            "Enregistrer": lambda: self.save_file(False),
            "Enregistrer sous": self.save_file,
            "Quitter": self.parent.quit,
            "Configurer le port série": self.configure_ports,
            "Table de correspondance": self.show_correspondence_table,
            "Choisir un microcontrôleur": self.select_microcontroller,
            "Vérifier": self.checkCircuit,
            "Téléverser": self.download_script,
            "Documentation": self.open_documentation,
            "À propos": self.about,
        }

        for menu_name, options in menus.items():
            self.create_menu(menu_name, options, menu_commands)

        # Display selected microcontroller label
        self.microcontroller_label = tk.Label(
            self.menu_bar,
            text="(Aucun microcontrôleur n'est choisi)" if not self.selected_microcontroller else self.selected_microcontroller,
            bg="#333333",
            fg="white",
            font=("FiraCode-Bold", 12),
        )
        self.microcontroller_label.pack(side="right", fill="y", padx=175)

        # Bind to parent to close dropdowns when clicking outside
        self.parent.bind("<Button-1>", self.close_dropdown, add="+")
        self.canvas.bind("<Button-1>", self.close_dropdown, add="+")

        self.parent.bind("<Control-s>", lambda _: self.save_file(False), add="+")

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
        combobox.set(self.selected_microcontroller if self.selected_microcontroller else "Choisir un microcontrôleur")
        combobox.pack(pady=10)
        
        default_option = "Arduino Mega"  # Changez ceci selon votre choix
        combobox.set(default_option)   # Définit l'option par défaut
        # Create a button to confirm the selection
        def confirm_selection():
            selected_option = combobox.get()
            print(f"Selected option: {selected_option}")
            self.selected_microcontroller = selected_option
            print(f"{selected_option} selected.")
            # Update the label text
            self.microcontroller_label.config(text=self.selected_microcontroller)
            dialog.destroy()

        confirm_button = Button(dialog, text="Confirmer", command=confirm_selection)
        confirm_button.pack(pady=10)
        
    # def map_mcu_pin(self, treeview=None, input_pin_ios, output_pin_ios, input_pins, output_pins):
    #     # Populate the table with input and output pin mappings
    #     self.mcu_pin= {}
    #     for idx, pin_io in enumerate(input_pin_ios):
    #         mcu_pin = input_pins[idx]
    #         pin_number = pin_io["id"].split("_")[-1]
    #         treeview.insert("", "end", values=(pin_number, "Input", mcu_pin))
    #         self.mcu_pin.update({f"I{pin_number}":f"I{mcu_pin}"})
            

    #     for idx, pin_io in enumerate(output_pin_ios):
    #         mcu_pin = output_pins[idx]
    #         pin_number = pin_io["id"].split("_")[-1]
    #         treeview.insert("", "end", values=(pin_number, "Output", mcu_pin))
    #         self.mcu_pin.update({f"O{pin_number}":f"O{mcu_pin}"})
            
    def show_correspondence_table(self, show=True):
        """Displays the correspondence table between pin_io objects and microcontroller pins in a table format."""
        if self.selected_microcontroller is None:
            messagebox.showwarning(
                "Aucun microcontrôleur sélectionné", "Veuillez d'abord sélectionner un microcontrôleur."
            )
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
        table_window.withdraw()
        table_window.title("Table de correspondance")
        table_window.geometry("500x350")

        # if show:
        # Create a Treeview widget for the table
        tree = ttk.Treeview(table_window, columns=("ID", "Type", "MCU Pin"), show="headings", height=15)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Define columns and headings
        tree.column("ID", anchor="center", width=120)
        tree.column("Type", anchor="center", width=120)
        tree.column("MCU Pin", anchor="center", width=120)
        tree.heading("ID", text="Id de l'entrée/sortie")
        tree.heading("Type", text="Type")
        tree.heading("MCU Pin", text="Pin du microcontrôleur")

        #self.map_mcu_pin(tree, input_pin_ios, output_pin_ios, input_pins, output_pins)
        # Populate the table with input and output pin mappings
        self.mcu_pin= {}
        for idx, pin_io in enumerate(input_pin_ios):
            mcu_pin = input_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            # if show:
            tree.insert("", "end", values=(pin_number, "Entrée", mcu_pin))
            self.mcu_pin.update({f"I{pin_number}":f"I{mcu_pin}"})
            

        for idx, pin_io in enumerate(output_pin_ios):
            mcu_pin = output_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "Sortie", mcu_pin))
            self.mcu_pin.update({f"O{pin_number}":f"O{mcu_pin}"})

        if show:
            table_window.deiconify() 
            # Add a scrollbar if the list gets too long
            scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
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
        btn = Button(
            self.menu_bar,
            text=menu_name,
            bg="#333333",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            highlightbackground="#333333",  # Border color when inactive
            highlightcolor="#444444",  # Border color when active
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
            option_btn = Button(
                dropdown,
                text=option,
                bg="#333333",
                fg="white",
                activebackground="#444444",
                activeforeground="white",
                highlightbackground="#333333",  # Border color when inactive
                highlightcolor="#444444",  # Border color when active
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
            if isinstance(child, Button) and hasattr(child, "dropdown"):
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
                if isinstance(child, Button) and hasattr(child, "dropdown")
            )
        ):
            for child in self.menu_bar.winfo_children():
                if isinstance(child, Button) and hasattr(child, "dropdown"):
                    child.dropdown.place_forget()

    # Menu Handler Functions
    def new_file(self):
        """Handler for the 'New' menu item."""
        # Clear the canvas and reset the circuit
        self.open_file_path = None
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
                        battery_pos_wire_end = val["end"]
                    elif key == "_battery_neg_wire":
                        battery_neg_wire_end = val["end"]

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
                self.open_file_path = file_path
            except Exception as e:
                print(f"Error loading file: {e}")
                messagebox.showerror(
                    "Erreur d'ouverture", f"Une erreur s'est produite lors de l'ouverture du fichier:\n{e}"
                )
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

    def save_file(self, prompt_for_path: bool = True):
        """Handler for the 'Save' menu item."""
        print("Save File")
        if prompt_for_path or not self.open_file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
        else:
            file_path = self.open_file_path
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
                        comp_data.pop("XY", None)  # Remove XY, will be recalculated anyway
                    if key == "_battery":
                        comp_data.pop("battery_rect", None)
                # Save the data to a JSON file
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(circuit_data, file, indent=4)
                print(f"Circuit saved to {file_path}")
                messagebox.showinfo("Sauvegarde réussie", f"Circuit sauvegardé dans {file_path}")
                self.open_file_path = file_path
            except (TypeError, KeyError) as e:
                print(f"Error saving file: {e}")
                messagebox.showerror(
                    "Erreur de sauvegarde", f"Une erreur s'est produite lors de la sauvegarde du fichier:\n{e}"
                )
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

            confirm_button = Button(dialog, text="Confirm", command=confirm_selection)
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

    def send_data(self, data):
        """
        Send a string of data to the microcontroller through the serial port.
        """
        if self.serial_port.connection and self.serial_port.connection.is_open:
            try:
                # Convertir la chaîne en bytes et l'envoyer
                self.serial_port.connection.write(data.encode('utf-8'))
                print(f"Données envoyées: {data}")
                #time.sleep(0.5) 
                #if self.serial_port.connection.in_waiting > 0:  # Vérifie s'il y a des données disponibles
                data = self.serial_port.connection.readline().decode('utf-8').strip() 
                print(f"réponse: {data} à {self.serial_port.baud_rate} bauds")
            except serial.SerialException as e:
                print(f"Erreur lors de l'envoi des données: {e}")
        else:
            print("Le port série n'est pas ouvert. Impossible d'envoyer les données.")

    def close_port(self):
        """Upload the script to the microcontroller through the serial port."""
        if self.serial_port.connection and self.serial_port.connection.is_open:
            self.serial_port.connection.close()
            print(f"Port série {self.serial_port.com_port} fermé.")
        else:
            print("Le port série est déjà fermé.")
            
    def download_script(self):
        self.checkCircuit()
        self.serial_port.connect()
        self.send_data(self.script)
        #self.close_port()
        
    def is_linked_to(self, dest, src):
        res = False
        c, l = src
        for zone in dest:
            c1, l1,c2, l2 = zone
            if (c >= c1 and c<= c2 and l >= l1 and l<= l2):
                res = True
                break
        return res
    
    def decodeFunc(self,inVar, funcName):
        s =""
        if funcName == "NandGate":
            s = f"!( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"& {v['val']} "
            s += ") "
        elif funcName == "AndGate":
            s = f"( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"& {v['val']} "
            s += ") "   
        elif funcName == "NorGate":
            s = f"! ( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"| {v['val']} "
            s += ") "         
        elif funcName == "OrGate":
            s = f"( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"| {v['val']} "
            s += ") "         
        elif funcName == "NotGate":
            s = f"! {inVar[0]['val']} "
        elif funcName == "XorGate":
            s = f"( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"^ {v['val']} "
            s += ") "  
        elif funcName == "XnorGate":
            s = f"! ( {inVar[0]['val']} "
            for v in inVar[1:]:
                s += f"| {v['val']} "
            s += ") "  
        elif funcName == "Mux":  
            e =["( ","( ","( ","( ","( ","( ","( ","( "]
            for v in range(8):
                v2, v1, v0  = (v & 1)^1, ((v & 2) >> 1)^1, ((v & 4) >> 2)^1
                e[v] += inVar[v]['val'] + " & " + inVar[11]["einv"] + " & " + \
                        v0*" !" + inVar[8]["sel"] + " & " + v1*" !" + inVar[9]["sel"] + " & " + v2*" !" + inVar[10]["sel"] + " ) "
            s = " ( " + e[0]
            for et in e[1:]:
                s += "| " + et
            s += " ) "
        elif funcName == "Demux":  
            s ="("
            out = inVar[0]['numO']
            v2, v1, v0  = (out & 1)^1, ((out & 2) >> 1)^1, ((out & 4) >> 2)^1
            s += v0*" !" + inVar[0]['val'] + " & " + v1*"!" + inVar[1]['val'] + " & " + v2*"!" + inVar[2]['val'] + \
                 " & " + inVar[3]["einv"] + " & " + inVar[4]["einv"] + " & " + inVar[5]["enb"]
            s += " ) "
        elif funcName == "DFlipFlop":  
            s ="("
            s += inVar[0]['val'] + " & CLK & " + inVar[3]['iset'] + " & " + inVar[2]['irst'] + " | !" + inVar[3]['iset']
            s += " ) "
        elif funcName == "JKFlipFlop":  
            if inVar[4].get('iK'): 
                    K = f"!{inVar[4]['iK']}"
            else:   K = inVar[4]["K"]
            if inVar[1].get('clk'): 
                    CLK = f"{inVar[1]['clk']} "
            else:   CLK = f"!{inVar[3]['iclk']} "
            if inVar[3].get('iset'): 
                    set = f"!{inVar[3]['iset']}"
                    iset = f"{inVar[3]['iset']}"
                    rst = f"!{inVar[2]['irst']}"
            else:   
                    set = f"!{inVar[2]['iset']}"
                    iset = f"{inVar[2]['iset']}"
                    rst = f"!{inVar[1]['irst']}"
            sT =f"T{self.varTempNum} = "
            sT += "((" + inVar[0]['J'] + f" & !T{self.varTempNum}_precedent) | (!{K} & T{self.varTempNum}_precedent)) & {set} & {rst} & CLK | {iset} " 
            sT += " ); "
            s = inVar[0]['numO']*" !" + f"T{self.varTempNum} "
            self.varTempNum +=1
            self.varScript += [sT]
        elif funcName == "BinaryCounter": 
            if inVar[0]['numO'] == 0:
                self.numTemp = []
                CE = inVar[6]["CE"]
                iU = inVar[8]["iU"]
                iL = inVar[7]["iL"]
                D0 = inVar[0]["val"]
                D1 = inVar[1]["val"]
                D2 = inVar[0]["val"]
                D3 = inVar[0]["val"]
                sT = f"T{self.varTempNum} = clk & {CE} & {iL} & !T{self.varTempNum}_precedent | !{iL} & {D0} & clk | !{CE} & {iL} & clk & T{self.varTempNum}_precedent; "
                self.numTemp += [self.varTempNum]
                self.varTempNum +=1
                self.varScript += [sT]
                sT = f"T{self.varTempNum} = (!{CE} | !T{self.varTempNum-1}_precedent | !T{self.varTempNum}_precedent) & " \
                    + f"({CE} & T{self.varTempNum - 1}_precedent | T{self.varTempNum}_precedent ) & {iL} & clk  | !{iL} & {D1} & clk | !{CE} & {iL} & clk & T{self.varTempNum}_precedent; "
                self.numTemp += [self.varTempNum]
                self.varTempNum +=1
                self.varScript += [sT]
                sT = f"T{self.varTempNum} = (!{CE} | !T{self.varTempNum-2}_precedent | !T{self.varTempNum-1}_precedent | !T{self.varTempNum}_precedent) & clk & " \
                    + f"({CE} & T{self.varTempNum - 2}_precedent & T{self.varTempNum - 1}_precedent | T{self.varTempNum}_precedent ) & {iL} & clk  | !{iL} & {D2} & clk  | !{CE} & {iL} & clk  & T{self.varTempNum}_precedent; "
                self.numTemp += [self.varTempNum]
                self.varTempNum +=1
                self.varScript += [sT]
                sT = f"T{self.varTempNum} = (!{CE} | !T{self.varTempNum-3}_precedent  | !T{self.varTempNum-2}_precedent | !T{self.varTempNum-1}_precedent | !T{self.varTempNum}_precedent) & " \
                    + f"({CE} & T{self.varTempNum - 3}_precedent & T{self.varTempNum - 2}_precedent & T{self.varTempNum - 1}_precedent | T{self.varTempNum}_precedent ) & {iL} & clk  | !{iL} & {D3} & clk  | !{CE} & {iL} & clk  & T{self.varTempNum}_precedent; "
                self.numTemp += [self.varTempNum]
                self.varTempNum +=1
                self.varScript += [sT]
            s = f"T{self.numTemp[inVar[0]['numO']]} " 

        return s                 
    
    def checkCloseCircuit(self, ioOut, params={}):
        #id, (c1,l1,c2,l2)  = ioOut 
        id, [ioZone] = ioOut
        #ioZone = [(c1,l1,c2,l2)]
        chip_select = params.get("chip_select", [])
        chip_out_inv =  params.get("chip_out_inv", [])
        chip_in_enable = params.get("chip_in_enable", [])
        chip_in_enable_inv =  params.get("chip_in_enable_inv", [])
        chip_in_clock =  params.get("chip_in_clock", [])
        chip_in_inv_reset = params.get("chip_in_inv_reset", [])
        chip_in_inv_set = params.get("chip_in_inv_set", [])   
        chip_in_inv_clock = params.get("chip_in_inv_clock", [])   
        chip_in_j = params.get("chip_in_j", [])
        chip_in_k = params.get("chip_in_k", [])
        chip_in_inv_k = params.get("chip_in_inv_k", [])
        
        chip_in_ce = params.get("count_enable_pin", [])
        chip_in_inv_L = params.get("inv_load_enable_pin", [])
        chip_in_inv_U = params.get("inv_up_down_input_pin", [])
        chip_out_TC = params.get("terminal_count_pin", [])  
              
        findOut = False
        circuitClose = True
        script = ""
        #chip_out_checked = []
        
        for nf,f in enumerate(self.func):
            idOut, inLst, fName, outLst = deepcopy(f)
            if chip_select:
                  chipSel = chip_select  
                  chipSel = [list(chipS[1:]) for chipS in chipSel if chipS[0] == idOut]
                  if chipSel:
                      [chipSel] = chipSel
            else: chipSel = []
            
            if chip_in_enable_inv:
                  chipEnInv = chip_in_enable_inv  
                  chipEnInv = [list(chipEI[1:]) for chipEI in chipEnInv if chipEI[0] == idOut]
                  if chipEnInv:
                      [chipEnInv] = chipEnInv
            else: chipEnInv = []
            
            if chip_in_enable:
                  chipEn = chip_in_enable  
                  chipEn = [list(chipE[1:]) for chipE in chipEn if chipE[0] == idOut]
                  if chipEn:
                      [chipEn] = chipEn
            else: chipEn = []
            
            if chip_in_clock:
                  chipInClock = chip_in_clock 
                  chipInClock = [list(chipICLK[1:]) for chipICLK in chipInClock if chipICLK[0] == idOut]
                  if chipInClock:
                      [chipInClock] =chipInClock
                  chipInClock = [(c1,l1) for (c1,l1,nfunc) in chipInClock if nfunc == nf]
            else: chipInClock = []

            if chip_in_inv_reset:
                  chipInInvReset = chip_in_inv_reset 
                  chipInInvReset = [list(chipInInvR[1:]) for chipInInvR in chipInInvReset if chipInInvR[0] == idOut]
                  if chipInInvReset:
                      [chipInInvReset] = chipInInvReset
                  chipInInvReset = [(c1,l1) for (c1,l1,nfunc) in chipInInvReset if nfunc == nf]
            else: chipInInvReset = []

            if chip_in_inv_set:
                  chipInInvSet = chip_in_inv_set 
                  chipInInvSet = [list(chipInInvS[1:]) for chipInInvS in chipInInvSet if chipInInvS[0] == idOut]
                  if chipInInvSet:
                      [chipInInvSet] = chipInInvSet                  
                  chipInInvSet = [(c1,l1) for (c1,l1,nfunc) in chipInInvSet if nfunc == nf]
            else: chipInInvSet = []

            if chip_in_inv_clock:
                  chipInInvClk = chip_in_inv_clock 
                  chipInInvClk = [list(chipInIClk[1:]) for chipInIClk in chipInInvClk if chipInIClk[0] == idOut]
                  if chipInInvClk:
                      [chipInInvClk] = chipInInvClk
                  chipInInvClk = [(c1,l1) for (c1,l1,nfunc) in chipInInvClk if nfunc == nf]
            else: chipInInvClk = []
            
            if chip_in_j:
                  chipInJ = chip_in_j 
                  chipInJ = [list(chipIJ[1:]) for chipIJ in chipInJ if chipIJ[0] == idOut]
                  if chipInJ:
                      [chipInJ] = chipInJ
                  chipInJ = [(c1,l1) for (c1,l1,nfunc) in chipInJ if nfunc == nf]
            else: chipInJ = []
            
            if chip_in_k:
                  chipInK = chip_in_k 
                  chipInK = [list(chipIK[1:]) for chipIK in chipInK if chipIK[0] == idOut]
                  if chipInK:
                      [chipInK] = chipInK
                  chipInK = [(c1,l1) for (c1,l1,nfunc) in chipInK if nfunc == nf]
            else: chipInK = []
            
            if chip_in_inv_k:
                  chipInInvK = chip_in_inv_k 
                  chipInInvK = [list(chipIIK[1:]) for chipIIK in chipInInvK if chipIIK[0] == idOut]
                  if chipInInvK:
                      [chipInInvK] = chipInInvK
                  chipInInvK = [(c1,l1) for (c1,l1,nfunc) in chipInInvK if nfunc == nf]
            else: chipInInvK = []
        
            if chip_in_ce:
                  chipInCE = chip_in_ce 
                  chipInCE = [list(chipICE[1:]) for chipICE in chipInCE if chipICE[0] == idOut]
                  if chipInCE:
                      [chipInCE] = chipInCE
                  chipInCE = [(c1,l1) for (c1,l1,nfunc) in chipInCE if nfunc == nf]
            else: chipInCE = []
            
            if chip_in_inv_L:
                  chipInInvL = chip_in_inv_L 
                  chipInInvL = [list(chipIIL[1:]) for chipIIL in chipInInvL if chipIIL[0] == idOut]
                  if chipInInvL:
                      [chipInInvL] = chipInInvL
                  chipInInvL = [(c1,l1) for (c1,l1,nfunc) in chipInInvL if nfunc == nf]
            else: chipInInvL = []
            
            if chip_in_inv_U:
                  chipInInvU = chip_in_inv_U 
                  chipInInvU = [list(chipIIU[1:]) for chipIIU in chipInInvU if chipIIU[0] == idOut]
                  if chipInInvU:
                      [chipInInvU] = chipInInvU
                  chipInInvU = [(c1,l1) for (c1,l1,nfunc) in chipInInvU if nfunc == nf]
            else: chipInInvU = []
            
            if chip_out_TC:
                  chipOutTC = chip_out_TC 
                  chipOutTC = [list(chipOTC[1:]) for chipOTC in chipOutTC if chipOTC[0] == idOut]
                  if chipOutTC:
                      [chipOutTC] = chipOutTC
                  chipOutTC = [(c1,l1) for (c1,l1,nfunc) in chipOutTC if nfunc == nf]
            else: chipOutTC = []

            if chip_out_inv:
                  chipOutInv = chip_out_inv 
                  chipOutInv = [list(chipOI[1:]) for chipOI in chipOutInv if chipOI[0] == idOut]
                  if chipOutInv:
                      [chipOutInv] = chipOutInv
            else: chipOutInv = []
            
            inLst += chipSel  + chipEnInv + chipEn + chipInClock + chipInInvReset + chipInInvSet + \
                     chipInInvClk + chipInK + chipInInvK + chipInCE + chipInInvL + chipInInvU 
            outLst += chipOutInv + chipOutTC
            for no,out in enumerate(outLst):
                #if out not in chip_out_checked:
                    if self.is_linked_to(ioZone, out): 
                        findOut = True
                        #self.script += "( "
                        #chip_out_checked += [out]
                        inFuncConst = []
                        for n,inFunc in enumerate(inLst):
                            findIn = False
                            if  self.is_linked_to(self.pwrP, inFunc) or self.is_linked_to(self.pwrM, inFunc):
                                constKey = 'val'
                                pos, neg = "1", "0"
                                for c in chipSel:
                                    if c == inFunc:
                                        constKey = "sel"
                                for c in chipEnInv:
                                    if c == inFunc:
                                        constKey = "einv"
                                        pos, neg = "0", "1"
                                for c in chipEn:
                                    if c == inFunc:
                                        constKey = "enb"
                                for c in chipInInvReset:
                                    if c == inFunc:
                                        constKey = 'irst'
                                for c in chipInInvSet:
                                    if c == inFunc:
                                        constKey = 'iset'
                                        
                                for c in chipInInvClk:
                                    if c == inFunc:
                                        constKey = 'iclk'
                                for c in chipInJ:
                                    if c == inFunc:
                                        constKey = "J"
                                for c in chipInK:
                                    if c == inFunc:
                                        constKey = "K"
                                for c in chipInInvK:
                                    if c == inFunc:
                                        constKey = "iK"

                                for c in chipInCE:
                                    if c == inFunc:
                                        constKey = "CE"
                                for c in chipInInvL:
                                    if c == inFunc:
                                        constKey = "iL"
                                for c in chipInInvU:
                                    if c == inFunc:
                                        constKey = "iU"


                                if self.is_linked_to(self.pwrP, inFunc):
                                        inFuncConst += [{constKey:pos, "num":n, 'numO':no}]
                                else:   inFuncConst += [{constKey:neg, "num":n, 'numO':no}]
                                findIn = True
                                print("connecté à pwr")
                            if not findIn:
                                for n_io,io_inZone in enumerate(self.io_in):
                                    id, [zone] = io_inZone
                                    if self.is_linked_to(zone, inFunc):
                                        constKey = 'val'
                                        for c in chipSel:
                                            if c == inFunc:
                                                constKey = "sel"
                                        for c in chipEnInv:
                                            if c == inFunc:
                                                constKey = "einv"
                                        for c in chipEn:
                                            if c == inFunc:
                                                constKey = "enb"
                                        for c in chipInInvReset:
                                            if c == inFunc:
                                                constKey = 'irst'
                                        for c in chipInInvSet:
                                            if c == inFunc:
                                                constKey = 'iset'
                                        for c in chipInClock:
                                            if c == inFunc:
                                                constKey = 'clk'
                                                
                                        for c in chipInInvClk:
                                            if c == inFunc:
                                                constKey = 'iclk'
                                        for c in chipInJ:
                                            if c == inFunc:
                                                constKey = "J"
                                        for c in chipInK:
                                            if c == inFunc:
                                                constKey = "K"
                                        for c in chipInInvK:
                                            if c == inFunc:
                                                constKey = "iK"
                                                
                                        for c in chipInCE:
                                            if c == inFunc:
                                                constKey = "CE"
                                        for c in chipInInvL:
                                            if c == inFunc:
                                                constKey = "iL"
                                        for c in chipInInvU:
                                            if c == inFunc:
                                                constKey = "iU"
                                                
                                        #inFuncConst += [{constKey:self.mcu_pin[f"I{id[4:]}"], "num":n, "numO":no}] # [self.mcu_pin[f"I{id[4:]}"]] # ici ajouter n 
                                        inFuncConst += [{constKey:f"I{n_io+1}", "num":n_io, "numO":no}] # [self.mcu_pin[f"I{id[4:]}"]] # ici ajouter n 
                                        findIn = True
                                        print("connecté à une ENTRÉE EXTERNE")
                                        break
                            if not findIn:
                                for n_io, io_chipInZone in enumerate(self.chip_in_wire):
                                    id, zone = io_chipInZone
                                    if self.is_linked_to(zone, inFunc):
                                        constKey = 'val'
                                        for c in chipSel:
                                            if c == inFunc:
                                                constKey = "sel"
                                        for c in chipEnInv:
                                            if c == inFunc:
                                                constKey = "einv"
                                        for c in chipEn:
                                            if c == inFunc:
                                                constKey = "enb"
                                        for c in chipInInvReset:
                                            if c == inFunc:
                                                constKey = 'irst'
                                        for c in chipInInvSet:
                                            if c == inFunc:
                                                constKey = 'iset'
                                        for c in chipInClock:
                                            if c == inFunc:
                                                constKey = 'clk'
                                                
                                        for c in chipInInvClk:
                                            if c == inFunc:
                                                constKey = 'iclk'
                                        for c in chipInJ:
                                            if c == inFunc:
                                                constKey = "J"
                                        for c in chipInK:
                                            if c == inFunc:
                                                constKey = "K"
                                        for c in chipInInvK:
                                            if c == inFunc:
                                                constKey = "iK"
                                                
                                        for c in chipInCE:
                                            if c == inFunc:
                                                constKey = "CE"
                                        for c in chipInInvL:
                                            if c == inFunc:
                                                constKey = "iL"
                                        for c in chipInInvU:
                                            if c == inFunc:
                                                constKey = "iU"
                                                
                                        #inFuncConst += [{constKey:self.mcu_pin[f"I{id[4:]}"], "num":n, "numO":no}]
                                        inFuncConst += [{constKey:f"I{n_io+1}", "num":n_io, "numO":no}]
                                        findIn = True
                                        print("connecté à une ENTRÉE EXTERNE par cable") # ici ajouter n {'val':self.mcu_pin[f"I{id[4:]}"], "num":n}
                                        break
                                    
                            if not findIn:      ## recherche d'une sortie de chip connectée à l'entrée actuelle de la chip
                                findNext =False
                                for nextOut in self.chip_out_wire: 
                                    #id, (c1, l1) = nextOut
                                    #outZone = deepcopy(self.board.sketcher.matrix[f"{c1},{l1}"]["link"])
                                    
                                    if self.is_linked_to(nextOut, inFunc):
                                        #for next in nextOut:
                                            for cow in self.chip_out:
                                                id, pts = cow[0], cow[1:]
                                                for pt in pts:
                                                    if self.is_linked_to(nextOut, pt):
                                                        outZone =(id,[nextOut])
                                                        print("On passe à une autre sortie...")
                                                        ######## RAPPEL RECURSIF SUR OUTZONE ######################
                                                        if outZone not in self.chip_out_checked:
                                                            self.chip_out_checked += [outZone]
                                                            isPinOut = False
                                                            for pinOut in self.io_out:
                                                                id, [pinZoneOut] = pinOut
                                                                if self.is_linked_to(pinZoneOut, pt):
                                                                    #outPrev = self.mcu_pin[f"O{id[4:]}"]
                                                                    outPrev = f"O{no+1}"
                                                                    constKey = 'val'
                                                                    for c in chipSel:
                                                                        if c == inFunc:
                                                                            constKey = "sel"
                                                                    for c in chipEnInv:
                                                                        if c == inFunc:
                                                                            constKey = "einv"
                                                                    for c in chipEn:
                                                                        if c == inFunc:
                                                                            constKey = "enb"
                                                                            
                                                                    for c in chipOutTC:
                                                                        if c == inFunc:
                                                                            constKey = "TC"
                                                                
                                                                    for c in chipOutInv:
                                                                        if c == pt:
                                                                            outPrev = "!" + outPrev
                                                                    isPinOut = True
                                                                    inFuncConst += [{constKey:outPrev, "num":n, 'numO':no}] # [self.mcu_pin[f"O{id[4:]}"]] 
                                                                    findNext = True
                                                            if not isPinOut:
                                                                findNext, s = self.checkCloseCircuit(outZone,params)
                                                                constKey = 'val'
                                                                for c in chipSel:
                                                                    if c == inFunc:
                                                                        constKey = "sel"
                                                                for c in chipEnInv:
                                                                    if c == inFunc:
                                                                        constKey = "einv"
                                                                for c in chipEn:
                                                                    if c == inFunc:
                                                                        constKey = "enb"

                                                                    for c in chipOutTC:
                                                                        if c == inFunc:
                                                                            constKey = "TC"

                                                                for c in chipOutInv:
                                                                    if c == pt:
                                                                        s = "!" + s 
                                                                        
                                                                inFuncConst += [{constKey:s, "num":n, 'numO':no}]
                                                                self.chip_out_script += [(s,outZone)]
                                                        else: 
                                                            # il faut voir si une sortie io n'existe pas sinon var temp
                                                            isPinOut = False
                                                            for pinOut in self.io_out:
                                                                id, [pinZoneOut] = pinOut
                                                                if self.is_linked_to(pinZoneOut, pt):
                                                                    isPinOut = True
                                                                    #outPrev = self.mcu_pin[f"O{id[4:]}"]
                                                                    outPrev = f"O{no+1}"
                                                                    constKey = 'val'
                                                                    for c in chipSel:
                                                                        if c == inFunc:
                                                                            constKey = "sel"
                                                                    for c in chipEnInv:
                                                                        if c == inFunc:
                                                                            constKey = "einv"
                                                                    for c in chipEn:
                                                                        if c == inFunc:
                                                                            constKey = "enb"

                                                                    for c in chipOutTC:
                                                                        if c == inFunc:
                                                                            constKey = "TC"

                                                                    for c in chipOutInv:
                                                                        if c == pt:
                                                                            outPrev = "!" + outPrev
                                                                            
                                                                    inFuncConst += [{constKey:outPrev, "num":n, 'numO':no}]
                                                            if not isPinOut:
                                                                for coc in self.chip_out_script:
                                                                    if coc[1] == outZone:
                                                                        exp = coc[0]
                                                                        constKey = 'val'
                                                                        for c in chipSel:
                                                                            if c == inFunc:
                                                                                constKey = "sel"
                                                                        for c in chipEnInv:
                                                                            if c == inFunc:
                                                                                constKey = "einv"
                                                                        for c in chipEn:
                                                                            if c == inFunc:
                                                                                constKey = "enb"

                                                                        for c in chipOutTC:
                                                                            if c == inFunc:
                                                                                constKey = "TC"

                                                                        for c in chipOutInv:
                                                                            if c == pt:
                                                                                exp = "!" + exp
                                                                                
                                                                        inFuncConst += [{constKey:exp, "num":n, 'numO':no}] 
                                                                        break
                                                            findNext = True
                                                        break
                            if not findIn and not findNext:
                                self.in_outOC += [(id,inFunc)]
                                circuitClose = False
                        if findIn or findNext:
                            #self.script += ") "
                            script = self.decodeFunc(inFuncConst, fName) 
        if not findOut:
            self.in_outOC += [ioOut]   
            circuitClose = False 
        # if  not findIn and not findNext:
        #     circuitClose = False

        return circuitClose, script        
                                    
                                
        

    def checkCircuit(self):
        print("Lancer la vérification")
        self.func = []
        self.wire = []
        (xBatNeg, yBatNeg) = self.current_dict_circuit['_battery_neg_wire']["end"]
        (xBatPos, yBatPos) = self.current_dict_circuit['_battery_pos_wire']["end"]
        (_, _),(colBatNeg, lineBatNeg) = self.sketcher.find_nearest_grid_point(xBatNeg, yBatNeg)
        (_, _),(colBatPos, lineBatPos) = self.sketcher.find_nearest_grid_point(xBatPos, yBatPos)
        #self.pwrs = [(61, 1, "-"), (61, 2, "+")]  # [(col, line, "+" ou "-"), ...]
        self.pwrs = [(colBatNeg, lineBatNeg, "-"), (colBatPos, lineBatPos, "+")]  # [(col, line, "+" ou "-"), ...]
        self.pwrChip = {"+": [], "-": [], "pwrConnected":[], "pwrNotConnected": [], "pwrMissConnected": []}  # , "pwrNOTUSED": [], "pwrCC": []
        self.io_in, self.io_out = [], []
        self.chip_in, self.chip_out = [], [] 
        self.chip_ioCC, self.chip_ioOK = [], []
        self.pwrM, self.pwrP, self.wireNotUsed, self.pwrCC = [], [], [], []
        self.io_inCC, self.io_outCC = [], []
        self.chip_out_wire, self.chip_outCC = [], []
        self.chip_in_wire = []
        self.in_outOC = []
        self.chip_out_checked = []
        self.chip_out_script = []
        
        chip_select = []
        chip_out_inv = []
        chip_in_enable = []
        chip_in_enable_inv = []
        chip_in_clock = []
        chip_in_inv_reset = []
        chip_in_inv_set = []
        chip_in_inv_clock = []
        chip_in_j = []
        chip_in_k = []
        chip_in_inv_k = []
        
        chip_in_ce = []
        chip_in_inv_L = []
        chip_in_inv_U = []
        chip_out_TC = []        

        self.varTempNum = 1
        self.varScript = []

        self.show_correspondence_table(False)
        for id, component in self.current_dict_circuit.items():
            if id[:6] == "_chip_":
                (x, y) = component["pinUL_XY"]
                numPinBR = component["pinCount"] // 2
                (real_x, real_y), (col, line) = self.sketcher.find_nearest_grid_chip(x, y)
                #ioIn, ioOut = [], []
                for io in component["io"]:  #  [([(ce1, le1), ...], "&", [(cs1, ls1), (cs2, ls2), ...]), ...]
                    #io = component["io"]
                    # ioIN, ioOut = [], []
                    ioIn = [
                        # (col + (numPin % numPinBR) - 1 + (numPin // numPinBR), line + 1 - (numPin // numPinBR))
                        # for numPin in io[0]
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in io[0]
                    ]
                    
                    ioOut = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in io[1]
                    ]
                    self.func += [(id, ioIn, component["symbScript"], ioOut)]
                    if ioIn:
                        self.chip_in += [(id, *ioIn)]
                    if ioOut:
                        self.chip_out += [(id, *ioOut)]
                # print(f"ioIN  = {ioIn}")
                # print(f"ioOUT = {ioOut}")
                # print(f"self.func= {self.func}")
                # print(f"ce1-ce2, self.func, cs1:({io[0][0]}-{io[0][1]} , {chip["symbScript"]} , {io[1][0]})")
                for pwr in component["pwr"]:
                    numPin, polarity = pwr[0], pwr[1]
                    col_pin = col + numPin - 1 if numPin <= numPinBR else col + (component["pinCount"] - numPin)
                    line_pin = line if numPin > numPinBR else line+1
                    self.pwrChip[polarity] += [
                        (id, col_pin, line_pin)
                    ]
                    # print(f"pwrChip= {self.pwrChip}")
                ############### gestion des MUX DEMUX #################
                    #### les sélecteurs ###
                ioSel = component.get("io_select", [])
                if ioSel:    
                    ioS = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in ioSel[0]
                    ]
                    if ioS:
                        chip_select += [(id, *ioS)]
                        self.chip_in += [(id, *ioS)]
                    
                    #### les sorties inversées ###
                ioOutInv = component.get("io_out_inv", [])
                if ioOutInv:
                    ioOI = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in ioOutInv[0]
                    ]
                    if ioOI:
                        chip_out_inv += [(id, *ioOI)]
                        self.chip_out += [(id, *ioOI)]
                
                    #### les entrées enable ###
                ioInEnable = component.get("io_enable", [])
                if ioInEnable:
                    ioIEn = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in ioInEnable[0]
                    ]
                    if ioIEn:
                        chip_in_enable += [(id, *ioIEn)]
                        self.chip_in += [(id, *ioIEn)]
                    
                    #### les entrées enable inverse ###
                ioInEnableInv = component.get("io_enable_inv", [])
                if ioInEnableInv:
                    ioIEnInv = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR))
                        for numPin in ioInEnableInv[0]
                    ]
                    if ioIEnInv:
                        chip_in_enable_inv += [(id, *ioIEnInv)]
                        self.chip_in += [(id, *ioIEnInv)]
                        
                    #### l' entrée clock  ###
                ioInClock = component.get("clock_pin", [])
                if ioInClock:
                    ioInCLK = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInClock,[])
                    ]
                    if ioInCLK:
                        chip_in_clock += [(id, *ioInCLK)]
                        self.chip_in += [(id, *ioInCLK)]
                        
                    #### l' entrée clock Inv  ###
                ioInClockInv = component.get("inv_clock_pin", [])
                if ioInClockInv:
                    ioInCLKInv = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInClockInv,[])
                    ]
                    if ioInCLKInv:
                        chip_in_inv_clock += [(id, *ioInCLKInv)]
                        self.chip_in += [(id, *ioInCLKInv)]
                        
                    #### l' entrée Reset Inv  ###
                ioInResetInv = component.get("inv_reset_pin", [])
                if ioInResetInv:
                    ioInRinv = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInResetInv, [])
                    ]
                    if ioInRinv:
                        chip_in_inv_reset += [(id, *ioInRinv)]
                        self.chip_in += [(id, *ioInRinv)]
                                
                    #### l' entrée Set Inv  ###
                ioInSetInv = component.get("inv_set_pin", [])
                if ioInSetInv:
                    ioInSinv = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInSetInv, [])
                    ]
                    if ioInSinv:
                        chip_in_inv_set += [(id, *ioInSinv)]
                        self.chip_in += [(id, *ioInSinv)]
                    
                    #### l' entrée J ###
                ioInJ = component.get("j_input_pin", [])
                if ioInJ:
                    ioIJ = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInJ, [])
                    ]
                    if ioIJ:
                        chip_in_j += [(id, *ioIJ)]
                        self.chip_in += [(id, *ioIJ)]
                    
                    #### l' entrée K Inv  ###
                ioInKInv = component.get("inv_k_input_pin", [])
                if ioInKInv:
                    ioIKInv = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInKInv, [])
                    ]
                    if ioIKInv:
                        chip_in_inv_k  += [(id, *ioIKInv)]
                        self.chip_in += [(id, *ioIKInv)]
                    
                    #### l' entrée K   ###
                ioInK = component.get("k_input_pin", [])
                if ioInK:
                    ioIK = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInK, [])
                    ]
                    if ioIK:
                        chip_in_k  += [(id, *ioIK)]
                        self.chip_in += [(id, *ioIK)]
                
                    #### l' entrée CE   ###
                ioInCE = component.get("count_enable_pin", [])
                if ioInCE:
                    ioICE = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInCE, [])
                    ]
                    if ioICE:
                        chip_in_ce  += [(id, *ioICE)]
                        self.chip_in += [(id, *ioICE)]
                    
                    #### l' entrée L   ###
                ioInInvL = component.get("inv_load_enable_pin", [])
                if ioInInvL:
                    ioIIL = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInInvL, [])
                    ]
                    if ioIIL:
                        chip_in_inv_L  += [(id, *ioIIL)]
                        self.chip_in += [(id, *ioIIL)]
                    
                    #### l' entrée U   ###
                ioInInvU = component.get("inv_up_down_input_pin", [])
                if ioInInvU:
                    ioIIU = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioInInvU, [])
                    ]
                    if ioIIU:
                        chip_in_inv_U  += [(id, *ioIIU)]
                        self.chip_in += [(id, *ioIIU)]
                    
                    #### l' entrée TC   ###
                ioOutTC = component.get("terminal_count_pin", [])
                if ioOutTC:
                    ioOTC = [
                        (col + numPin  - 1 if numPin <= numPinBR else col + (numPinBR - (numPin % numPinBR) ), line + 1 - (numPin // numPinBR),n)
                        for (n,numPin) in sum(ioOutTC, [])
                    ]
                    if ioOTC:
                        chip_out_TC  += [(id, *ioOTC)]
                        self.chip_out += [(id, *ioOTC)]
                    
            elif id[:6] == "_wire_":  # [(col1, line1,col2,line2), ...]
                self.wire += [(id, *component["coord"][0])]
            elif id[:4] == "_io_":  # [(col1, line1,col2,line2), ...]
                (col, line) = component["coord"][0][0], component["coord"][0][1]
                ioZone = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
                if component["type"] == INPUT or component["type"] == CLOCK:
                    self.io_in += [(id, [ioZone])]
                else:
                    self.io_out += [(id, [ioZone])]
        print(f"func= {self.func}\n")
        print(f"pwrChip= {self.pwrChip}\n")
        print(f"wire = {self.wire}")
        print(f"pwr = {self.pwrs}")
        print(f"io_in = {self.io_in}")
        print(f"io_out = {self.io_out}")
        print(f"chip_in = {self.chip_in}")
        print(f"chip_out = {self.chip_out}")
        for pwr in self.pwrs:
            (col, line, p) = pwr
            if p == "-":
                   self.pwrM = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
            else:  self.pwrP = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
        for w in self.wire:
            id,c1,l1,c2,l2 = w
            if self.is_linked_to(self.pwrM, (c1, l1)):
                    self.pwrM += deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            elif  self.is_linked_to(self.pwrP, (c1, l1)):  
                    self.pwrP += deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            elif w not in self.wireNotUsed: 
                self.wireNotUsed += [w] #deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            if self.is_linked_to(self.pwrM, (c2, l2)):
                    self.pwrM += deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            elif  self.is_linked_to(self.pwrP, (c2, l2)):  
                    self.pwrP += deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            elif w not in self.wireNotUsed:  
                 self.wireNotUsed += [w] #deepcopy(self.board.sketcher.matrix[f"{c2},{l2}"]["link"])
            again = True
            while again and len(self.wireNotUsed)>0:
                again = False
                for wused in self.wireNotUsed[:]:
                    id,cu1,lu1,cu2,lu2 = wused
                    if self.is_linked_to(self.pwrM, (cu1, lu1)):
                            self.pwrM += deepcopy(self.board.sketcher.matrix[f"{cu2},{lu2}"]["link"])
                            self.wireNotUsed.remove(wused)
                            again = True
                    elif  self.is_linked_to(self.pwrP, (cu1, lu1)):  
                            self.pwrP += deepcopy(self.board.sketcher.matrix[f"{cu2},{lu2}"]["link"])
                            self.wireNotUsed.remove(wused)
                            again = True
                    
                    if self.is_linked_to(self.pwrM, (cu2, lu2)):
                            self.pwrM += deepcopy(self.board.sketcher.matrix[f"{cu1},{lu1}"]["link"])
                            if not again:
                                self.wireNotUsed.remove(wused)
                            again = True
                    elif  self.is_linked_to(self.pwrP, (cu2, lu2)):  
                            self.pwrP += deepcopy(self.board.sketcher.matrix[f"{cu1},{lu1}"]["link"])
                            if not again:
                                 self.wireNotUsed.remove(wused)
                            again = True
                    if again:
                        if (self.is_linked_to(self.pwrP, (cu1, lu1)) and self.is_linked_to(self.pwrM, (cu1, lu1))) or \
                                (self.is_linked_to(self.pwrP, (cu2, lu2)) and self.is_linked_to(self.pwrM, (cu2, lu2))):
                            self.pwrCC += [wused]
                            #print(f"CC dans le cable {wused}")                    
            if (self.is_linked_to(self.pwrP, (c1, l1)) and self.is_linked_to(self.pwrM, (c1, l1))) or \
                    (self.is_linked_to(self.pwrP, (c2, l2)) and self.is_linked_to(self.pwrM, (c2, l2))):
                    self.pwrCC += [w]
                    #print(f"CC dans le cable {w}")
        #pwrM.clear()
        #pwrP.clear()
    ###############   Verification des chip sur pwr + #####################
        for chip in self.pwrChip["+"]:
            id, col_pin, line_pin = chip
            if self.is_linked_to(self.pwrP, (col_pin, line_pin)):
                  if id not in self.pwrChip["pwrConnected"]:
                    self.pwrChip["pwrConnected"].append((id,"+"))
            elif self.is_linked_to(self.pwrM, (col_pin, line_pin)):
                  if id not in self.pwrChip["pwrMissConnected"]:
                    self.pwrChip["pwrMissConnected"].append((id,"+"))
            elif id not in self.pwrChip["pwrNotConnected"]:
                    self.pwrChip["pwrNotConnected"].append((id,"+"))
    ###############   Verification des chip sur pwr - #####################
        for chip in self.pwrChip["-"]:
            id, col_pin, line_pin = chip
            if self.is_linked_to(self.pwrM, (col_pin, line_pin)):
                  if id not in self.pwrChip["pwrConnected"]:
                    self.pwrChip["pwrConnected"].append((id,"-"))
            elif self.is_linked_to(self.pwrP, (col_pin, line_pin)):
                  if id not in self.pwrChip["pwrMissConnected"]:
                    self.pwrChip["pwrMissConnected"].append((id,"-"))
            elif id not in self.pwrChip["pwrNotConnected"]:
                    self.pwrChip["pwrNotConnected"].append((id,"-"))
    ###############   Verification des chip_out sur pwr #####################
        for chipAllio in self.chip_out:
            id = chipAllio[0]
            for chipio in chipAllio[1:]:
                c1,l1, *n = chipio
                if self.is_linked_to(self.pwrM, (c1, l1)):
                    self.chip_ioCC += [(id, chipio)]
                elif self.is_linked_to(self.pwrP, (c1, l1)):
                    self.chip_ioCC += [(id,chipio)]
                else:
                    self.chip_ioOK += [(id,chipio)]
                    ###############   Verification des chip_out sur  io_in #####################
                for ioin in self.io_in:
                    id, [ioInZone] = ioin
                    if self.is_linked_to(ioInZone, (c1, l1)):
                        self.io_outCC += [ioin[0]]
                    
     ###############   Verification des io_in sur pwr #####################
        for ioin in self.io_in:
            #c1, l1 = ioin[1][0], ioin[1][1]
            id, ioInZone = ioin
            [(c1,l1,c2,l2)] = ioInZone[0]
            inChipInWire = False
            if self.is_linked_to(self.pwrM, (c1, l1)):
                inChipInWire = True
                if ioin[0] not in self.io_outCC:
                    self.io_outCC += [ioin[0]]
            elif self.is_linked_to(self.pwrP, (c1, l1)): 
                inChipInWire = True
                if ioin[0] not in self.io_outCC:
                    self.io_outCC += [ioin[0]]
            if not inChipInWire:
                ciw = deepcopy(self.board.sketcher.matrix[f"{c1},{l1}"]["link"])
                again = True
                while again and len(self.wireNotUsed)>0:
                    again = False
                    for wused in self.wireNotUsed[:]:
                        id,cu1,lu1,cu2,lu2 = wused
                        if self.is_linked_to(ciw, (cu1, lu1)):
                                ciw += deepcopy(self.board.sketcher.matrix[f"{cu2},{lu2}"]["link"])
                                self.wireNotUsed.remove(wused)
                                again = True
                        elif  self.is_linked_to(ciw, (cu2, lu2)):  
                                ciw += deepcopy(self.board.sketcher.matrix[f"{cu1},{lu1}"]["link"])
                                self.wireNotUsed.remove(wused)
                                again = True
                        elt = (ioin[0], ciw)
                        if not elt in self.chip_in_wire:
                            self.chip_in_wire += [elt]
                    
        ###############   Verification des self.chip_out sur chip_out #####################
        for chipAllio in self.chip_out:
            id = chipAllio[0]
            inChipOutWire = False
            for chipio in chipAllio[1:]:
                (c1,l1, *n) = chipio
                for cow in self.chip_out_wire:
                    if self.is_linked_to(cow, (c1, l1)):
                        inChipOutWire = True
                        if chipio not in self.chip_outCC:
                            self.chip_outCC += [(id,chipio)] 
                if not inChipOutWire:
                    cow = deepcopy(self.board.sketcher.matrix[f"{c1},{l1}"]["link"])
                    again = True
                    while again and len(self.wireNotUsed)>0:
                        again = False
                        for wused in self.wireNotUsed[:]:
                            id,cu1,lu1,cu2,lu2 = wused
                            if self.is_linked_to(cow, (cu1, lu1)):
                                    cow += deepcopy(self.board.sketcher.matrix[f"{cu2},{lu2}"]["link"])
                                    self.wireNotUsed.remove(wused)
                                    again = True
                                    if not cow in self.chip_out_wire:
                                        self.chip_out_wire += [cow]
                            elif  self.is_linked_to(cow, (cu2, lu2)):  
                                    cow += deepcopy(self.board.sketcher.matrix[f"{cu1},{lu1}"]["link"])
                                    self.wireNotUsed.remove(wused)
                                    again = True
                                    if not cow in self.chip_out_wire:
                                        self.chip_out_wire += [cow]
                
        ################# Redefinir les zones des io_out avec les cables non utilisés ##############
        for n,ioOut in enumerate(self.io_out):
            id, [ioOutZone] = ioOut
            c1,l1,c2,l2 = ioOutZone[0]
            ioOutZoneWire = []
            inIoOutZoneWire = False
            for cow in self.wireNotUsed:   # self.chip_out_wire
                cow = [(cow[1:])]
                if self.is_linked_to(cow, (c1, l1)):
                    inIoOutZoneWire = True
                    ioOutZoneWire += [cow]
            if inIoOutZoneWire:
                self.io_out[n] =  (id,ioOutZoneWire)
                
        # ################ Redefinir les zones des chip_out avec les cables non utilisés ##############
        # for chipO in self.chip_out:
        #     id = chipO[0]
        #     for co in chipO[1:]:
        #         for        

        if not self.pwrCC and not self.pwrChip["pwrMissConnected"] and not self.chip_ioCC \
                        and not self.io_outCC and not self.chip_outCC and not self.in_outOC:
            print("vérification du circuit fermé")
            self.script = ""
            params ={
                        "chip_select":chip_select, 
                        "chip_out_inv":chip_out_inv, 
                        "chip_in_enable":chip_in_enable, 
                        "chip_in_enable_inv": chip_in_enable_inv, 
                        "chip_in_clock" : chip_in_clock,
                        "chip_in_inv_reset" : chip_in_inv_reset,
                        "chip_in_inv_set" : chip_in_inv_set,
                        "chip_in_inv_clock" : chip_in_inv_clock,                
                        "chip_in_j" : chip_in_j,
                        "chip_in_k" : chip_in_k,
                        "chip_in_inv_k" : chip_in_inv_k,
                        "count_enable_pin" : chip_in_ce, 
                        "inv_load_enable_pin" : chip_in_inv_L ,
                        "inv_up_down_input_pin" : chip_in_inv_U ,
                        "terminal_count_pin" : chip_out_TC ,                  
                    }
            def io_position(io):
                id,[[p]] = io
                return p[0]
            
                    # "chip_in_address_pins":chip_in_address_pins}
            for no,ioOut in enumerate(sorted(self.io_out, key=lambda io: io_position(io))):
               #self.script += self.mcu_pin[f"O{ioOut[0][4:]}"] + " = "  # f"O{no+1}"
               
               circuitClose, script = self.checkCloseCircuit(ioOut,params)
               if circuitClose :
                        print(f"le circuit est fermée sur la sortie {ioOut}")
                        for s in self.varScript:
                            self.script += s 
                        self.varScript = []
                        self.script += f"O{no+1}" + " = "
                        self.script += f"{script}; \n"
                        print(f"script temp : {self.script}")
               else:    print(f"le circuit est ouvert sur la sortie {ioOut}")

                                    
        print(f"pwrChipConnected : {self.pwrChip['pwrConnected']}")
        print(f"pwrChipNotConnected : {self.pwrChip['pwrNotConnected']}")
        print(f"pwrChipMissConnected : {self.pwrChip['pwrMissConnected']}")
        print(f"wireNotUsed : {self.wireNotUsed}")
        print(f"pwrCC : {self.pwrCC}")
        print(f"chip_ioCC : {self.chip_ioCC}")
        print(f"chip_ioOK : {self.chip_ioOK}")
        print(f"io_outCC : {self.io_outCC}")
        print(f"chip_outCC : {self.chip_outCC}")
        print(f"in_outOC : {self.in_outOC}")
        print(f"chip_out_wire : {self.chip_out_wire}")
        print(f"chip_in_wire : {self.chip_in_wire}")
        print(f"chip_select : {chip_select}")
        print(f"chip_out_inv : {chip_out_inv}")
        print(f"chip_in_enable : {chip_in_enable}")
        print(f"chip_in_enable_inv : {chip_in_enable_inv}")
        print(f"map pin mcu : {self.mcu_pin}")
        print(f"script final : {self.script}")
        if self.script:
            messagebox.showinfo("Script du circuit", f"Circuit= {self.script}")
        else:
            messagebox.showinfo("Script du circuit", f"Le circuit présente au moins un défaut et ne peut être téléversé.")
