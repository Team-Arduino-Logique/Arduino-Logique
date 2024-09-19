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

import json
import os


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
        raise NotImplementedError("Do not instanciate base ChipFunction.")

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
        input_pins (tuple[int]): A tuple containing the input pins.
        output_pins (tuple[int]): A tuple containing the output pins.
    Methods:
        __str__(): Returns a string representation of the AND gate.
        chip_internal_function(): Placeholder for the internal function of the AND gate.
    """

    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        """
        Initializes an AND gate with the specified input and output pins.
        Args:
            input_pins (tuple[int]): A tuple containing the input pins.
            output_pins (tuple[int]): A tuple containing the output pin.
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
        input_pins (tuple[int]): A tuple containing the indices of the input pins.
        output_pins (tuple[int]): A tuple containing the index of the output pin.
    Methods:
        __str__(): Returns a string representation of the OR gate.
        chip_internal_function(): Placeholder for the internal logic of the OR gate.
    Raises:
        ValueError: If the number of input pins is less than two.
        ValueError: If the number of output pins is not exactly one.
    """

    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        """
        Initializes an OR gate with the specified input and output pins.
        Args:
            input_pins (tuple[int]): A tuple containing the input pin numbers.
            output_pins (tuple[int]): A tuple containing the output pin number.
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
        input_pins (tuple[int]): A tuple containing the input pin number(s).
        output_pins (tuple[int]): A tuple containing the output pin number(s).
    Methods:
        __str__(): Returns a string representation of the NOT gate.
        chip_internal_function(): Placeholder for the internal logic of the NOT gate.
    """

    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        """
        Initializes a NOT gate with the specified input and output pins.
        Args:
            input_pins (tuple[int]): A tuple containing the input pin number(s).
            output_pins (tuple[int]): A tuple containing the output pin number(s).
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
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("XOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("XOR gate must have exactly one output pin.")

    def __str__(self):
        return f"XOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        pass


class NandGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("NAND gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("NAND gate must have exactly one output pin.")

    def __str__(self):
        return f"NAND Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        pass


class NorGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("NOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("NOR gate must have exactly one output pin.")

    def __str__(self):
        return f"NOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        pass


class XnorGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("XNOR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("XNOR gate must have exactly one output pin.")

    def __str__(self):
        return f"XNOR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def chip_internal_function(self):
        pass


class Chip:
    def __init__(self, name: str, pkg: Package, functions: tuple[ChipFunction]):
        self.name = name
        self.package = pkg
        self.functions = functions

    @staticmethod
    def from_json(json_data: dict, package_dict: dict[str, Package] = None):
        functions = []
        for func_data in json_data["functions"]:
            func_type = func_data["func_type"]
            input_pins = tuple(func_data["input_pins"])
            output_pins = tuple(func_data["output_pins"])
            if func_type == "AND":
                functions.append(AndGate(input_pins, output_pins))
            elif func_type == "OR":
                functions.append(OrGate(input_pins, output_pins))
            elif func_type == "NOT":
                functions.append(NotGate(input_pins, output_pins))
            elif func_type == "XOR":
                functions.append(XorGate(input_pins, output_pins))
            elif func_type == "NAND":
                functions.append(NandGate(input_pins, output_pins))
            elif func_type == "NOR":
                functions.append(NorGate(input_pins, output_pins))
            elif func_type == "XNOR":
                functions.append(XnorGate(input_pins, output_pins))
            else:
                raise ValueError(f"Unknown function type: {func_type}")

        if package_dict is not None and isinstance(json_data["package"], str):
            return Chip(json_data["name"], package_dict[json_data["package"]], tuple(functions))

        raise ValueError("The package does not exist in the Components/Packages directory.")

    def __str__(self):
        new_line = "\n\t"
        return f"Chip:\t{self.name}\t\n{self.package},\t\nFunctions:\n\t{new_line.join(str(func) for func in self.functions)}"


class Wire:
    pass


class Breadboard:
    pass


class Circuit:
    def __init__(self):
        pass


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
    for filename in os.listdir(CHIPS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(CHIPS_DIR, filename), "r", encoding="utf-8") as file:
                chip_data = json.load(file)
                chip = Chip.from_json(chip_data, packages)
                chips[chip.name] = chip

    print("-------------------LOADED PACKAGES-------------------")
    for package in packages.values():
        print(package)

    print("--------------------LOADED CHIPS:--------------------")
    for chip in chips.values():
        print(chip)
