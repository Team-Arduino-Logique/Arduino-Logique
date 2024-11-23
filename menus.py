"""
This module defines the `Menus` class for creating a custom menu bar in a Tkinter application.
The menu bar includes options for file operations, controller selection, port configuration, and help documentation.
"""

from copy import deepcopy

from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
from typing import Callable
import serial.tools.list_ports  # type: ignore

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
)
from dataCDLT import INPUT, OUTPUT, USED

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
        model (list): The model data for the circuit.
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
        self.com_port: str | None = None
        """The selected COM port."""
        self.script = ""
        
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
            "Circuit": [
                "Vérifier",
                "Téléverser",
            ],
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
            "Vérifier": self.checkCircuit,
            "Téléverser": self.download_script,
            "Documentation": self.open_documentation,
            "À propos": self.about,
        }

        for menu_name, options in menus.items():
            self.create_menu(menu_name, options, menu_commands)

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
            dialog.destroy()

        confirm_button = tk.Button(dialog, text="Confirm", command=confirm_selection)
        confirm_button.pack(pady=10)

    def show_correspondence_table(self):
        """Displays the correspondence table between pin_io objects and microcontroller pins in a table format."""
        if self.selected_microcontroller is None:
            messagebox.showwarning("No Microcontroller Selected", "Please select a microcontroller first.")
            return

        pin_mappings = MICROCONTROLLER_PINS.get(self.selected_microcontroller)
        if not pin_mappings:
            messagebox.showerror("Error", f"No pin mappings found for {self.selected_microcontroller}.")
            return

        input_pins = pin_mappings["input_pins"]
        output_pins = pin_mappings["output_pins"]

        # Gather pin_io objects from current_dict_circuit
        pin_ios = [value for key, value in self.current_dict_circuit.items() if key.startswith("_io_")]

        # Separate pin_ios into inputs and outputs
        input_pin_ios = [pin for pin in pin_ios if pin["type"] == INPUT]
        output_pin_ios = [pin for pin in pin_ios if pin["type"] == OUTPUT]

        # Check if we have more pin_ios than available pins
        if len(input_pin_ios) > len(input_pins):
            messagebox.showerror(
                "Too Many Inputs",
                f"You have {len(input_pin_ios)} input pin_ios but only "
                f"{len(input_pins)} available input pins on the microcontroller.",
            )
            return
        if len(output_pin_ios) > len(output_pins):
            messagebox.showerror(
                "Too Many Outputs",
                f"You have {len(output_pin_ios)} output pin_ios but only "
                f"{len(output_pins)} available output pins on the microcontroller.",
            )
            return

        # Create a new window for the correspondence table
        table_window = tk.Toplevel(self.parent)
        table_window.title("Correspondence Table")
        table_window.geometry("400x300")

        # Create a Treeview widget for the table
        tree = ttk.Treeview(table_window, columns=("ID", "Type", "MCU Pin"), show="headings", height=10)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Define columns and headings
        tree.column("ID", anchor="center", width=120)
        tree.column("Type", anchor="center", width=80)
        tree.column("MCU Pin", anchor="center", width=120)
        tree.heading("ID", text="Pin IO ID")
        tree.heading("Type", text="Type")
        tree.heading("MCU Pin", text="MCU Pin")

        # Populate the table with input and output pin mappings
        for idx, pin_io in enumerate(input_pin_ios):
            mcu_pin = input_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "Input", mcu_pin))

        for idx, pin_io in enumerate(output_pin_ios):
            mcu_pin = output_pins[idx]
            pin_number = pin_io["id"].split("_")[-1]
            tree.insert("", "end", values=(pin_number, "Output", mcu_pin))

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
            option_btn = tk.Button(
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
        messagebox.showinfo("New File", "A new circuit has been created.")

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
                messagebox.showinfo("Open File", f"Circuit loaded from {file_path}")
            except Exception as e:
                print(f"Error loading file: {e}")
                messagebox.showerror("Open Error", f"An error occurred while opening the file:\n{e}")
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
                messagebox.showinfo("Save Successful", f"Circuit saved to {file_path}")
            except (TypeError, KeyError) as e:
                print(f"Error saving file: {e}")
                messagebox.showerror("Save Error", f"An error occurred while saving the file:\n{e}")
        else:
            print("Save file cancelled.")

    def configure_ports(self):
        """Handler for the 'Configure Ports' menu item."""
        print("Configure Ports")
        options = [comport.device for comport in serial.tools.list_ports.comports()]
        if len(options) == 0:
            message = "No COM ports available. Please connect a device and try again."
            print(message)
            messagebox.showwarning("No COM Ports", message)
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
        print("Open Documentation")
        messagebox.showinfo("Documentation", "Documentation not available yet.")

    def about(self):
        """Handler for the 'About' menu item."""
        print("About this software")
        messagebox.showinfo("About", "ArduinoLogique v1.0\nSimulateur de circuits logiques")
            
    def open_port(self):
        """Handler for the 'Open Port' menu item."""
        try:
            self.serial_conn = serial.Serial(
                port=self.com_port,
                baudrate=self.baud_rate,
                timeout=self.timeout
            )
            print(f"Port série {self.com_port} ouvert avec succès.")
        except serial.SerialException as e:
            print(f"Erreur lors de l'ouverture du port {self.com_port}: {e}")

    def send_data(self, data):
        """
        Send a string of data to the microcontroller through the serial port.
        """
        if self.serial_conn and self.serial_conn.is_open:
            try:
                # Convertir la chaîne en bytes et l'envoyer
                self.serial_conn.write(data.encode('utf-8'))
                print(f"Données envoyées: {data}")
            except serial.SerialException as e:
                print(f"Erreur lors de l'envoi des données: {e}")
        else:
            print("Le port série n'est pas ouvert. Impossible d'envoyer les données.")

    def close_port(self):
        """Upload the script to the microcontroller through the serial port."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print(f"Port série {self.com_port} fermé.")
        else:
            print("Le port série est déjà fermé.")
            
    def download_script(self):
        self.checkCircuit()
        self.open_port()
        self.send_data(self.script)
        self.close_port()
        
    def is_linked_to(self, dest, src):
        res = False
        c, l = src
        for zone in dest:
            c1, l1,c2, l2 = zone
            if (c >= c1 and c<= c2 and l >= l1 and l<= l2):
                res = True
                break
        return res
    
    def checkCloseCircuit(self, ioOut):
        id, (c1,l1,c2,l2)  = ioOut 
        ioZone = [(c1,l1,c2,l2)]
        findOut = False
        circuitClose = True
        #chip_out_checked = []
        
        for f in self.func:
            id, inLst, fName, outLst = f
            for out in outLst:
                #if out not in chip_out_checked:
                    if self.is_linked_to(ioZone, out): 
                        findOut = True
                        #chip_out_checked += [out]
                        for inFunc in inLst:
                            findIn = False
                            if  self.is_linked_to(self.pwrP, inFunc) or self.is_linked_to(self.pwrM, inFunc):
                                findIn = True
                                print("connecté à pwr")
                            if not findIn:
                                for io_inZone in self.io_in:
                                    id, zone = io_inZone
                                    if self.is_linked_to([zone], inFunc):
                                        findIn = True
                                        print("connecté à une ENTRÉE EXTERNE")
                            if not findIn:      ## recherche d'une sortie de chip connectée à l'entrée actuelle de la chip
                                findNext =False
                                for nextOut in self.chip_out_wire: 
                                    #id, (c1, l1) = nextOut
                                    #outZone = deepcopy(self.board.sketcher.matrix[f"{c1},{l1}"]["link"])
                                    
                                    if self.is_linked_to(nextOut, inFunc):
                                        for next in nextOut:
                                            for cow in self.chip_out:
                                                id, pt = cow
                                                if self.is_linked_to([next], pt):
                                                    outZone =(id,next)
                                                    print("On passe à une autre sortie...")
                                                    ######## RAPPEL RECURSIF SUR OUTZONE ######################
                                                    if outZone not in self.chip_out_checked:
                                                        self.chip_out_checked += [outZone]
                                                        findNext = self.checkCloseCircuit(outZone)
                                                    else: findNext = True
                                                    break
                            if not findIn and not findNext:
                                self.in_outOC += [(id,inFunc)]
                                circuitClose = False
        if not findOut:
            self.in_outOC += [ioOut]   
            circuitClose = False 
        if not findOut and not findIn and not findNext:
            circuitClose = False

        return circuitClose           
                                    
                                
        

    def checkCircuit(self):
        print("Lancer la vérification")
        self.func = []
        self.wire = []
        self.pwrs = [(61, 1, "-"), (61, 2, "+")]  # [(col, line, "+" ou "-"), ...]
        self.pwrChip = {"+": [], "-": [], "pwrConnected":[], "pwrNotConnected": [], "pwrMissConnected": []}  # , "pwrNOTUSED": [], "pwrCC": []
        self.io_in, self.io_out = [], []
        self.chip_in, self.chip_out = [], []
        self.chip_ioCC, self.chip_ioOK = [], []
        self.pwrM, self.pwrP, self.wireNotUsed, self.pwrCC = [], [], [], []
        self.io_inCC, self.io_outCC = [], []
        self.chip_out_wire, self.chip_outCC = [], []
        self.in_outOC = []
        self.chip_out_checked = []

        for id, component in self.current_dict_circuit.items():
            if id[:6] == "_chip_":
                (x, y) = component["pinUL_XY"]
                numPinBR = component["pinCount"] // 2
                (real_x, real_y), (col, line) = self.sketcher.find_nearest_grid_chip(x, y)
                ioIn, ioOut = [], []
                for io in component["io"]:  #  [([(ce1, le1), ...], "&", [(cs1, ls1), (cs2, ls2), ...]), ...]
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
                    self.chip_in += [(id, *ioIn)]
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
            elif id[:6] == "_wire_":  # [(col1, line1,col2,line2), ...]
                self.wire += [(id, *component["coord"][0])]
            elif id[:4] == "_io_":  # [(col1, line1,col2,line2), ...]
                (col, line) = component["coord"][0][0], component["coord"][0][1]
                ioZone = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
                if component["type"] == INPUT:
                    self.io_in += [(id, *ioZone)]
                else:
                    self.io_out += [(id, *ioZone)]
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
        for chipio in self.chip_out:
            id, (c1,l1)  = chipio
            if self.is_linked_to(self.pwrM, (c1, l1)):
                self.chip_ioCC += [chipio]
            elif self.is_linked_to(self.pwrP, (c1, l1)):
                self.chip_ioCC += [chipio]
            else:
                self.chip_ioOK += [chipio]
                ###############   Verification des chip_out sur  io_in #####################
            for ioin in self.io_in:
                if self.is_linked_to([ioin[1]], (c1, l1)):
                    self.io_outCC += [ioin[0]]
                    
     ###############   Verification des io_in sur pwr #####################
        for ioin in self.io_in:
            c1, l1 = ioin[1][0], ioin[1][1]
            if self.is_linked_to(self.pwrM, (c1, l1)):
                if ioin[0] not in self.io_outCC:
                    self.io_outCC += [ioin[0]]
            elif self.is_linked_to(self.pwrP, (c1, l1)): 
                if ioin[0] not in self.io_outCC:
                    self.io_outCC += [ioin[0]]
                    
        ###############   Verification des self.chip_out sur chip_out #####################
        for chipio in self.chip_out:
            id, (c1,l1)  = chipio  
            inChipOutWire = False
            for cow in self.chip_out_wire:
                if self.is_linked_to(cow, (c1, l1)):
                    inChipOutWire = True
                    if chipio not in self.chip_outCC:
                        self.chip_outCC += [(chipio)] 
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
                        elif  self.is_linked_to(cow, (cu2, lu2)):  
                                cow += deepcopy(self.board.sketcher.matrix[f"{cu1},{lu1}"]["link"])
                                self.wireNotUsed.remove(wused)
                                again = True
            self.chip_out_wire += [cow]
        if not self.pwrCC and not self.pwrChip["pwrMissConnected"] and not self.chip_ioCC \
                        and not self.io_outCC and not self.chip_outCC:
            print("vérification du circuit fermé")
            for ioOut in self.io_out:
               if  self.checkCloseCircuit(ioOut):
                        print(f"le circuit est fermée sur la sortie {ioOut}")
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
