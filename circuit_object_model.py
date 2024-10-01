"""
This module defines classes and functions for modeling electronic components and circuits.
Classes:
- Package: Represents an electronic component package.
- ChipFunction: A base class representing a generic chip function.
- AndGate: Represents an AND gate chip function.
- OrGate: Represents an OR gate chip function.
- NotGate: Represents a NOT gate chip function.
- XorGate: Represents an XOR gate chip function.
- NandGate: Represents a NAND gate chip function.
- NorGate: Represents a NOR gate chip function.
- XnorGate: Represents an XNOR gate chip function.
- Chip: Represents an electronic chip composed of multiple functions.
- Wire: Represents a wire in a circuit (currently not implemented).
- Breadboard: Represents a breadboard for building circuits (currently not implemented).
- Circuit: Represents an electronic circuit (currently not implemented).
Usage:
------
The module can be used to load and represent electronic components and circuits from JSON files. 
The main block demonstrates loading packages and chips from JSON files in specified directories and
printing their details.
"""

from __future__ import annotations
from dataclasses import dataclass
import json
import os


@dataclass
class ConnectionPointID:
    """
    ConnectionPointID class represents an identifier for a connection point in a circuit model.
    Attributes:
        group (int): The group (top/bottom of divider) to which the connection point belongs.
        column_num (int): The column number of the connection point within the group.
    """

    group: int
    column_num: int


@dataclass
class ConnectionPoint:
    """
    Represents a connection point in a circuit.
    Attributes:
        connection_id (ConnectionPointID): The unique identifier for the connection point.
        connected_component (Pin | None): The component connected to this point, if any.
    """

    connection_id: ConnectionPointID
    connected_component: Pin | None


@dataclass
class Pin:
    """
    Represents a pin on an electronic component.
    Attributes:
        pin_num (int): The pin number.
        connection_point (ConnectionPoint): The connection point of the pin.
    """

    pin_num: int
    connection_point: ConnectionPoint


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


class ChipFunction:
    """
    A base class representing a generic chip function.

    This class serves as a template for specific chip functions.
    It contains a method that should be overridden by subclasses to
    implement the specific internal function of the chip to link inputs and outputs.
    """

    def __init__(self):
        raise NotImplementedError("Do not instantiate base ChipFunction.")

    def __str__(self) -> str:
        """
        Returns a string representation of the ChipFunction object.

        This method should be overridden by subclasses to provide
        a specific string representation of the chip function.

        Returns:
            str: A string representation of the chip function.
        """
        raise NotImplementedError("Function not implemented.")

    def chip_internal_function(self):
        """
        Placeholder for the chip's internal function linking the inputs and outputs.

        This method should be overridden by subclasses to provide
        the specific implementation of the chip's internal function.

        Raises:
            NotImplementedError: If the method is not overridden.
        """
        raise NotImplementedError("Function not implemented.")


class AndGate(ChipFunction):
    """
    Represents an AND gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the AND gate.
        chip_internal_function(): Placeholder for the internal function of the AND gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes an AND gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("AND gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("AND gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the AND gate.
        Returns:
            str: A string describing the AND gate with its input and output pins.
        """
        return f"AND Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the AND gate.
        This method should be implemented to define the behavior of the AND gate.
        """
        # TODO: Implement the internal function of the AND gate


class OrGate(ChipFunction):
    """
    Represents an OR gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the indices of the input pins.
        output_pins (list[Pin]): A tuple containing the index of the output pin.
    Methods:
        __str__(): Returns a string representation of the OR gate.
        chip_internal_function(): Placeholder for the internal logic of the OR gate.
    Raises:
        ValueError: If the number of input pins is less than two.
        ValueError: If the number of output pins is not exactly one.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes an OR gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pin numbers.
            output_pins (list[Pin]): A tuple containing the output pin number.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """

        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("OR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("OR gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the OR Gate object.
        The string includes the input pins and output pins of the OR Gate.
        Returns:
            str: A formatted string describing the OR Gate with its input and output pins.
        """

        return f"OR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        A placeholder method for the internal functionality of a chip.
        This method is intended to be overridden by subclasses to implement
        specific internal behaviors of a chip. Currently, it does nothing.
        Returns:
            None
        """
        # TODO: Implement the internal function of the OR gate


class NotGate(ChipFunction):
    """
    Represents a NOT gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pin number(s).
        output_pins (list[Pin]): A tuple containing the output pin number(s).
    Methods:
        __str__(): Returns a string representation of the NOT gate.
        chip_internal_function(): Placeholder for the internal logic of the NOT gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes a NOT gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pin number(s).
            output_pins (list[Pin]): A tuple containing the output pin number(s).
        Raises:
            ValueError: If the number of input pins is not exactly one.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) != 1:
            raise ValueError("NOT gate must have exactly one input pin.")
        if len(self.output_pins) != 1:
            raise ValueError("NOT gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the NOT gate.
        Returns:
            str: A string describing the NOT gate, including its input and output pins.
        """
        return f"NOT Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal logic of the NOT gate.
        """
        # TODO: Implement the internal function of the NOT gate


class XorGate(ChipFunction):
    """
    Represents an XOR gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the XOR gate.
        chip_internal_function(): Placeholder for the internal function of the XOR gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes an XOR gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("XOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("XOR gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the XOR gate.
        Returns:
            str: A string describing the XOR gate with its input and output pins.
        """
        return f"XOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the XOR gate.
        This method should be implemented to define the behavior of the XOR gate.
        """
        # TODO: Implement the internal function of the XOR gate


class NandGate(ChipFunction):
    """
    Represents a NAND gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the NAND gate.
        chip_internal_function(): Placeholder for the internal function of the NAND gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes a NAND gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("NAND gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("NAND gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the NAND gate.
        Returns:
            str: A string describing the NAND gate with its input and output pins.
        """
        return f"NAND Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the NAND gate.
        This method should be implemented to define the behavior of the NAND gate.
        """
        # TODO: Implement the internal function of the NAND gate


class NorGate(ChipFunction):
    """
    Represents a NOR gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the NOR gate.
        chip_internal_function(): Placeholder for the internal function of the NOR gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes a NOR gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("NOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("NOR gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the NOR gate.
        Returns:
            str: A string describing the NOR gate with its input and output pins.
        """
        return f"NOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the NOR gate.
        This method should be implemented to define the behavior of the NOR gate.
        """
        # TODO: Implement the internal function of the NOR gate


class XnorGate(ChipFunction):
    """
    Represents an XNOR gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the XNOR gate.
        chip_internal_function(): Placeholder for the internal function of the XNOR gate.
    """

    def __init__(self, input_pins: list[Pin], output_pins: list[Pin]):
        """
        Initializes an XNOR gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("XNOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("XNOR gate must have exactly one output pin.")

    def __str__(self):
        """
        Returns a string representation of the XNOR gate.
        Returns:
            str: A string describing the XNOR gate with its input and output pins.
        """
        return f"XNOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the XNOR gate.
        This method should be implemented to define the behavior of the XNOR gate.
        """
        # TODO: Implement the internal function of the XNOR gate


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

        functions: list[ChipFunction] = []
        for func_data in json_data["functions"]:
            func_type = func_data["func_type"]
            if func_type == "AND":
                functions.append(AndGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "OR":
                functions.append(OrGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "NOT":
                functions.append(NotGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "XOR":
                functions.append(XorGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "NAND":
                functions.append(NandGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "NOR":
                functions.append(NorGate(func_data["input_pins"], func_data["output_pins"]))
            elif func_type == "XNOR":
                functions.append(XnorGate(func_data["input_pins"], func_data["output_pins"]))
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

    start_pin: Pin
    end_pin: Pin


class Breadboard:
    """
    A class to represent a breadboard used in electronic circuits.

    It stores the info on the size of the board, the pin groupings, the power rails
    Attributes:
    -----------
        TODO
    Methods:
    --------
        TODO
    """

    # TODO: implement breadboard class


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

    def __init__(self, breadboard: Breadboard):
        self.breadboard = breadboard
        self.chips: list[Chip] = []
        self.wires: list[Wire] = []

    def add_chip(self, new_chip: Chip, top_left_connection: ConnectionPointID):
        # TODO
        pass

    def add_wire(self, start_pin: Pin, end_pin: Pin):
        """
        Adds a wire to the circuit connecting the specified pins.
        Args:
            start_pin (Pin): The starting pin of the wire.
            end_pin (Pin): The ending pin of the wire.
        """
        self.wires.append(Wire(start_pin, end_pin))

    def validate_pins(self):
        """
        Validates the pins and connections in the circuit.
        Ensures that all pins are correctly connected and that there are no conflicts.
        """
        # TODO: Implement pin validation logic

    def get_logic_functions(self):
        """
        Returns the logic functions of the circuit by following connections and calling internal_chip_function.
        Returns:
            dict: A dictionary mapping output pins to their logic functions.
        """
        logic_functions = {}
        # TODO: Implement logic to follow connections and call internal_chip_function
        return logic_functions


if __name__ == "__main__":
    packages = {}
    PACKAGES_DIR = "./Components/Packages"
    for filename in os.listdir(PACKAGES_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(PACKAGES_DIR, filename), "r", encoding="utf-8") as file:
                pkg_data = json.load(file)
                package = Package.from_json(pkg_data)
                packages[package.type_name] = package

    chips = {}
    CHIPS_DIR = "./Components/Chips"
    for root, _, files in os.walk(CHIPS_DIR):
        for filename in files:
            if filename.endswith(".json"):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                    chip_data = json.load(file)
                    chip = Chip.from_json(chip_data, packages)
                    chips[chip.name] = chip

    print("-------------------LOADED PACKAGES-------------------")
    for package in packages.values():
        print(package)

    print("--------------------LOADED CHIPS:--------------------")
    for chip in chips.values():
        print(chip)
