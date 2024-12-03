"""
This module defines classes and functions for representing and manipulating electronic circuit components,
such as packages, chips, wires, and breadboards. It includes functionality for loading component data from JSON files,
creating instances of these components, and managing their interactions within a circuit.

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

from .chip_functions import (
    AndGate,
    BinaryCounter,
    ChipFunction,
    DFlipFlop,
    Demux,
    JKFlipFlop,
    LogicalFunction,
    Mux,
    NandGate,
    NorGate,
    NotGate,
    OrGate,
    XnorGate,
    XorGate,
)
from .circuit_util_elements import ConnectionPointID, FunctionRepresentation, Pin


@dataclass
class Package:
    """
    A class used to represent an electronic component package.
    Attributes:
        type_name (str): The name of the package type.
        chip_width (float): The width of the package.
        pin_count (int): The number of pins on the package.
    """

    type_name: str
    chip_width: float
    pin_count: int

    @staticmethod
    def from_json(json_data: dict):
        """
        Constructs a Package object from a JSON dictionary.
        Parameters:
            json_data : dict - The JSON dictionary containing the package data.
        Returns:
            Package - The Package object constructed from the JSON data.
        """
        return Package(json_data["type_name"], json_data["chip_width"], json_data["pin_count"])


class Chip:
    """
    Represents an integrated circuit chip with a specific package and a set of functions.
    Attributes:
        element_id (str): The unique identifier of the chip.
        chip_type (str): The type of the chip (e.g., "74HCXX").
        description (str): A description of the chip.
        package_name (str): The name of the package associated with the chip.
        pin_count (int): The number of pins on the chip.
        chip_width (float): The width of the chip.
        functions (list[ChipFunction]): A list of functions performed by the chip.
        position (ConnectionPointID, optional): The position of the chip on the breadboard.
    """

    def __init__(
        self,
        element_id: str,
        chip_type: str | None = None,
        description: str | None = None,
        pkg: Package | None = None,
        functions: list[ChipFunction] | None = None,
        vcc: Pin | None = None,
        gnd: Pin | None = None,
        position: ConnectionPointID | None = None,
        model: Chip | None = None,
    ):
        """
        Initializes a Chip instance.
        Args:
            element_id (str): The unique identifier of the chip.
            chip_type (str): The chip_type of the chip (74HCXX).
            description (str): A description of the chip.
            pkg (Package): The package associated with the chip.
            functions (list[ChipFunction]): A list containing the functions of the chip.
            position (ConnectionPointID, optional): The position of the chip on the breadboard (from the top left pin).
                                                    Defaults to None.
        """
        self.element_id = element_id
        if (
            chip_type is not None
            and description is not None
            and pkg is not None
            and functions is not None
            and vcc is not None
            and gnd is not None
            and model is None
        ):
            self.chip_type = chip_type
            self.description = description
            self.package_name: str = pkg.type_name
            self.pin_count: int = pkg.pin_count
            self.chip_width: float = pkg.chip_width
            self.functions: list[ChipFunction] = functions
            self.vcc = vcc
            self.gnd = gnd
            if position is not None:
                for fn in self.functions:
                    fn.calculate_pin_pos(position, 1, self.pin_count)
            self.position: ConnectionPointID | None = position
            if position is not None:
                self.set_position(position)
        elif model is not None:
            self.chip_type = model.chip_type
            self.description = model.description
            self.package_name = model.package_name
            self.pin_count = model.pin_count
            self.chip_width = model.chip_width
            self.functions = model.functions
            self.vcc = model.vcc
            self.gnd = model.gnd
        else:
            raise ValueError("Invalid parameters provided.")

    def set_position(self, position: ConnectionPointID):
        """
        Sets the position of the chip on the breadboard.
        Args:
            position (ConnectionPointID): The position of the chip on the breadboard.
        """
        self.position = position
        for fn in self.functions:
            fn.calculate_pin_pos(position, self.pin_count, self.pin_count)

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
            "AND": lambda data: AndGate(data["input_pins"], data["output_pins"]),
            "OR": lambda data: OrGate(data["input_pins"], data["output_pins"]),
            "NOT": lambda data: NotGate(data["input_pins"], data["output_pins"]),
            "XOR": lambda data: XorGate(data["input_pins"], data["output_pins"]),
            "NAND": lambda data: NandGate(data["input_pins"], data["output_pins"]),
            "NOR": lambda data: NorGate(data["input_pins"], data["output_pins"]),
            "XNOR": lambda data: XnorGate(data["input_pins"], data["output_pins"]),
            "MUX": lambda data: Mux(
                data["input_pins"],
                data["output_pins"],
                data["inv_output_pins"],
                data["select_pins"],
                data["enable_pins"],
                data["inv_enable_pins"],
            ),
            "DEMUX": lambda data: Demux(
                data["input_pins"],
                data["output_pins"],
                data["enable_pins"],
                data["inv_enable_pins"],
            ),
            "D_FLIP_FLOP": lambda data: DFlipFlop(
                data["clock_pin"],
                data["clock_type"],
                data["reset_pin"],
                data["inv_reset_pin"],
                data["set_pin"],
                data["inv_set_pin"],
                data["data_pin"],
                data["output_pin"],
                data["inv_output_pin"],
            ),
            "JK_FLIP_FLOP": lambda data: JKFlipFlop(
                data["clock_pin"],
                data["clock_type"],
                data["reset_pin"],
                data["inv_reset_pin"],
                data["set_pin"],
                data["inv_set_pin"],
                data["j_input_pin"],
                data["inv_j_input_pin"],
                data["k_input_pin"],
                data["inv_k_input_pin"],
                data["output_pin"],
                data["inv_output_pin"],
            ),
            "BINARY_COUNTER": lambda data: BinaryCounter(
                data["clock_pin"],
                data["clock_type"],
                data["reset_pin"],
                data["inv_reset_pin"],
                data["count_enable_pin"],
                data["inv_count_enable_pin"],
                data["load_enable_pin"],
                data["inv_load_enable_pin"],
                data["up_down_input_pin"],
                data["inv_up_down_input_pin"],
                data["terminal_count_pin"],
                data["ripple_clock_output_pin"],
                data["data_pins"],
                data["output_pins"],
            ),
        }

        functions: list[ChipFunction] = []
        for func_data in json_data["functions"]:
            func_type = func_data["func_type"]
            if func_type in function_creators:
                functions.append(function_creators[func_type](func_data))
            else:
                raise ValueError(f"Unknown function type: {func_type}")

        if package_dict is not None and isinstance(json_data["package"], str):
            return Chip(
                json_data["name"],
                json_data["name"],
                json_data["description"],
                package_dict[json_data["package"]],
                functions,
                Pin(json_data["vcc_pin"], None),
                Pin(json_data["gnd_pin"], None),
            )

        raise ValueError("The package does not exist in the Components/Packages directory.")

    def to_generic_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the Chip object.
        Returns:
            dict: A dictionary containing the attributes of the Chip object, without position and instance info.
        """
        attr_dict = {
            "label": self.chip_type,
            "description": self.description,
            "type": self.chip_type,
            "packageName": self.package_name,
            "pinCount": self.pin_count,
            "chipWidth": self.chip_width,
            "pwr": [(self.vcc.pin_num, "+"), (self.gnd.pin_num, "-")],
        }

        if self.functions:
            attr_dict["logicFunctionName"] = self.functions[0].__class__.__name__
            attr_dict["io"] = [
                ([pin.pin_num for pin in func.input_pins], [pin.pin_num for pin in func.output_pins])
                for func in self.functions
                #if isinstance(func, LogicalFunction) and not isinstance(func, Mux) and not isinstance(func, Demux)
                if isinstance(func, LogicalFunction) or  isinstance(func, Mux) or isinstance(func, Demux)
            ]
            attr_dict["io_select"] = [
                [pin.pin_num for pin in func.select_pins]
                for func in self.functions
                #if isinstance(func, LogicalFunction) and not isinstance(func, Mux) and not isinstance(func, Demux)
                if isinstance(func, Mux) 
            ]
            attr_dict["io_out_inv"] = [
                [pin.pin_num for pin in func.inv_output_pins]
                for func in self.functions
                #if isinstance(func, LogicalFunction) and not isinstance(func, Mux) and not isinstance(func, Demux)
                if isinstance(func, Mux) 
            ]
            attr_dict["io_enable"] = [
                [pin.pin_num for pin in func.enable_pins]
                for func in self.functions
                #if isinstance(func, LogicalFunction) and not isinstance(func, Mux) and not isinstance(func, Demux)
                if isinstance(func, Mux) or  isinstance(func, Demux)
            ]
            attr_dict["io_enable_inv"] = [
                [pin.pin_num for pin in func.inv_enable_pins]
                for func in self.functions
                #if isinstance(func, LogicalFunction) and not isinstance(func, Mux) and not isinstance(func, Demux)
                if isinstance(func, Mux) or  isinstance(func, Demux)
            ]
        return attr_dict

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
            f"Chip:\t{self.element_id}"
            f"\nPackage: {self.package_name},"
            f"\nChip width: {self.chip_width},"
            f"\nPin count: {self.pin_count},"
            f"\nFunctions:"
            f"\n\t{new_line.join(str(func) for func in self.functions)}"
        )


@dataclass
class Wire:
    """
    Represents a wire in a circuit.
    Attributes:
        element_id: The unique identifier of the wire.
        start_pin: The starting pin of the wire.
        end_pin: The ending pin of the wire.
    """

    element_id: str
    start: ConnectionPointID
    end: ConnectionPointID


@dataclass
class IO:
    """
    Represents an input/output component in a circuit.
    Attributes:
        element_id: The unique identifier of the IO component.
        position: The position of the IO component on the breadboard.
    """

    element_id: str
    position: ConnectionPointID


class Circuit:
    """
    Represents an electronic circuit with chip, wire, io and power components.
    Attributes:
        chips (dict[str, Chip]): A dictionary of chips in the circuit, indexed by label.
        wires (dict[str, Wire]): A dictionary of wires in the circuit, indexed by label.
        io (dict[str, IO]): A dictionary of input/output components in the circuit, indexed by label.
        power (dict[str, Power]): A dictionary of power components in the circuit, indexed by label.
    """

    def __init__(self) -> None:
        self.chips: dict[str, Chip] = {}
        self.wires: dict[str, Wire] = {}
        self.io: dict[str, IO] = {}
        # self.power: dict[str, Power] = {}

    def add_chip(self, new_chip: Chip) -> None:
        """
        Adds a chip to the circuit.
        Args:
            new_chip (Chip): The chip to add to the circuit.
        """
        self.chips[new_chip.element_id] = new_chip

    def remove_chip(self, element_id) -> bool:
        """
        Removes a chip from the circuit.
        Args:
            element_id (str): The unique identifier of the chip to remove.
        Returns:
            bool: True if the chip was removed successfully, False otherwise.
        """
        ret = self.chips.pop(element_id, None)
        return ret is not None

    def add_wire(self, wire: Wire) -> None:
        """
        Adds a wire to the circuit.
        Args:
            wire (Wire): The wire to add to the circuit.
        """
        self.wires[wire.element_id] = wire

    def remove_wire(self, element_id) -> bool:
        """
        Removes a wire from the circuit.
        Args:
            element_id (str): The unique identifier of the wire to remove.
        Returns:
            bool: True if the wire was removed successfully, False otherwise.
        """
        ret = self.wires.pop(element_id, None)
        return ret is not None

    def add_io(self, io: IO) -> None:
        """
        Adds an input/output component to the circuit.
        Args:
            io (IO): The input/output component to add to the circuit.
        """
        self.io[io.element_id] = io

    def remove_io(self, element_id) -> bool:
        """
        Removes an input/output component from the circuit.
        Args:
            element_id (str): The unique identifier of the input/output component to remove.
        Returns:
            bool: True if the input/output component was removed successfully, False otherwise.
        """
        ret = self.io.pop(element_id, None)
        return ret is not None

    def get_func_list(self) -> list[FunctionRepresentation]:
        """
        Returns a list of function representations for all the chips in the circuit.
        """
        ret_list: list[FunctionRepresentation] = []
        for circuit_chip in self.chips.values():
            for func in circuit_chip.functions:
                ret_list.append(func.chip_internal_function())
        return ret_list

    def trace_functions(self):
        """
        Traces the functions of the chips in the circuit.
        """
        funcs = self.get_func_list()
        # TODO KHALID


def get_all_available_chips() -> dict[str, Chip]:
    """
    Returns a dictionary of all available chips.
    """
    file_errors = []
    available_packages = {}
    pkgs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Components", "Packages")
    for filename in os.listdir(pkgs_dir):
        if filename.endswith(".json"):
            with open(os.path.join(pkgs_dir, filename), "r", encoding="utf-8") as file:
                pkg_data = json.load(file)
                try:
                    package = Package.from_json(pkg_data)
                    available_packages[package.type_name] = package
                except ValueError as e:
                    file_errors.append(f"Error loading package from {filename}: {e}")

    all_chips = {}
    chips_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Components", "Chips")
    for root, _, files in os.walk(chips_dir):
        for filename in files:
            if filename.endswith(".json"):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                    chip_data = json.load(file)
                    try:
                        new_chip = Chip.from_json(chip_data, available_packages)
                        all_chips[new_chip.chip_type] = new_chip
                    except ValueError as e:
                        file_errors.append(f"Error loading chip from {filename}: {e}")

    if file_errors:
        print("--------------------ERRORS---------------------")
        for error in file_errors:
            print(error)

    return all_chips


def get_chip_modification_times() -> dict[str, float]:
    """
    Returns a dictionary of chip modification times.
    """
    chip_mod_times = {}
    chips_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Components", "Chips")
    for root, _, files in os.walk(chips_dir):
        for filename in files:
            if filename.endswith(".json"):
                chip_mod_times[filename] = os.path.getmtime(os.path.join(root, filename))
    return chip_mod_times


if __name__ == "__main__":
    available_chips = get_all_available_chips()
    print("--------------------LOADED CHIPS:--------------------")
    for chip in available_chips.values():
        print(chip)

    # Example usage of the Circuit class
    circuit = Circuit()
    new_chip_to_add: Chip = Chip("74HC08-1", model=available_chips["74HC08"])
    new_chip_to_add.set_position(ConnectionPointID(10, 10))
    circuit.add_chip(new_chip_to_add)

    new_chip_to_add = Chip("74HC08-2", model=available_chips["74HC08"])
    new_chip_to_add.set_position(ConnectionPointID(100, 100))
    circuit.add_chip(new_chip_to_add)

    new_chip_to_add = Chip("74HC151-1", model=available_chips["74HC151"])
    new_chip_to_add.set_position(ConnectionPointID(20, 20))
    circuit.add_chip(new_chip_to_add)

    new_chip_to_add = Chip("74HC191", model=available_chips["74HC191"])
    new_chip_to_add.set_position(ConnectionPointID(30, 30))
    circuit.add_chip(new_chip_to_add)

    print(circuit.get_func_list())
