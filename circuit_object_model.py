from enum import Enum
import json
import os
from utils import Dimensions


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


class ChipFunctionTypes(Enum):
    pass


class ChipFunction:
    def function(self):
        raise NotImplementedError("Function not implemented.")


class AndGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("AND gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("AND gate must have exactly one output pin.")

    def __str__(self):
        return f"AND Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def function(self):
        pass


class OrGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) < 2:
            raise ValueError("OR gate must have at least two input pins.")
        if len(self.output_pins) != 1:
            raise ValueError("OR gate must have exactly one output pin.")

    def __str__(self):
        return f"OR Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def function(self):
        pass


class NotGate(ChipFunction):
    def __init__(self, input_pins: tuple[int], output_pins: tuple[int]):
        self.input_pins = input_pins
        self.output_pins = output_pins
        if len(self.input_pins) != 1:
            raise ValueError("NOT gate must have exactly one input pin.")
        if len(self.output_pins) != 1:
            raise ValueError("NOT gate must have exactly one output pin.")

    def __str__(self):
        return f"NOT Gate:\n\t\tInput Pins: {self.input_pins},\n\t\tOutput Pins: {self.output_pins}"

    def function(self):
        pass


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

    def function(self):
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

    def function(self):
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

    def function(self):
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

    def function(self):
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
    def __init__(self, size: Dimensions):
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
