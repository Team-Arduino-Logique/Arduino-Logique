"""
This module defines classes for representing connection points and pins in a circuit model.
Classes:
    ConnectionPointID: Represents an identifier for a connection point in a circuit model.
    ConnectionPoint: Represents a connection point in a circuit.
    Pin: Represents a pin on an electronic component.

"""

from __future__ import annotations
from dataclasses import dataclass


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
    connection_point: ConnectionPoint | None
