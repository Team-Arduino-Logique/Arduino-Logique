"""
This module provides functions to create various digital logic gates and flip-flops,
as well as a base class for chip functions. The module includes classes for AND, OR,
NOT, XOR, NAND, NOR, XNOR gates, multiplexers (MUX), demultiplexers (DEMUX), D flip-flops,
and JK flip-flops. Each class represents a specific type of digital logic component
and includes methods for initialization, string representation, and a placeholder
for the internal function of the chip.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from math import log2
from .circuit_util_elements import ConnectionPointID, FunctionRepresentation, Pin, TruthTable, TruthTableRow


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


class ChipFunction(ABC):
    """
    A base class representing a generic chip function.

    This class serves as a template for specific chip functions.
    It contains a method that should be overridden by subclasses to
    implement the specific internal function of the chip to link inputs and outputs.
    """

    def __init__(self) -> None:
        """
        Initializes a ChipFunction object.
        """
        self.all_pins: list[Pin] = []

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Function not implemented.")

    @abstractmethod
    def chip_internal_function(self) -> FunctionRepresentation:
        """
        Represents an internal function of a chip.
        This method is intended to be overridden by subclasses to provide
        specific functionality for different types of chips. It should return
        an instance of `FunctionRepresentation` that encapsulates the behavior
        of the chip's internal function.
        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        Returns:
            FunctionRepresentation: An object representing the chip's internal function.
        """

        raise NotImplementedError("Function not implemented.")

    def calculate_pin_pos(self, top_left_pin_pos: ConnectionPointID, top_left_pin_num: int, num_pins: int) -> None:
        """
        Calculates the position of all pins based on the top-left pin position and the pin number.
        Args:
            top_left_pin_pos (ConnectionPointID): The position of the top-left pin.
            top_left_pin_num (int): The pin number.
            num_pins (int): The total number of pins.
        Returns:
            None
        """
        pins_per_side = num_pins // 2
        if top_left_pin_num == num_pins:
            top_right_pin_num = num_pins - pins_per_side + 1
            for pin in self.all_pins:
                if pin.pin_num <= top_left_pin_num and pin.pin_num >= top_right_pin_num:
                    pin.connection_point = ConnectionPointID(
                        top_left_pin_pos.col + (top_left_pin_num - pin.pin_num), top_left_pin_pos.line
                    )
                else:
                    pin.connection_point = ConnectionPointID(
                        top_left_pin_pos.col + pin.pin_num - 1, top_left_pin_pos.line + 1
                    )

        else:
            raise NotImplementedError("Rotated chips not supported yet")


class LogicalFunction(ChipFunction, ABC):
    """
    Represents a logical function within a chip, inheriting from ChipFunction.
    Attributes:
        input_pins (list[int]): List of input pin numbers.
        output_pins (list[int]): List of output pin numbers.
        operator (str): The logical operator to be applied (e.g., &, |, ^, !).
        all_pins (list[Pin]): Combined list of input and output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int], operator: str):
        """
        Initializes the LogicalFunction with input pins, output pins, and a logical operator.
        Args:
            input_pins (list[int]): List of input pin numbers.
            output_pins (list[int]): List of output pin numbers.
            operator (str): The logical operator to be applied.
        """
        super().__init__()
        self.input_pins: list[Pin] = [Pin(pin_num, None) for pin_num in input_pins]
        self.output_pins: list[Pin] = [Pin(pin_num, None) for pin_num in output_pins]
        self.all_pins = self.input_pins + self.output_pins
        self.operator = operator

    def chip_internal_function(self) -> FunctionRepresentation:
        """
        Generates a FunctionRepresentation object based on the current state of the input and output pins.
        Returns:
            FunctionRepresentation: An object representing the input and output pins and the logical operator.
        """
        input_pin_pos = [pin.connection_point for pin in self.input_pins if pin.connection_point is not None]
        output_pin_pos = [pin.connection_point for pin in self.output_pins if pin.connection_point is not None]
        return FunctionRepresentation(input_pin_pos, output_pin_pos, self.operator)

    @abstractmethod
    def __str__(self):
        raise NotImplementedError("Function not implemented.")


class AndGate(LogicalFunction):
    """
    Represents an AND gate in a digital circuit.
    Attributes:
        input_pins (list[Pin]): A tuple containing the input pins.
        output_pins (list[Pin]): A tuple containing the output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes an AND gate with the specified input and output pins.
        Args:
            input_pins (list[Pin]): A tuple containing the input pins.
            output_pins (list[Pin]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "&")
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


class OrGate(LogicalFunction):
    """
    Represents an OR gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the indices of the input pins.
        output_pins (list[int]): A tuple containing the index of the output pin.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes an OR gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pin numbers.
            output_pins (list[int]): A tuple containing the output pin number.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """

        super().__init__(input_pins, output_pins, "|")
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


class NotGate(LogicalFunction):
    """
    Represents a NOT gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pin number(s).
        output_pins (list[int]): A tuple containing the output pin number(s).
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes a NOT gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pin number(s).
            output_pins (list[int]): A tuple containing the output pin number(s).
        Raises:
            ValueError: If the number of input pins is not exactly one.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "!")

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


class XorGate(LogicalFunction):
    """
    Represents an XOR gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pins.
        output_pins (list[int]): A tuple containing the output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes an XOR gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pins.
            output_pins (list[int]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "^")

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


class NandGate(LogicalFunction):
    """
    Represents a NAND gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pins.
        output_pins (list[int]): A tuple containing the output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes a NAND gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pins.
            output_pins (list[int]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "!&")

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


class NorGate(LogicalFunction):
    """
    Represents a NOR gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pins.
        output_pins (list[int]): A tuple containing the output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes a NOR gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pins.
            output_pins (list[int]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "!|")

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


class XnorGate(LogicalFunction):
    """
    Represents an XNOR gate in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pins.
        output_pins (list[int]): A tuple containing the output pins.
    """

    def __init__(self, input_pins: list[int], output_pins: list[int]):
        """
        Initializes an XNOR gate with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pins.
            output_pins (list[int]): A tuple containing the output pin.
        Raises:
            ValueError: If the number of input pins is less than two.
            ValueError: If the number of output pins is not exactly one.
        """
        super().__init__(input_pins, output_pins, "!^")

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


class Mux(ChipFunction):
    """
    Represents a multiplexer in a digital circuit.
    Attributes:
        input_pins (list[int]): A tuple containing the input pins.
        output_pins (list[int]): A tuple containing the output pins.
        inv_output_pins (list[int]): A tuple containing the inverted output pins.
        select_pins (list[int]): A tuple containing the select pins.
        enable_pins (list[int]): A tuple containing the active HIGH enable pins.
        inv_enable_pins (list[int]): A tuple containing the active LOW enable pins.
    """

    def __init__(
        self,
        input_pins: list[int],
        output_pins: list[int],
        inv_output_pins: list[int],
        select_pins: list[int],
        enable_pins: list[int],
        inv_enable_pins: list[int],
    ):
        """
        Initializes a Mux with the specified input and output pins.
        Args:
            input_pins (list[int]): A tuple containing the input pins.
            output_pins (list[int]): A tuple containing the output pins.
            inv_output_pins (list[int]): A tuple containing the inverted output pins.
            select_pins (list[int]): A tuple containing the select pins.
            enable_pins (list[int]): A tuple containing the active HIGH enable pins.
            inv_enable_pins (list[int]): A tuple containing the active LOW enable pins.
        Raises:

        """
        super().__init__()
        self.input_pins: list[Pin] = [Pin(pin_num, None) for pin_num in input_pins]
        self.output_pins: list[Pin] = [Pin(pin_num, None) for pin_num in output_pins]
        self.inv_output_pins: list[Pin] = [Pin(pin_num, None) for pin_num in inv_output_pins]
        self.select_pins: list[Pin] = [Pin(pin_num, None) for pin_num in select_pins]
        self.enable_pins: list[Pin] = [Pin(pin_num, None) for pin_num in enable_pins]
        self.inv_enable_pins: list[Pin] = [Pin(pin_num, None) for pin_num in inv_enable_pins]
        self.all_pins = (
            self.input_pins
            + self.output_pins
            + self.inv_output_pins
            + self.select_pins
            + self.enable_pins
            + self.inv_enable_pins
        )
        if len(self.input_pins) < 2:
            raise ValueError("MUX must have at least two input pins.")
        if len(self.output_pins) < 1 or len(self.inv_output_pins) < 1:
            raise ValueError("MUX must have at least one output pin or inverted output pin.")
        if len(self.select_pins) != log2(len(self.input_pins)):
            raise ValueError("MUX must have log2(num input pins) select pins.")

        if len(self.enable_pins) > 0 or len(self.select_pins) != 3 or len(self.input_pins) != 8:
            raise ValueError("Arbitrary MUX size not supported yet")

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

    def chip_internal_function(self) -> FunctionRepresentation:
        """
        Returns a FunctionRepresentation object representing the internal function of the MUX with a truth table.
        Only works for 8-input, 1-output MUX, with 3 select pins, with an active LOW enable pin.
        """

        input_pin_pos = [
            pin.connection_point
            for pin in self.enable_pins + self.inv_enable_pins + self.select_pins[::-1] + self.input_pins
            if pin.connection_point is not None
        ]
        output_pin_pos = [
            pin.connection_point for pin in self.inv_output_pins + self.output_pins if pin.connection_point is not None
        ]

        truth_table = TruthTable(
            [
                TruthTableRow(["H", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "L", "L", "L", "L", "X", "X", "X", "X", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "L", "L", "L", "H", "X", "X", "X", "X", "X", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "L", "L", "H", "X", "L", "X", "X", "X", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "L", "L", "H", "X", "H", "X", "X", "X", "X", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "L", "H", "L", "X", "X", "L", "X", "X", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "L", "H", "L", "X", "X", "H", "X", "X", "X", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "L", "H", "H", "X", "X", "X", "L", "X", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "L", "H", "H", "X", "X", "X", "H", "X", "X", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "H", "L", "L", "X", "X", "X", "X", "L", "X", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "H", "L", "L", "X", "X", "X", "X", "H", "X", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "H", "L", "H", "X", "X", "X", "X", "X", "L", "X", "X"], ["H", "L"]),
                TruthTableRow(["L", "H", "L", "H", "X", "X", "X", "X", "X", "H", "X", "X"], ["L", "H"]),
                TruthTableRow(["L", "H", "H", "L", "X", "X", "X", "X", "X", "X", "L", "X"], ["H", "L"]),
                TruthTableRow(["L", "H", "H", "L", "X", "X", "X", "X", "X", "X", "H", "X"], ["L", "H"]),
                TruthTableRow(["L", "H", "H", "H", "X", "X", "X", "X", "X", "X", "X", "L"], ["H", "L"]),
                TruthTableRow(["L", "H", "H", "H", "X", "X", "X", "X", "X", "X", "X", "H"], ["L", "H"]),
            ]
        )

        return FunctionRepresentation(input_pin_pos, output_pin_pos, truth_table)


class Demux(ChipFunction):
    """
    Represents an demultiplexer in a digital circuit.
    Attributes:
        address_pins (list[int]): A tuple containing the address pins.
        output_pins (list[int]): A tuple containing the output pins.
        enable_pins (list[int]): A tuple containing the active HIGH enable pins.
        inv_enable_pins (list[int]): A tuple containing the active LOW enable pins.
    """

    def __init__(
        self,
        address_pins: list[int],
        output_pins: list[int],
        enable_pins: list[int],
        inv_enable_pins: list[int],
    ):
        """
        Initializes a DEMUX with the specified input and output pins.
        Args:
            address_pins (list[int]): A tuple containing the address pins.
            output_pins (list[int]): A tuple containing the output pins.
            enable_pins (list[int]): A tuple containing the active HIGH enable pins.
            inv_enable_pins (list[int]): A tuple containing the active LOW enable pins.
        Raises:
            ValueError: If the number of output pins is less than two.
            ValueError: If the number of address pins is not exactly one.
            ValueError: If the number of address pins is not equal to log2(num output pins).
        """
        super().__init__()
        self.address_pins: list[Pin] = [Pin(pin_num, None) for pin_num in address_pins]
        self.output_pins: list[Pin] = [Pin(pin_num, None) for pin_num in output_pins]
        self.enable_pins: list[Pin] = [Pin(pin_num, None) for pin_num in enable_pins]
        self.inv_enable_pins: list[Pin] = [Pin(pin_num, None) for pin_num in inv_enable_pins]

        self.all_pins = self.address_pins + self.output_pins + self.enable_pins + self.inv_enable_pins

        if len(self.output_pins) < 2:
            raise ValueError("DEMUX must have at least two input pins.")
        if len(self.address_pins) < 1:
            raise ValueError("DEMUX must have at least one address pin.")
        if len(self.address_pins) != log2(len(self.output_pins)):
            raise ValueError("DEMUX must have log2(num output_pins) address pins.")

        if (
            len(self.enable_pins) != 1
            or len(self.inv_enable_pins) != 2
            or len(self.output_pins) != 8
            or len(self.address_pins) != 3
        ):
            raise ValueError("Arbitrary DEMUX size not supported yet")

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
        Returns a FunctionRepresentation object representing the internal function of the MUX with a truth table.
        Only works for 2-active-low-enable, 1- active-high-enable, 3-address-pin, 8-output-pin DEMUX.
        """
        input_pin_pos = [
            pin.connection_point
            for pin in self.inv_enable_pins + self.enable_pins + self.address_pins
            if pin.connection_point is not None
        ]
        output_pin_pos = [pin.connection_point for pin in self.output_pins if pin.connection_point is not None]

        truth_table = TruthTable(
            [
                TruthTableRow(["H", "X", "X", "X", "X", "X"], ["L", "L", "L", "L", "L", "L", "L", "L"]),
                TruthTableRow(["X", "H", "X", "X", "X", "X"], ["L", "L", "L", "L", "L", "L", "L", "L"]),
                TruthTableRow(["X", "X", "L", "X", "X", "X"], ["L", "L", "L", "L", "L", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "L", "L", "L"], ["H", "L", "L", "L", "L", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "H", "L", "L"], ["L", "H", "L", "L", "L", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "L", "H", "L"], ["L", "L", "H", "L", "L", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "H", "H", "L"], ["L", "L", "L", "H", "L", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "L", "L", "H"], ["L", "L", "L", "L", "H", "L", "L", "L"]),
                TruthTableRow(["L", "L", "H", "H", "L", "H"], ["L", "L", "L", "L", "L", "H", "L", "L"]),
                TruthTableRow(["L", "L", "H", "L", "H", "H"], ["L", "L", "L", "L", "L", "L", "H", "L"]),
                TruthTableRow(["L", "L", "H", "H", "H", "H"], ["L", "L", "L", "L", "L", "L", "L", "H"]),
            ]
        )

        return FunctionRepresentation(input_pin_pos, output_pin_pos, truth_table)


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
        clock_pin: int,
        clock_type: str,
        reset_pin: int,
        inv_reset_pin: int,
        set_pin: int,
        inv_set_pin: int,
        data_pin: int,
        output_pin: int,
        inv_output_pin: int,
    ):
        """
        Initializes a D Flip Flop with the specified input and output pins.
        Args:
            clock_pin (int): The clock pin.
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
        clock_pin: int,
        clock_type: str,
        reset_pin: int,
        inv_reset_pin: int,
        set_pin: int,
        inv_set_pin: int,
        j_input_pin: int,
        inv_j_input_pin: int,
        k_input_pin: int,
        inv_k_input_pin: int,
        output_pin: int,
        inv_output_pin: int,
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
        clock_pin: int,
        clock_type: str,
        synch_reset_pin: int,
        inv_synch_reset_pin: int,
        count_enable_parallel_pin: int,
        inv_count_enable_parallel_pin: int,
        count_enable_trickle_pin: int,
        inv_count_enable_trickle_pin: int,
        load_enable_pin: int,
        inv_load_enable_pin: int,
        up_down_input_pin: int,
        terminal_count_pin: int,
        ripple_clock_output_pin: int,
        data_pins: list[int],
        output_pins: list[int],
    ):
        """
        Initializes a binary counter with the specified input and output pins.
        Args:
            clock_pin (int): The clock pin.
            clock_type (str): The type of the clock signal (e.g., rising, falling, etc.).
            synch_reset_pin (int): The synchronous reset pin.
            inv_synch_reset_pin (int): The inverted synchronous reset pin (Active LOW).
            count_enable_parallel_pin (int): The count enable pin.
            inv_count_enable_parallel_pin (int): The inverted count enable pin (Active LOW).
            count_enable_trickle_pin (int): The count enable trickle pin.
            inv_count_enable_trickle_pin (int): The inverted count enable trickle pin (Active LOW).
            load_enable_pin (int): The load enable pin.
            inv_load_enable_pin (int): The inverted load enable pin (Active LOW).
            up_down_input_pin (int): The up/down input pin.
            terminal_count_pin (int): The terminal count pin.
            ripple_clock_output_pin (int): The ripple clock output pin.
            data_pins (list[int]): A tuple containing the data pins.
            output_pins (list[int]): A tuple containing the output pins.
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
