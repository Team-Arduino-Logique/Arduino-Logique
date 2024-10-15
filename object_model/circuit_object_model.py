"""
This module defines classes and functions for representing and manipulating electronic circuit components,
such as packages, chips, wires, and breadboards. It includes functionality for loading component data from JSON files,
creating instances of these components, and managing their interactions within a circuit.
Classes:
- Package: Represents an electronic component package with attributes like type name, chip width, and pin count.
- Chip: Represents an integrated circuit chip with a specific package and a set of functions.
- Wire: Represents a wire in a circuit, connecting two pins.
- Breadboard: Represents a breadboard used in electronic circuits.
- Circuit: Represents an electronic circuit, managing chips, wires, and their connections on a breadboard.
Functions:
- Package.from_json(json_data: dict) -> Package: Constructs a Package object from a JSON dictionary.
- Chip.from_json(json_data: dict, 
                package_dict: dict[str, Package] | None = None) -> Chip:
                Creates a Chip object from JSON data.
Usage:
------
The module can be used to load component data from JSON files, create instances of packages and chips, and manage their
interactions within a circuit. The main script demonstrates loading packages and chips from JSON files and printing
their details.
"""

from __future__ import annotations
from dataclasses import dataclass
import json
import os
from typing import Callable, Dict, Any

from breadboard import Breadboard

from .chip_functions import (
    ChipFunction,
    create_and_gate,
    create_binary_counter,
    create_d_flip_flop,
    create_demux,
    create_jk_flip_flop,
    create_mux,
    create_nand_gate,
    create_nor_gate,
    create_not_gate,
    create_or_gate,
    create_xnor_gate,
    create_xor_gate,
)
from .circuit_util_elements import ConnectionPoint, ConnectionPointID, Pin


class Package:
    """
    A class used to represent an electronic component package.
    Attributes
    ----------
    type_name : str
        The type name of the package (e.g., DIP, QFP).
    chip_width : float
        The width of the chip.
    pin_count : int
        The number of pins in the package.
    Methods
    -------
    __str__():
        Returns a string representation of the Package object.
    __eq__(other):
        Checks if two Package objects are equal.
    from_json(json_data: dict):
        Constructs a Package object from a JSON dictionary.
    """

    def __init__(self, type_name: str, chip_width: float, pin_count: int):
        self.type_name = type_name
        self.chip_width = chip_width
        self.pin_count = pin_count

    def __str__(self):
        return f"Package:\t\n\t{self.type_name},\t\n\tChip Width: {self.chip_width},\t\n\tPin Count: {self.pin_count}"

    def __eq__(self, other):
        if isinstance(other, Package):
            return (
                self.type_name == other.type_name
                and self.chip_width == other.chip_width
                and self.pin_count == other.pin_count
            )
        return False

    @staticmethod
    def from_json(json_data: dict):
        """
        Constructs a Package object from a JSON dictionary.
        Parameters:
        -----------
        json_data : dict
            The JSON dictionary containing the package data.
        Returns:
        --------
        Package
            The Package object constructed from the JSON data.
        """
        return Package(json_data["type_name"], json_data["chip_width"], json_data["pin_count"])


class Chip:
    """
    Represents an integrated circuit chip with a specific package and a set of functions.
    Attributes:
        name (str): The name of the chip.
        package (Package): The package type of the chip.
        functions (tuple[ChipFunction]): A tuple containing the functions of the chip.
    Methods:
        from_json(json_data: dict, package_dict: dict[str, Package] = None) -> Chip:
            Creates a Chip instance from a JSON dictionary.
        __str__() -> str:
            Returns a string representation of the Chip instance.
    """

    def __init__(self, name: str, pkg: Package, functions: list[ChipFunction]):
        """
        Initializes a CircuitObject instance.
        Args:
            name (str): The name of the circuit object.
            pkg (Package): The package associated with the circuit object.
            functions (list[ChipFunction]): A list containing the functions of the chip.
        """

        self.name: str = name
        self.package: Package = pkg
        # TODO get number of pins from package and assign to functions
        self.functions: list[ChipFunction] = functions


    @staticmethod
    def from_json(json_data: dict, package_dict: dict[str, Package] | None = None):
        """
        Create a Chip object from JSON data.
        Args:
            json_data (dict): A dictionary containing the JSON data to create the Chip object.
                Expected keys:
                    - "functions" (list): A list of dictionaries, each representing a function.
                        Each dictionary should have the following keys:
                            - "func_type" (str): The type of the function (e.g., "AND", "OR", etc.).
                            - "input_pins" (list): A list of input pin identifiers.
                            - "output_pins" (list): A list of output pin identifiers.
                    - "package" (str): The name of the package.
                    - "name" (str): The name of the chip.
            package_dict (dict[str, Package], optional): A dictionary mapping package names to Package objects.
                Defaults to None.
        Returns:
            Chip: A Chip object created from the provided JSON data.
        Raises:
            ValueError: If an unknown function type is encountered or if the package does not exist
            in the provided package_dict.
        """

        function_creators: Dict[str, Callable[[Dict[str, Any]], ChipFunction]] = {
            "AND": create_and_gate,
            "OR": create_or_gate,
            "NOT": create_not_gate,
            "XOR": create_xor_gate,
            "NAND": create_nand_gate,
            "NOR": create_nor_gate,
            "XNOR": create_xnor_gate,
            "MUX": create_mux,
            "DEMUX": create_demux,
            "D_FLIP_FLOP": create_d_flip_flop,
            "JK_FLIP_FLOP": create_jk_flip_flop,
            "BINARY_COUNTER": create_binary_counter,
        }

        functions: list[ChipFunction] = []
        for func_data in json_data["functions"]:
            func_type = func_data["func_type"]
            if func_type in function_creators:
                functions.append(function_creators[func_type](func_data))
            else:
                raise ValueError(f"Unknown function type: {func_type}")

        if package_dict is not None and isinstance(json_data["package"], str):
            return Chip(json_data["name"], package_dict[json_data["package"]], functions)

        raise ValueError("The package does not exist in the Components/Packages directory.")

    def __str__(self):
        """
        Returns a string representation of the Chip object.
        The string includes the chip's name, package type, and a list of its functions.
        Each function is displayed on a new line with indentation for better readability.
        Returns:
            str: A formatted string representing the Chip object.
        """

        new_line = "\n\t"
        return (
            f"Chip:\t{self.name}"
            f"\n{self.package},"
            f"\nFunctions:"
            f"\n\t{new_line.join(str(func) for func in self.functions)}"
        )


@dataclass
class Wire:
    """
    Represents a wire in a circuit.
    Attributes:
        start_pin: The starting pin of the wire.
        end_pin: The ending pin of the wire.
    """

    start: ConnectionPointID
    end: ConnectionPointID


class Circuit:
    """
    Represents an electronic circuit.
    Attributes:
        breadboard (Breadboard): The breadboard used in the circuit.
        chips (list[Chip]): A list of chips placed on the breadboard.
        wires (list[Wire]): A list of wires connecting the chips.
    Methods:
        add_chip(chip: Chip, position: tuple[int, int]): Adds a chip to the circuit at the specified position.
        add_wire(start_pin: int, end_pin: int): Adds a wire to the circuit connecting the specified pins.
        validate_pins(): Validates the pins and connections in the circuit.
        get_logic_functions(): Returns the logic functions of the circuit by following connections and
                                calling internal_chip_function.
    """

    # TODO make the class
    def __init__(self, breadboard: Breadboard):
        self.breadboard = breadboard
        self.chips: list[Chip] = []
        self.wires: list[Wire] = []

    def add_chip(self, new_chip: Chip, top_left_connection: ConnectionPointID):
        """
        Adds a chip to the circuit at the specified position.
        """


    def add_wire(self, start: ConnectionPointID, end: ConnectionPointID):
        """
        Adds a wire to the circuit connecting the specified pins.
        Args:
            start_pin (Pin): The starting pin of the wire.
            end_pin (Pin): The ending pin of the wire.
        """



    def validate_pins(self):
        """
        Validates the pins and connections in the circuit.
        Ensures that all pins are correctly connected and that there are no conflicts.
        """

    def get_logic_functions(self):
        """
        Returns the logic functions of the circuit by following connections and calling internal_chip_function.
        Returns:
            dict: A dictionary mapping output pins to their logic functions.
        """
        logic_functions = {}
        return logic_functions


if __name__ == "__main__":
    file_errors = []
    packages = {}
    PACKAGES_DIR = "./Components/Packages"
    for filename in os.listdir(PACKAGES_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(PACKAGES_DIR, filename), "r", encoding="utf-8") as file:
                pkg_data = json.load(file)
                try:
                    package = Package.from_json(pkg_data)
                    packages[package.type_name] = package
                except ValueError as e:
                    file_errors.append(f"Error loading package from {filename}: {e}")

    chips = {}
    CHIPS_DIR = "./Components/Chips"
    for root, _, files in os.walk(CHIPS_DIR):
        for filename in files:
            if filename.endswith(".json"):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                    chip_data = json.load(file)
                    try:
                        chip = Chip.from_json(chip_data, packages)
                        chips[chip.name] = chip
                    except ValueError as e:
                        file_errors.append(f"Error loading chip from {filename}: {e}")

    print("-------------------LOADED PACKAGES-------------------")
    for package in packages.values():
        print(package)

    print("--------------------LOADED CHIPS:--------------------")
    for chip in chips.values():
        print(chip)

    if file_errors:
        print("--------------------ERRORS---------------------")
        for error in file_errors:
            print(error)

    # Example usage of the Circuit class

