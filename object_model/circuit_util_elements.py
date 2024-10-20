"""
This module defines classes for representing connection points and pins in a circuit model.
Classes:
    ConnectionPointID: Represents an identifier for a connection point in a circuit model.
    Pin: Represents a pin on an electronic component.
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
class TruthTable:
    #TODO
    pass

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
