"""
This module defines classes for representing connection points and pins in a circuit model.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ConnectionPointID:
    """
    Represents an identifier for a connection point in a circuit model.
    Attributes:
        col (int): The column of the connection point.
        line (int): The line of the connection point.
    """

    col: int
    line: int


@dataclass
class Pin:
    """
    Represents a pin on an electronic component.
    Attributes:
        pin_num (int): The pin number.
        connection_point (ConnectionPointID): The connection point of the pin.
    """

    pin_num: int
    connection_point: ConnectionPointID | None


@dataclass
class TruthTableRow:
    """
    A row for a truth table, with input and output signals.

    Allowed values are:
    - "H" for high
    - "L" for low
    - "X" for undefined
    - "R" for rising edge
    - "F" for falling edge
    - "Q" for reference to the previous state of the output
    - "nQ" for reference to the previous state of the output, negated
    - "lP" for LOW level pulse
    - "hP" for HIGH level pulse
    - "tL" for transition to LOW on clock pulse
    - "tH" for transition to HIGH on clock pulse

    """
    input_signals: list[str]
    output_signals: list[str]

    ALLOWED_SIGNALS = ["H", "L", "X", "R", "F", "Q", "nQ"]

    def __post_init__(self):
        for signal in self.input_signals + self.output_signals:
            if signal not in self.ALLOWED_SIGNALS:
                raise ValueError(f"Invalid signal: {signal}. Allowed signals are {self.ALLOWED_SIGNALS}.")

@dataclass
class TruthTable:
    """
    Represents a truth table. Made of lists of lists; every row is a state.

    E.g. for a 2-input, 1-output truth table (xor):
    [
        [["L", "L"], ["L"]],
        [["L", "H"], ["H"]],
        [["H", "L"], ["H"]],
        [["H", "H"], ["L"]],
    ]
    """
    rows: list[TruthTableRow]

@dataclass
class FunctionRepresentation:
    """
    Represents a function in a circuit model.
    Attributes:
        fn_inputs (list[ConnectionPointID]): The input connection points of the function.
        fn_outputs (list[ConnectionPointID]): The output connection points of the function.
        function (TruthTable | str): The function represented as a truth table or a string.
    """
    fn_inputs: list[ConnectionPointID]
    fn_outputs: list[ConnectionPointID]
    function: TruthTable | str
