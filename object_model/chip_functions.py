"""
This module provides functions to create various digital logic gates and flip-flops,
as well as a base class for chip functions. The module includes classes for AND, OR,
NOT, XOR, NAND, NOR, XNOR gates, multiplexers (MUX), demultiplexers (DEMUX), D flip-flops,
and JK flip-flops. Each class represents a specific type of digital logic component
and includes methods for initialization, string representation, and a placeholder
for the internal function of the chip.
Functions:
    create_and_gate(data: dict) -> AndGate:
    create_or_gate(data: dict) -> OrGate:
    create_not_gate(data: dict) -> NotGate:
    create_xor_gate(data: dict) -> XorGate:
    create_nand_gate(data: dict) -> NandGate:
    create_nor_gate(data: dict) -> NorGate:
    create_xnor_gate(data: dict) -> XnorGate:
    create_mux(data: dict) -> Mux:
    create_demux(data: dict) -> Demux:
    create_d_flip_flop(data: dict) -> DFlipFlop:
    create_jk_flip_flop(data: dict) -> JKFlipFlop:
    create_binary_counter(data: dict) -> BinaryCounter:
Classes:
    ChipFunction:
    AndGate(ChipFunction):
    OrGate(ChipFunction):
    NotGate(ChipFunction):
    XorGate(ChipFunction):
    NandGate(ChipFunction):
    NorGate(ChipFunction):
    XnorGate(ChipFunction):
    Mux(ChipFunction):
    Demux(ChipFunction):
        Represents a demultiplexer in a digital circuit.
    DFlipFlop(ChipFunction):
        Represents a D flip-flop in a digital circuit.
    JKFlipFlop(ChipFunction):
        Represents a JK flip-flop in a digital circuit.
    BinaryCounter(ChipFunction):

"""

from __future__ import annotations
from math import log2
from object_model.circuit_util_elements import Pin


def create_and_gate(data: dict) -> AndGate:
    """
    Creates an AndGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the AND gate.
    Returns:
        AndGate: An AndGate object initialized with the provided pins.
    """
    return AndGate(data["input_pins"], data["output_pins"])


def create_or_gate(data: dict) -> OrGate:
    """
    Creates an OrGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the OR gate.
    Returns:
        OrGate: An OrGate object initialized with the provided pins.
    """
    return OrGate(data["input_pins"], data["output_pins"])


def create_not_gate(data: dict) -> NotGate:
    """
    Creates a NotGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the NOT gate.
    Returns:
        NotGate: A NotGate object initialized with the provided pins.
    """
    return NotGate(data["input_pins"], data["output_pins"])


def create_xor_gate(data: dict) -> XorGate:
    """
    Creates an XorGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the XOR gate.
    Returns:
        XorGate: An XorGate object initialized with the provided pins.
    """
    return XorGate(data["input_pins"], data["output_pins"])


def create_nand_gate(data: dict) -> NandGate:
    """
    Creates a NandGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the NAND gate.
    Returns:
        NandGate: A NandGate object initialized with the provided pins.
    """
    return NandGate(data["input_pins"], data["output_pins"])


def create_nor_gate(data: dict) -> NorGate:
    """
    Creates a NorGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the NOR gate.
    Returns:
        NorGate: A NorGate object initialized with the provided pins.
    """
    return NorGate(data["input_pins"], data["output_pins"])


def create_xnor_gate(data: dict) -> XnorGate:
    """
    Creates an XnorGate object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input and output pins for the XNOR gate.
    Returns:
        XnorGate: An XnorGate object initialized with the provided pins.
    """
    return XnorGate(data["input_pins"], data["output_pins"])


def create_mux(data: dict) -> Mux:
    """
    Creates a Mux object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the input, output,
        inverted output, select, enable, and inverted enable pins for the MUX.
    Returns:
        Mux: A Mux object initialized with the provided pins.
    """
    return Mux(
        data["input_pins"],
        data["output_pins"],
        data["inv_output_pins"],
        data["select_pins"],
        data["enable_pins"],
        data["inv_enable_pins"],
    )


def create_demux(data: dict) -> Demux:
    """
    Creates a Demux object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the address, output, enable, and inverted enable pins for the DEMUX.
    Returns:
        Demux: A Demux object initialized with the provided pins.
    """
    return Demux(
        data["address_pins"],
        data["output_pins"],
        data["enable_pins"],
        data["inv_enable_pins"],
    )


def create_d_flip_flop(data: dict) -> DFlipFlop:
    """
    Creates a DFlipFlop object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the clock, reset,
        set, data, output, and inverted output pins for the D Flip Flop.
    Returns:
        DFlipFlop: A DFlipFlop object initialized with the provided pins.
    """
    return DFlipFlop(
        data["clock_pin"],
        data["clock_type"],
        data["reset_pin"],
        data["inv_reset_pin"],
        data["set_pin"],
        data["inv_set_pin"],
        data["data_pin"],
        data["output_pin"],
        data["inv_output_pin"],
    )


def create_jk_flip_flop(data: dict) -> JKFlipFlop:
    """
    Creates a JKFlipFlop object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the clock, reset, set,
        J input, K input, output, and inverted output pins for the JK Flip Flop.
    Returns:
        JKFlipFlop: A JKFlipFlop object initialized with the provided pins.
    """
    return JKFlipFlop(
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
    )


def create_binary_counter(data: dict) -> BinaryCounter:
    """
    Creates a BinaryCounter object from the provided data dictionary.
    Args:
        data (dict): A dictionary containing the clock, reset, enable,
        load, up/down, terminal count, ripple clock, data, and output
        pins for the binary counter.
    Returns:
        BinaryCounter: A BinaryCounter object initialized with the provided pins.
    """
    return BinaryCounter(
        data["clock_pin"],
        data["clock_type"],
        data["synch_reset_pin"],
        data["inv_synch_reset_pin"],
        data["count_enable_parallel_pin"],
        data["inv_count_enable_parallel_pin"],
        data["count_enable_trickle_pin"],
        data["inv_count_enable_trickle_pin"],
        data["load_enable_pin"],
        data["inv_load_enable_pin"],
        data["up_down_input_pin"],
        data["terminal_count_pin"],
        data["ripple_clock_output_pin"],
        data["data_pins"],
        data["output_pins"],
    )


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
        inv_output_pin: Pin,
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
        inv_output_pin: Pin,
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
