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
from math import log2
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


class Mux(ChipFunction):
    """
    Represents a multiplexer in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
        inv_output_pins (list[Pin]): A tuple containing the inverted output pins.
        select_pins (list[Pin]): A tuple containing the select pins.
        enable_pins (list[Pin]): A tuple containing the active HIGH enable pins.
        inv_enable_pins (list[Pin]): A tuple containing the active LOW enable pins.
    Methods:
        __str__(): Returns a string representation of the MUX.
        chip_internal_function(): Placeholder for the internal function of the MUX.
    """

    def __init__(
        self,
        input_pins: list[Pin],
        output_pins: list[Pin],
        inv_output_pins: list[Pin],
        select_pins: list[Pin],
        enable_pins: list[Pin],
        inv_enable_pins: list[Pin],
    ):
        """
        Initializes a Mux with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pins.
            inv_output_pins (list[Pin]): A tuple containing the inverted output pins.
            select_pins (list[Pin]): A tuple containing the select pins.
            enable_pins (list[Pin]): A tuple containing the active HIGH enable pins.
            inv_enable_pins (list[Pin]): A tuple containing the active LOW enable pins.
        Raises:

        """
        self.input_pins = input_pins
        self.output_pins = output_pins
        self.inv_output_pins = inv_output_pins
        self.select_pins = select_pins
        self.enable_pins = enable_pins
        self.inv_enable_pins = inv_enable_pins
        if len(self.input_pins) < 2:
            raise ValueError("MUX must have at least two input pins.")
        if len(self.output_pins) < 1 or len(self.inv_output_pins) < 1:
            raise ValueError("MUX must have at least one output pin or inverted output pin.")
        if len(self.select_pins) != log2(len(self.input_pins)):
            raise ValueError("MUX must have log2(num input pins) select pins.")

    def __str__(self):
        """
        Returns a string representation of the MUX.
        Returns:
            str: A string describing the MUX with its input and output pins.
        """
        return (
            f"MUX:\n\t\tInput Pins: {self.input_pins},"
            f"\n\t\tOutput Pins: {self.output_pins},"
            f"\n\t\tInverted Output Pins: {self.inv_output_pins},"
            f"\n\t\tSelect Pins: {self.select_pins},"
            f"\n\t\tEnable Pins: {self.enable_pins},"
            f"\n\t\tInverted Enable Pins: {self.inv_enable_pins}"
        )

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the MUX.
        This method should be implemented to define the behavior of the MUX.
        """
        # TODO: Implement the internal function of the MUX

class Demux(ChipFunction):
    """
    Represents an demultiplexer in a digital circuit.
    Attributes:
        address_pins (list[Pin]): A tuple containing the address pins.
        output_pins (list[Pin]): A tuple containing the output pins.
        enable_pins (list[Pin]): A tuple containing the active HIGH enable pins.
        inv_enable_pins (list[Pin]): A tuple containing the active LOW enable pins.
    Methods:
        __str__(): Returns a string representation of the DEMUX.
        chip_internal_function(): Placeholder for the internal function of the DEMUX.
    """

    def __init__(
        self,
        address_pins: list[Pin],
        output_pins: list[Pin],
        enable_pins: list[Pin],
        inv_enable_pins: list[Pin],
    ):
        """
        Initializes a DEMUX with the specified input and output pins.
        Args:
            address_pins (list[Pin]): A tuple containing the address pins.
            output_pins (list[Pin]): A tuple containing the output pins.
            enable_pins (list[Pin]): A tuple containing the active HIGH enable pins.
            inv_enable_pins (list[Pin]): A tuple containing the active LOW enable pins.
        Raises:

        """
        self.address_pins = address_pins
        self.output_pins = output_pins
        self.enable_pins = enable_pins
        self.inv_enable_pins = inv_enable_pins
        if len(self.output_pins) < 2:
            raise ValueError("DEMUX must have at least two input pins.")
        if len(self.address_pins) < 1:
            raise ValueError("DEMUX must have at least one address pin.")
        if len(self.address_pins) != log2(len(self.output_pins)):
            raise ValueError("DEMUX must have log2(num output_pins) address pins.")

    def __str__(self):
        """
        Returns a string representation of the DEMUX.
        Returns:
            str: A string describing the DEMUX with its input and output pins.
        """
        return (
            f"DEMUX:\n\t\tAddress Pins: {self.address_pins},"
            f"\n\t\tOutput Pins: {self.output_pins},"
            f"\n\t\tEnable Pins: {self.enable_pins},"
            f"\n\t\tInverted Enable Pins: {self.inv_enable_pins}"
        )

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the DEMUX.
        This method should be implemented to define the behavior of the DEMUX.
        """
        # TODO: Implement the internal function of the DEMUX

class DFlipFlop(ChipFunction):
    """
    Represents an D flip flop in a digital circuit.
    Attributes:

    Methods:
        __str__(): Returns a string representation of the D flip flop.
        chip_internal_function(): Placeholder for the internal function of the D flip flop.
    """

    def __init__(
        self,
        clock_pin: Pin,
        clock_type: str,
        reset_pin: Pin,
        inv_reset_pin: Pin,
        set_pin: Pin,
        inv_set_pin: Pin,
        data_pin: Pin,
        output_pin: Pin,
        inv_output_pin: Pin
    ):
        """
        Initializes a D Flip Flop with the specified input and output pins.
        Args:
            clock_pin (Pin): The clock pin.
            clock_type (str): The type of the clock signal (e.g., rising, falling, etc.).
            reset_pin (Pin): The reset pin.
            inv_reset_pin (Pin): The inverted reset pin (Active LOW).
            set_pin (Pin): The set pin.
            inv_set_pin (Pin): The inverted set pin (Active LOW).
            data_pin (Pin): The data pin.
            output_pin (Pin): The output pin.
            inv_output_pin (Pin): The inverted output pin (Active LOW).
        Raises:
            ValueError: If the D Flip Flop does not have either set or inverted set pin.
            ValueError: If the D Flip Flop has both set and inverted set pins.
            ValueError: If the D Flip Flop does not have either reset or inverted reset pin.
            ValueError: If the D Flip Flop has both reset and inverted reset pins.
        """
        self.clock_pin = clock_pin
        self.clock_type = clock_type
        self.reset_pin = reset_pin
        self.inv_reset_pin = inv_reset_pin
        self.set_pin = set_pin
        self.inv_set_pin = inv_set_pin
        self.data_pin = data_pin
        self.output_pin = output_pin
        self.inv_output_pin = inv_output_pin

        if self.clock_type not in ["RISING_EDGE", "FALLING_EDGE"]:
            raise ValueError("Clock type must be either RISING_EDGE or FALLING_EDGE.")

        if self.inv_set_pin is None and self.set_pin is None:
            raise ValueError("D Flip Flop must have either set or inverted set pin.")
        if self.inv_set_pin is not None and self.set_pin is not None:
            raise ValueError("D Flip Flop cannot have both set and inverted set pins.")
        if self.inv_reset_pin is None and self.reset_pin is None:
            raise ValueError("D Flip Flop must have either reset or inverted reset pin.")
        if self.inv_reset_pin is not None and self.reset_pin is not None:
            raise ValueError("D Flip Flop cannot have both reset and inverted reset pins.")

    def __str__(self):
        """
        Returns a string representation of the D flip flop.
        Returns:
            str: A string describing the D flip flop with its input and output pins.
        """
        return (
            f"D Flip Flop:\n\t\tClock Pin: {self.clock_pin},"
            f"\n\t\tClock Type: {self.clock_type},"
            f"\n\t\tReset Pin: {self.reset_pin},"
            f"\n\t\tInverted Reset Pin: {self.inv_reset_pin},"
            f"\n\t\tSet Pin: {self.set_pin},"
            f"\n\t\tInverted Set Pin: {self.inv_set_pin},"
            f"\n\t\tData Pin: {self.data_pin},"
            f"\n\t\tOutput Pin: {self.output_pin},"
            f"\n\t\tInverted Output Pin: {self.inv_output_pin}"
        )

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the D Flip Flop.
        This method should be implemented to define the behavior of the D Flip Flop.
        """
        # TODO: Implement the internal function of the D Flip Flop

class JKFlipFlop(ChipFunction):
    """
    Represents a JK Flip Flop in a digital circuit.
    Attributes:

    Methods:
        __str__(): Returns a string representation of the JK Flip Flop.
        chip_internal_function(): Placeholder for the internal function of the JK Flip Flop.
    """

    def __init__(
        self,
        clock_pin: Pin,
        clock_type: str,
        reset_pin: Pin,
        inv_reset_pin: Pin,
        set_pin: Pin,
        inv_set_pin: Pin,
        j_input_pin: Pin,
        inv_j_input_pin: Pin,
        k_input_pin: Pin,
        inv_k_input_pin: Pin,
        output_pin: Pin,
        inv_output_pin: Pin
    ):
        """
        Initializes a JK Flip Flop with the specified input and output pins.
        Args:
            clock_pin (Pin): The clock pin.
            clock_type (str): The type of the clock signal (e.g., rising, falling, etc.).
            reset_pin (Pin): The reset pin.
            inv_reset_pin (Pin): The inverted reset pin (Active LOW).
            set_pin (Pin): The set pin.
            inv_set_pin (Pin): The inverted set pin (Active LOW).
            j_input_pin (Pin): The J input pin.
            inv_j_input_pin (Pin): The inverted J input pin (Active LOW).
            k_input_pin (Pin): The K input pin.
            inv_k_input_pin (Pin): The inverted K input pin (Active LOW).
            output_pin (Pin): The output pin.
            inv_output_pin (Pin): The inverted output pin (Active LOW).
        Raises:
            ValueError: If the JK Flip Flop does not have either J or inverted J input pin.
            ValueError: If the JK Flip Flop has both J and inverted J input pins.
            ValueError: If the JK Flip Flop does not have either K or inverted K input pin.
            ValueError: If the JK Flip Flop has both K and inverted K input pins.
            ValueError: If the JK Flip Flop does not have either set or inverted set pin.
            ValueError: If the JK Flip Flop has both set and inverted set pins.
            ValueError: If the JK Flip Flop does not have either reset or inverted reset pin.
            ValueError: If the JK Flip Flop has both reset and inverted reset pins.
        """
        self.clock_pin = clock_pin
        self.clock_type = clock_type
        self.reset_pin = reset_pin
        self.inv_reset_pin = inv_reset_pin
        self.set_pin = set_pin
        self.inv_set_pin = inv_set_pin
        self.j_input_pin = j_input_pin
        self.inv_j_input_pin = inv_j_input_pin
        self.k_input_pin = k_input_pin
        self.inv_k_input_pin = inv_k_input_pin
        self.output_pin = output_pin
        self.inv_output_pin = inv_output_pin

        if self.clock_type not in ["RISING_EDGE", "FALLING_EDGE"]:
            raise ValueError("Clock type must be either RISING_EDGE or FALLING_EDGE.")
        if self.j_input_pin is None and self.inv_j_input_pin is None:
            raise ValueError("JK Flip Flop must have either J or inverted J input pin.")
        if self.j_input_pin is not None and self.inv_j_input_pin is not None:
            raise ValueError("JK Flip Flop cannot have both J and inverted J input pins.")
        if self.k_input_pin is None and self.inv_k_input_pin is None:
            raise ValueError("JK Flip Flop must have either K or inverted K input pin.")
        if self.k_input_pin is not None and self.inv_k_input_pin is not None:
            raise ValueError("JK Flip Flop cannot have both K and inverted K input pins.")
        if self.inv_set_pin is None and self.set_pin is None:
            raise ValueError("JK Flip Flop must have either set or inverted set pin.")
        if self.inv_set_pin is not None and self.set_pin is not None:
            raise ValueError("JK Flip Flop cannot have both set and inverted set pins.")
        if self.inv_reset_pin is None and self.reset_pin is None:
            raise ValueError("JK Flip Flop must have either reset or inverted reset pin.")
        if self.inv_reset_pin is not None and self.reset_pin is not None:
            raise ValueError("JK Flip Flop cannot have both reset and inverted reset pins.")

    def __str__(self):
        """
        Returns a string representation of the JK Flip Flop.
        Returns:
            str: A string describing the JK Flip Flop with its input and output pins.
        """
        return (
            f"JK Flip Flop:\n\t\tClock Pin: {self.clock_pin},"
            f"\n\t\tClock Type: {self.clock_type},"
            f"\n\t\tReset Pin: {self.reset_pin},"
            f"\n\t\tInverted Reset Pin: {self.inv_reset_pin},"
            f"\n\t\tSet Pin: {self.set_pin},"
            f"\n\t\tInverted Set Pin: {self.inv_set_pin},"
            f"\n\t\tJ Input Pin: {self.j_input_pin},"
            f"\n\t\tInverted J Input Pin: {self.inv_j_input_pin},"
            f"\n\t\tK Input Pin: {self.k_input_pin},"
            f"\n\t\tInverted K Input Pin: {self.inv_k_input_pin},"
            f"\n\t\tOutput Pin: {self.output_pin},"
            f"\n\t\tInverted Output Pin: {self.inv_output_pin}"
        )

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the JK Flip Flop.
        This method should be implemented to define the behavior of the JK Flip Flop.
        """
        # TODO: Implement the internal function of the JK Flip Flop

class BinaryCounter(ChipFunction):
    """
    Represents a binary counter in a digital circuit.
    Attributes:

    Methods:
        __str__(): Returns a string representation of the binary counter.
        chip_internal_function(): Placeholder for the internal function of the binary counter.
    """

    def __init__(
        self,
        clock_pin: Pin,
        clock_type: str,
        synch_reset_pin: Pin,
        inv_synch_reset_pin: Pin,
        count_enable_parallel_pin: Pin,
        inv_count_enable_parallel_pin: Pin,
        count_enable_trickle_pin: Pin,
        inv_count_enable_trickle_pin: Pin,
        load_enable_pin: Pin,
        inv_load_enable_pin: Pin,
        up_down_input_pin: Pin,
        terminal_count_pin: Pin,
        ripple_clock_output_pin: Pin,
        data_pins: list[Pin],
        output_pins: list[Pin],
    ):
        """
        Initializes a binary counter with the specified input and output pins.
        Args:
            clock_pin (Pin): The clock pin.
            clock_type (str): The type of the clock signal (e.g., rising, falling, etc.).
            synch_reset_pin (Pin): The synchronous reset pin.
            inv_synch_reset_pin (Pin): The inverted synchronous reset pin (Active LOW).
            count_enable_parallel_pin (Pin): The count enable pin.
            inv_count_enable_parallel_pin (Pin): The inverted count enable pin (Active LOW).
            count_enable_trickle_pin (Pin): The count enable trickle pin.
            inv_count_enable_trickle_pin (Pin): The inverted count enable trickle pin (Active LOW).
            load_enable_pin (Pin): The load enable pin.
            inv_load_enable_pin (Pin): The inverted load enable pin (Active LOW).
            up_down_input_pin (Pin): The up/down input pin.
            terminal_count_pin (Pin): The terminal count pin.
            ripple_clock_output_pin (Pin): The ripple clock output pin.
            data_pins (list[Pin]): A tuple containing the data pins.
            output_pins (list[Pin]): A tuple containing the output pins.
        Raises:
            ValueError: If the clock type is not RISING_EDGE or FALLING_EDGE.
            ValueError: If the number of data pins is not equal to the number of output pins.
        """
        self.clock_pin = clock_pin
        self.clock_type = clock_type
        self.synch_reset_pin = synch_reset_pin
        self.inv_synch_reset_pin = inv_synch_reset_pin
        self.count_enable_parallel_pin = count_enable_parallel_pin
        self.inv_count_enable_parallel_pin = inv_count_enable_parallel_pin
        self.count_enable_trickle_pin = count_enable_trickle_pin
        self.inv_count_enable_trickle_pin = inv_count_enable_trickle_pin
        self.load_enable_pin = load_enable_pin
        self.inv_load_enable_pin = inv_load_enable_pin
        self.up_down_input_pin = up_down_input_pin
        self.terminal_count_pin = terminal_count_pin
        self.ripple_clock_output_pin = ripple_clock_output_pin
        self.data_pins = data_pins
        self.output_pins = output_pins

        if self.clock_type not in ["RISING_EDGE", "FALLING_EDGE"]:
            raise ValueError("Clock type must be either RISING_EDGE or FALLING_EDGE.")
        if len(self.data_pins) != len(self.output_pins):
            raise ValueError("Number of data pins must be equal to number of output pins.")

    def __str__(self):
        """
        Returns a string representation of the binary counter.
        Returns:
            str: A string describing the binary counter with its input and output pins.
        """
        return (
            f"Binary Counter:\n\t\tClock Pin: {self.clock_pin},"
            f"\n\t\tClock Type: {self.clock_type},"
            f"\n\t\tSynchronous Reset Pin: {self.synch_reset_pin},"
            f"\n\t\tInverted Synchronous Reset Pin: {self.inv_synch_reset_pin},"
            f"\n\t\tCount Enable Parallel Pin: {self.count_enable_parallel_pin},"
            f"\n\t\tInverted Count Enable Parallel Pin: {self.inv_count_enable_parallel_pin},"
            f"\n\t\tCount Enable Trickle Pin: {self.count_enable_trickle_pin},"
            f"\n\t\tInverted Count Enable Trickle Pin: {self.inv_count_enable_trickle_pin},"
            f"\n\t\tLoad Enable Pin: {self.load_enable_pin},"
            f"\n\t\tInverted Load Enable Pin: {self.inv_load_enable_pin},"
            f"\n\t\tUp/Down Input Pin: {self.up_down_input_pin},"
            f"\n\t\tTerminal Count Pin: {self.terminal_count_pin},"
            f"\n\t\tRipple Clock Output Pin: {self.ripple_clock_output_pin},"
            f"\n\t\tData Pins: {self.data_pins},"
            f"\n\t\tOutput Pins: {self.output_pins}"
        )

    def chip_internal_function(self):
        """
        Placeholder for the internal function of the binary counter.
        This method should be implemented to define the behavior of the binary counter.
        """
        # TODO: Implement the internal function of the binary counter

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
            elif func_type == "MUX":
                functions.append(
                    Mux(
                        func_data["input_pins"],
                        func_data["output_pins"],
                        func_data["inv_output_pins"],
                        func_data["select_pins"],
                        func_data["enable_pins"],
                        func_data["inv_enable_pins"],
                    )
                )
            elif func_type == "DEMUX":
                functions.append(
                    Demux(
                        func_data["address_pins"],
                        func_data["output_pins"],
                        func_data["enable_pins"],
                        func_data["inv_enable_pins"],
                    )
                )
            elif func_type == "D_FLIP_FLOP":
                functions.append(
                    DFlipFlop(
                        func_data["clock_pin"],
                        func_data["clock_type"],
                        func_data["reset_pin"],
                        func_data["inv_reset_pin"],
                        func_data["set_pin"],
                        func_data["inv_set_pin"],
                        func_data["data_pin"],
                        func_data["output_pin"],
                        func_data["inv_output_pin"],
                    )
                )
            elif func_type == "JK_FLIP_FLOP":
                functions.append(
                    JKFlipFlop(
                        func_data["clock_pin"],
                        func_data["clock_type"],
                        func_data["reset_pin"],
                        func_data["inv_reset_pin"],
                        func_data["set_pin"],
                        func_data["inv_set_pin"],
                        func_data["j_input_pin"],
                        func_data["inv_j_input_pin"],
                        func_data["k_input_pin"],
                        func_data["inv_k_input_pin"],
                        func_data["output_pin"],
                        func_data["inv_output_pin"],
                    )
                )
            elif func_type == "BINARY_COUNTER":
                functions.append(
                    BinaryCounter(
                        func_data["clock_pin"],
                        func_data["clock_type"],
                        func_data["synch_reset_pin"],
                        func_data["inv_synch_reset_pin"],
                        func_data["count_enable_parallel_pin"],
                        func_data["inv_count_enable_parallel_pin"],
                        func_data["count_enable_trickle_pin"],
                        func_data["inv_count_enable_trickle_pin"],
                        func_data["load_enable_pin"],
                        func_data["inv_load_enable_pin"],
                        func_data["up_down_input_pin"],
                        func_data["terminal_count_pin"],
                        func_data["ripple_clock_output_pin"],
                        func_data["data_pins"],
                        func_data["output_pins"],
                    )
                )
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
