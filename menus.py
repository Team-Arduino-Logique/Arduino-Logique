"""
This module defines the `Menus` class for creating a custom menu bar in a Tkinter application.
The menu bar includes options for file operations, controller selection, port configuration, and help documentation.
"""

from copy import deepcopy

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
from typing import Callable
import serial.tools.list_ports  # type: ignore

from breadboard import Breadboard
from component_sketch import ComponentSketcher


class Menus:
    """
    Menus class for creating a custom menu bar in a Tkinter application.
    Attributes:
        parent (tk.Tk | tk.Frame): The main window or parent frame.
        canvas (tk.Canvas): The canvas widget for drawing circuits.
        board (Breadboard): The Breadboard instance.
        model (list): The model data for the circuit.
        current_dict_circuit (dict): The current circuit data.
        zoom (Callable): The zoom function to adjust the canvas.
        com_port (str | None): The selected COM port.
    """

    def __init__(
        self,
        parent: tk.Tk | tk.Frame,
        canvas: tk.Canvas,
        board: Breadboard,
        current_dict_circuit: dict,
        zoom_function: Callable,
        sketcher: ComponentSketcher,

    ):
        """
        Initializes the custom menu bar.

        Parameters:
        - parent (tk.Tk or tk.Frame): The main window or parent frame.
        - canvas (tk.Canvas): The canvas widget for drawing circuits.
        - board (Breadboard): The Breadboard instance.
        - current_dict_circuit (dict): The current circuit data.
        - zoom_function (callable): The zoom function to adjust the canvas.
        """
        self.parent: tk.Tk | tk.Frame = parent
        """The main window or parent frame."""
        self.canvas: tk.Canvas = canvas
        """The canvas widget for drawing circuits."""
        self.board: Breadboard = board
        """The Breadboard instance."""
        self.current_dict_circuit: dict = current_dict_circuit
        """The current circuit data."""
        self.zoom: Callable = zoom_function
        """The zoom function to adjust the canvas."""
        self.sketcher = sketcher
        self.com_port: str | None = None
        """The selected COM port."""
        
        self.baud_rate = 115200
        self.timeout = 1
        self.serial_conn = None

        # Create the menu bar frame (do not pack here)
        self.menu_bar = tk.Frame(parent, bg="#333333")
        """The frame containing the menu bar buttons."""

        # Define menu items and their corresponding dropdown options
        menus = {
            "Fichier": ["Nouveau", "Ouvrir", "Enregistrer", "Quitter"],
            "Circuit": ["Vérification", "Téléverser"],
            "Controllers": ["Arduino", "ESP32", "STM32"],
            "Ports": ["Configurer le port série"],
            "Help": ["Documentation", "A propos"],
        }

        # Mapping menu labels to their handler functions
        menu_commands = {
            "Nouveau": self.new_file,
            "Ouvrir": self.open_file,
            "Enregistrer": self.save_file,
            "Quitter": self.parent.quit,
            "Vérification": self.checkCircuit,
            "Téléverser"  : self.download_script,
            "Arduino": self.Arduino,
            "ESP32": self.ESP32,
            "Configurer le port série": self.configure_ports,
            "Documentation": self.open_documentation,
            "A propos": self.about,
        }

        # Create each menu button and its dropdown
        for menu_name, options in menus.items():
            self.create_menu(menu_name, options, menu_commands)

        # Bind to parent to close dropdowns when clicking outside
        self.parent.bind("<Button-1>", self.close_dropdown, add="+")
        self.canvas.bind("<Button-1>", self.close_dropdown, add="+")

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
        )
        btn.pack(side="left")

        # Create the dropdown frame
        dropdown = tk.Frame(self.parent, bg="#333333", bd=1, relief="solid", width=200)

        # Calculate dropdown height based on number of options
        button_height = 30  # Approximate height of each dropdown button
        dropdown_height = button_height * len(options)
        dropdown.place(x=0, y=0, width=200, height=dropdown_height)  # Initial size based on options
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
                highlightbackground="#333333",  # Border color when inactive
                highlightcolor="#444444",  # Border color when active
                bd=0,
                anchor="w",
                width=200,
                padx=20,
                pady=5,
                font=("FiraCode-Bold", 12),
                command=menu_commands.get(option, lambda opt=option: print(f"{opt} selected")),
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
                        child.dropdown.place(x=btn_x, y=btn_y, width=200)
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
            self.is_descendant(event.widget, child.dropdown)
            for child in self.menu_bar.winfo_children()
            if isinstance(child, tk.Button) and hasattr(child, "dropdown")
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
                # Update current_dict_circuit and redraw the circuit
                self.board.sketcher.clear_board()

                # self.zoom(self.canvas, 10.0, self.board, 50, 10, [])
                x_o, y_o = self.board.sketcher.id_origins["xyOrigin"]
                self.board.sketcher.circuit(x_o, y_o, model=[])

                for key, val in circuit_data.items():
                    if "chip" in key:
                        x, y = val["XY"]
                        model_chip = [
                            (
                                self.board.sketcher.draw_chip,
                                1,
                                {
                                    **val,
                                    "matrix": self.board.sketcher.matrix,
                                },
                            )
                        ]
                        self.board.sketcher.circuit(x, y, model=model_chip)

                    elif "wire" in key:
                        model_wire = [
                            (
                                self.board.sketcher.draw_wire,
                                1,
                                {
                                    **val,
                                    "matrix": self.board.sketcher.matrix,
                                },
                            )
                        ]
                        self.board.sketcher.circuit(x_o, y_o, model=model_wire)
                    elif "io" in key:
                        model_io = [
                            (
                                self.board.sketcher.draw_pin_io,
                                1,
                                {
                                    **val,
                                    "matrix": self.board.sketcher.matrix,
                                },
                            )
                        ]
                        self.board.sketcher.circuit(x_o, y_o, model=model_io)
                    else:
                        print(f"Unspecified component: {key}")
                messagebox.showinfo("Open File", f"Circuit loaded from {file_path}")
            except Exception as e:
                print(f"Error loading file: {e}")
                messagebox.showerror("Open Error", f"An error occurred while opening the file:\n{e}")
                raise e
        else:
            print("Open file cancelled.")

    def save_file(self):
        """Handler for the 'Save' menu item."""
        print("Save File")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Extract the circuit data from current_dict_circuit
                circuit_data = deepcopy(self.current_dict_circuit)

                circuit_data.pop("last_id", None)  # Remove the "last_id" key
                for key, comp_data in circuit_data.items():
                    # Remove the "id" and "tags" keys before saving
                    comp_data.pop("id", None)
                    comp_data.pop("tags", None)
                    if "label" in comp_data:
                        comp_data["label"] = comp_data["type"]
                    if "wire" in key:
                        comp_data.pop("XY", None)  # Remove XY, will be recalculated anyway
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

        options = [comport.device for comport in serial.tools.list_ports.comports()]
        if len(options) == 0:
            message = "No COM ports available. Please connect a device and try again."
            print(message)
            messagebox.showwarning("No COM Ports", message)
        else:
            # Create a new top-level window for the dialog
            dialog = tk.Toplevel(self.parent)
            dialog.title("Configure Ports")

            # Set the size and position of the dialog
            dialog.geometry("300x150")

            # Create a label for the combobox
            label = tk.Label(dialog, text="Select an option:")
            label.pack(pady=10)
            # Create a combobox with the options
            combobox = ttk.Combobox(dialog, values=options)
            combobox.pack(pady=10)

            # Create a button to confirm the selection
            def confirm_selection():
                selected_option = combobox.get()
                print(f"Selected option: {selected_option}")
                self.com_port = selected_option
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
        """Ouvre le port série."""
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
        Envoie une chaîne de caractères sur le port série.
        :param data: Chaîne de caractères à envoyer.
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
        """Ferme le port série."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print(f"Port série {self.com_port} fermé.")
        else:
            print("Le port série est déjà fermé.")
            
    def download_script(self, script):
        self.open_port()
        self.send_data(script)
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

    def checkCircuit(self):
        print("Lancer la vérification")
        func = []
        wire = []
        pwrs = [(61, 1, "-"), (61, 2, "+")]  # [(col, line, "+" ou "-"), ...]
        pwrChip = {"+": [], "-": []}
        io = []
        pwrM, pwrP = [], []

        for id, component in self.current_dict_circuit.items():
            if id[:6] == "_chip_":
                (x, y) = component["pinUL_XY"]
                numPinBR = component["pinCount"] // 2
                (real_x, real_y), (col, line) = self.sketcher.find_nearest_grid_chip(x, y)
                ioIn, ioOut = [], []
                for io in component["io"]:  #  [([(ce1, le1), ...], "&", [(cs1, ls1), (cs2, ls2), ...]), ...]
                    # ioIN, ioOut = [], []
                    ioIn = [
                        (col + (numPin % numPinBR) - 1 + (numPin // numPinBR), line + 1 - (numPin // numPinBR))
                        for numPin in io[0]
                    ]
                    ioOut = [
                        (col + (numPin % numPinBR) - 1 + (numPin // numPinBR), line + 1 - (numPin // numPinBR))
                        for numPin in io[1]
                    ]
                    func += [(id, ioIn, component["symbScript"], ioOut)]
                    # print(f"ioIN  = {ioIn}")
                    # print(f"ioOUT = {ioOut}")
                    # print(f"func= {func}")
                    # print(f"ce1-ce2, func, cs1:({io[0][0]}-{io[0][1]} , {chip["symbScript"]} , {io[1][0]})")
                for pwr in component["pwr"]:
                    numPin, polarity = pwr[0], pwr[1]
                    col_pin = col + numPin - 1 if numPin <= numPinBR else col + (component["pinCount"] - numPin)
                    line_pin = line if numPin > numPinBR else line+1
                    pwrChip[polarity] += [
                        (id, col_pin, line_pin)
                    ]
                    # print(f"pwrChip= {pwrChip}")
            elif id[:6] == "_wire_":  # [(col1, line1,col2,line2), ...]
                wire += component["coord"]
        print(f"func= {func}\n")
        print(f"pwrChip= {pwrChip}\n")
        print(f"wire = {wire}")
        print(f"pwr = {pwrs}")
        for pwr in pwrs:
            (col, line, p) = pwr
            if p == "-":
                   pwrM = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
            else:  pwrP = deepcopy(self.board.sketcher.matrix[f"{col},{line}"]["link"])
        for w in wire:
            c1,l1,c2,l2 = w
            if self.is_linked_to(pwrM, (c1, l1)):
                    pwrM += self.board.sketcher.matrix[f"{c2},{l2}"]["link"]
            elif  self.is_linked_to(pwrP, (c1, l1)):  
                    pwrP += self.board.sketcher.matrix[f"{c2},{l2}"]["link"]
            if self.is_linked_to(pwrM, (c2, l2)):
                    pwrM += self.board.sketcher.matrix[f"{c1},{l1}"]["link"]
            elif  self.is_linked_to(pwrP, (c2, l2)):  
                    pwrP += self.board.sketcher.matrix[f"{c1},{l1}"]["link"]
            if (self.is_linked_to(pwrP, (c1, l1)) and self.is_linked_to(pwrM, (c1, l1))) or \
                (self.is_linked_to(pwrP, (c2, l2)) and self.is_linked_to(pwrM, (c2, l2))):
                print(f"CC dans le cable {w}")
        #pwrM.clear()
        #pwrP.clear()
        
