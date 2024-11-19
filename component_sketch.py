"""
component_sketch.py
This module provides a class `ComponentSketcher` for sketching and manipulating electronic components on 
a Tkinter canvas. It includes methods for drawing various components such as chips, wires, and pins, as 
well as handling events like dragging and clicking.
"""

import tkinter as tk
from tkinter import font
import math
from typing import Any, Callable


from dataCDLT import (
    HORIZONTAL,
    RIGHT,
    VERTICAL,
    VERTICAL_END_HORIZONTAL,
    LEFT,
    PERSO,
    NO,
    AUTO,
    FREE,
    USED,
    INPUT,
    OUTPUT,
)
from component_params import BOARD_830_PTS_PARAMS, DIP14_PARAMS


class ComponentSketcher:
    """
    A class to sketch and manipulate electronic components on a canvas.
    Attributes:
    canvas (tk.Canvas): The canvas on which components are drawn.
    hole_func (dict): A dictionary containing the function to draw holes.
    scale_factor (float): The scaling factor for the components.
    drag_selector (bool): A flag to indicate if dragging is in progress.
    nearest_multipoint (int): Index of the nearest multipoint during dragging.
    drag_chip_data (dict): Data related to the chip being dragged.
    wire_drag_data (dict): Data related to the wire being dragged.
    pin_io_drag_data (dict): Data related to the pin_io being dragged.
    delete_mode_active (bool): A flag to indicate if delete mode is active.
    drag_mouse (list): The current mouse position [x,y].
    id_type (dict): A dictionary to store the type of each ID.
    """

    def __init__(self, canvas) -> None:
        self.canvas: tk.Canvas = canvas
        self.hole_func = self.draw_square_hole
        self.scale_factor = 1.0
        self.drag_selector = False
        self.nearest_multipoint = -1
        self.drag_chip_data = {"chip_id": None, "x": 0, "y": 0}
        self.wire_drag_data: dict[str, str | int | None] = {
            "wire_id": None,
            "endpoint": None,
            "x": 0,
            "y": 0,
            "creating_wire": False,
        }
        self.pin_io_drag_data = {"pin_id": None, "x": 0, "y": 0}
        self.delete_mode_active = False
        self.drag_mouse = [0, 0]
        self.id_type: dict[str, int] = {}
        self.current_dict_circuit: dict[str, Any] = {}
        self.matrix: dict[str, Any] = {}
        self.id_origins = {"xyOrigin": (0, 0)}

    def circuit(self, x_distance=0, y_distance=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
        """
        Generates a circuit layout on the canvas based on the provided parameters and model.
        Parameters:
        - x_distance (int, optional): Initial x-coordinate distance. Defaults to 0.
        - y_distance (int, optional): Initial y-coordinate distance. Defaults to 0.
        - scale (float, optional): Scaling factor for the circuit elements. Defaults to 1.
        - width (int, optional): Width of the circuit. If not -1, it overrides the scale. Defaults to -1.
        - direction (str, optional): Direction of the circuit layout. Can be VERTICAL, HORIZONTAL, or PERSO.
                                     Defaults to VERTICAL.
        - **kwargs: Additional keyword arguments:
            - model (list, optional): Custom model for the circuit layout. Defaults to line_distribution.
            - dXY (tuple, optional): Custom x and y distances for PERSO direction.
        Returns:
        - tuple: Updated x_distance and y_distance after laying out the circuit.
        Raises:
        - ValueError: If the model argument is not a valid tuple or list structure.
        """

        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale

        model = kwargs.get("model", [(self.draw_hole, 1)])
        _, delta_y = kwargs.get("dXY", (0, 1))

        x, y = x_distance, y_distance
        for element in model:
            if callable(element[0]) and isinstance(element[1], int):
                for _ in range(element[1]):
                    if len(element) == 3:
                        (x, y) = element[0](x, y, scale, width, **element[2])
                    else:
                        (x, y) = element[0](x, y, scale, width)
            elif isinstance(element[0], list) and isinstance(element[1], int):
                for _ in range(element[1]):
                    if len(element) == 3:
                        (x, y) = self.circuit(x, y, scale, width, model=element[0], **element[2])
                    else:
                        (x, y) = self.circuit(x, y, scale, width, model=element[0])
            else:
                raise ValueError(
                    "The rail model argument must be a tuple (function(), int, [int]) or (list, int, [int])."
                )

        if direction == HORIZONTAL:
            x_distance = x
        elif direction == VERTICAL:
            y_distance = y + inter_space
        elif direction == PERSO:
            y_distance = y - inter_space * delta_y

        return (x_distance, y_distance)

    def on_wire_endpoint_click(self, _, wire_id, endpoint):
        """
        Event handler for when a wire endpoint is clicked.
        """
        self.wire_drag_data["wire_id"] = wire_id
        self.wire_drag_data["endpoint"] = endpoint

        endpoint_tag = self.current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
        self.canvas.itemconfig(endpoint_tag, outline="red", fill="red")

    def on_wire_endpoint_drag(self, event, wire_id, endpoint):
        """
        Event handler for dragging a wire endpoint.
        """
        self.drag_selector = True
        if self.wire_drag_data["wire_id"] == wire_id and self.wire_drag_data["endpoint"] == endpoint:
            # Convert event coordinates to canvas coordinates
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)

            color = self.current_dict_circuit[wire_id]["color"]
            coord = self.current_dict_circuit[wire_id]["coord"]

            multipoints = self.current_dict_circuit[wire_id]["multipoints"]
            x_o, y_o = self.id_origins["xyOrigin"]
            if endpoint == "start":
                self.matrix[f"{coord[0][0]},{coord[0][1]}"]["state"] = FREE
            else:
                self.matrix[f"{coord[0][2]},{coord[0][3]}"]["state"] = FREE

            (_, _), (cn, ln) = self.find_nearest_grid_wire(canvas_x, canvas_y, matrix=self.matrix)
            if endpoint == "start":
                coord = [(cn, ln, coord[0][2], coord[0][3])]
            else:
                coord = [(coord[0][0], coord[0][1], cn, ln)]

            model_wire = [
                (
                    self.draw_wire,
                    1,
                    {
                        "id": wire_id,
                        "color": color,
                        "coord": coord,
                        "multipoints": multipoints,
                        "matrix": self.matrix,
                    },
                )
            ]
            self.circuit(x_o, y_o, model=model_wire)

    def on_wire_endpoint_release(self, _, wire_id, endpoint):
        """
        Event handler for when a wire endpoint is released.
        """
        if self.wire_drag_data["wire_id"] == wire_id and self.wire_drag_data["endpoint"] == endpoint:
            # Reset drag data
            self.wire_drag_data["wire_id"] = None
            self.wire_drag_data["endpoint"] = None

            # Remove highlight
            endpoint_tag = self.current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
            self.canvas.itemconfig(endpoint_tag, outline="#404040", fill="#dfdfdf")
            self.drag_selector = False

    def update_wire_body(self, wire_id):
        """
        Updates the wire body based on the positions of the endpoints.
        """
        params = self.current_dict_circuit[wire_id]
        start_pos = self.canvas.coords(params["endpoints"]["start"]["tag"])
        end_pos = self.canvas.coords(params["endpoints"]["end"]["tag"])

        # Calculate center positions of the endpoints
        start_x = (start_pos[0] + start_pos[2]) / 2
        start_y = (start_pos[1] + start_pos[3]) / 2
        end_x = (end_pos[0] + end_pos[2]) / 2
        end_y = (end_pos[1] + end_pos[3]) / 2

        # Update wire body coordinates
        self.canvas.coords(params["wire_body_tag"], start_x, start_y, end_x, end_y)

    def snap_wire_endpoint_to_grid(self, event, wire_id, endpoint):
        """
        Snaps the wire endpoint to the nearest grid point, excluding central points.
        """

        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        coord = self.current_dict_circuit[wire_id]["coord"]
        xy = [self.current_dict_circuit[wire_id]["XY"]]
        color = self.current_dict_circuit[wire_id]["color"]
        if endpoint == "start":
            x = canvas_x  # pos[0] # + dx
            y = canvas_y  # pos[1] # + dy
            (_, _), (col, line) = self.find_nearest_grid_chip(x, y)
            coord = [(col, line, coord[0][2], coord[0][3])]
        else:
            x = canvas_x  # pos[2] # + dx
            y = canvas_y  # pos[3] # + dy
            (_, _), (col, line) = self.find_nearest_grid_wire(x, y)
            coord = [(coord[0][0], coord[0][1], col, line)]

        model_wire = [
            (self.draw_wire, 1, {"id": wire_id, "color": color, "coord": coord, "XY": xy, "matrix": self.matrix})
        ]

        self.circuit(self.id_origins["xyOrigin"], model=model_wire)

    def find_nearest_grid_point(self, x, y, matrix=None):
        """
        Finds the nearest grid point to (x, y).
        """
        if matrix is None:
            matrix = self.matrix

        min_distance = float("inf")
        nearest_point = (x, y)
        nearest_point_col_lin = (0, 0)
        for _, point in matrix.items():
            grid_x, grid_y = point["xy"]
            distance = math.hypot(
                x - grid_x - self.id_origins["xyOrigin"][0], y - grid_y - self.id_origins["xyOrigin"][1]
            )
            if distance < min_distance:
                min_distance = distance
                nearest_point = (grid_x, grid_y)
                nearest_point_col_lin = point["coord"]

        return nearest_point, nearest_point_col_lin

    def find_nearest_grid(self, x, y, matrix=None):
        """
        Find the nearest grid point to the given x, y coordinates on lines 6 or 21 ('f' lines).

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            matrix (dict, optional): The grid matrix to use. Defaults to self.matrix.

        Returns:
            tuple: (nearest_x, nearest_y) coordinates of the nearest grid point.
        """
        if matrix is None:
            matrix = self.matrix

        min_distance = float("inf")

        (x_o, y_o) = self.id_origins["xyOrigin"]

        nearest_point = (0, 0)
        nearest_point_col_lin = (0, 0)
        for point in matrix.items():

            # Consider only lines 7 and 21 ('f' lines)
            _, line = point[1]["coord"]
            if line not in (7, 21):
                continue

            grid_x, grid_y = point[1]["xy"]

            distance = math.hypot(x - grid_x - x_o, y - grid_y - y_o)
            if distance < min_distance:
                min_distance = distance
                nearest_point = self.xy_hole2chip(grid_x + x_o, grid_y + y_o)
                nearest_point_col_lin = point[1]["coord"]

        return nearest_point, nearest_point_col_lin

    def find_nearest_multipoint(self, x, y, wire_id):
        """
        Find the nearest multipoint to the given x, y coordinates on the wire body.
        """
        nearest_point = -1
        multipoint = self.current_dict_circuit[wire_id]["multipoints"]
        [(x_start, y_start, x_end, y_end)] = self.current_dict_circuit[wire_id]["coord"]
        x_start, y_start = self.get_xy(x_start, y_start, matrix=self.matrix)
        x_end, y_end = self.get_xy(x_end, y_end, matrix=self.matrix)
        i = 0
        while nearest_point == -1 and i < len(multipoint):
            if math.hypot(x - multipoint[i], y - multipoint[i + 1]) <= 15:
                nearest_point = i
            i += 2
        insert_point = False
        if nearest_point == -1:
            x1, y1 = x_start, y_start
            i = 0
            while nearest_point == -1 and i < len(multipoint):
                dx, dy = multipoint[i] - x1, multipoint[i + 1] - y1
                t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
                proj_x = x1 + t * dx
                proj_y = y1 + t * dy
                dist_segment = math.hypot(x - proj_x, y - proj_y)
                if dist_segment <= 10:
                    nearest_point = i
                x1, y1 = multipoint[i], multipoint[i + 1]
                i += 2
            if nearest_point == -1:
                nearest_point = len(multipoint)
            insert_point = True
        self.current_dict_circuit[wire_id]["multipoints"] = multipoint
        return nearest_point, insert_point

    def on_wire_body_enter(self, _, wire_id):
        """
        Event handler for when the mouse enters the wire body.
        """
        if not self.drag_selector and not self.delete_mode_active and not self.wire_drag_data["creating_wire"]:
            color = self.current_dict_circuit[wire_id]["color"]
            encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"
            self.canvas.config(cursor=f"dot #{encre} {contour}")

    def on_wire_body_leave(self, *_):
        """
        Event handler for when the mouse leaves the wire body.
        """
        if not self.drag_selector and not self.wire_drag_data["creating_wire"]:
            self.canvas.config(cursor="arrow")

    def on_wire_body_click(self, event, wire_id) -> None:
        """
        Event handler for when the wire body is clicked.
        """
        x, y = event.x, event.y
        x_o, y_o = self.id_origins["xyOrigin"]
        self.nearest_multipoint, insert_point = self.find_nearest_multipoint(x - x_o, y - y_o, wire_id)
        if self.delete_mode_active:
            print(f"Deleting wire {wire_id}")
            self.delete_wire(wire_id)

        else:
            self.wire_drag_data["creating_wire"] = True
            self.wire_drag_data["wire_id"] = wire_id
            self.wire_drag_data["endpoint"] = "selector_cable"
            endpoint_tag = "selector_cable"

            color = self.current_dict_circuit[wire_id]["color"]
            encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"
            self.canvas.itemconfig(endpoint_tag, outline=contour, fill=encre)
            if insert_point:
                multipoints = self.current_dict_circuit[wire_id]["multipoints"]
                multipoints.insert(
                    self.nearest_multipoint,
                    x - x_o,
                )
                multipoints.insert(self.nearest_multipoint + 1, y - y_o)
                self.current_dict_circuit[wire_id]["multipoints"] = multipoints

    def on_wire_body_left_click(self, event, wire_id) -> None:
        """
        Event handler for when the wire body is left-clicked.
        """
        x, y = event.x, event.y
        x_o, y_o = self.id_origins["xyOrigin"]
        self.nearest_multipoint, insert_point = self.find_nearest_multipoint(x - x_o, y - y_o, wire_id)
        if not insert_point:
            print("Deleting multipoint")
            multipoints: list[int] = self.current_dict_circuit[wire_id]["multipoints"]
            multipoints.pop(self.nearest_multipoint)
            multipoints.pop(self.nearest_multipoint)
            self.current_dict_circuit[wire_id]["multipoints"] = multipoints
            model_wire = [
                (
                    self.draw_wire,
                    1,
                    {
                        "id": wire_id,
                        "multipoints": multipoints,
                        "coord": self.current_dict_circuit[wire_id]["coord"],
                        "color": self.current_dict_circuit[wire_id]["color"],
                        "XY": [self.current_dict_circuit[wire_id]["XY"]],
                        "matrix": self.matrix,
                    },
                )
            ]
            self.circuit(x_o, y_o, model=model_wire)

    def delete_wire(self, wire_id):
        """
        Deletes the wire from the canvas and updates the matrix.
        """
        wire_params = self.current_dict_circuit[wire_id]
        for tag in wire_params["tags"]:
            self.canvas.delete(tag)
        endpoints = (
            f"{wire_params['coord'][0][0]},{wire_params['coord'][0][1]}",
            f"{wire_params['coord'][0][2]},{wire_params['coord'][0][3]}",
        )
        # Restore occupied holes
        for hole_id in endpoints:
            self.matrix[hole_id]["state"] = FREE

        # Delete the wire from the dictionary
        del self.current_dict_circuit[wire_id]
        # TODO Khalid update the Circuit instance
        print(f"Wire {wire_id} deleted")

    def on_wire_body_drag(self, event, wire_id):
        """
        Event handler for dragging the wire body.
        """
        if self.delete_mode_active:
            return
        x_o, y_o = self.id_origins["xyOrigin"]
        x, y = event.x - x_o, event.y - y_o
        multipoints = self.current_dict_circuit[wire_id]["multipoints"]
        coord = self.current_dict_circuit[wire_id]["coord"]
        xy = [self.current_dict_circuit[wire_id]["XY"]]
        color = self.current_dict_circuit[wire_id]["color"]
        multipoints[self.nearest_multipoint] = x
        multipoints[self.nearest_multipoint + 1] = y

        model_wire = [
            (
                self.draw_wire,
                1,
                {
                    "id": wire_id,
                    "multipoints": multipoints,
                    "coord": coord,
                    "color": color,
                    "XY": xy,
                    "matrix": self.matrix,
                },
            )
        ]
        self.circuit(x_o, y_o, model=model_wire)

    def on_wire_body_release(self, *_):
        """
        Event handler for when the wire body is released.
        """
        self.wire_drag_data["creating_wire"] = False

    def start_chip_drag(self, event, chip_id):
        """
        Initiates drag for the clicked chip.
        """
        # Initiate drag by setting drag_chip_data
        self.drag_chip_data["chip_id"] = chip_id

        # Convert event coordinates to canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # Adjust for scaling
        adjusted_x = canvas_x  # / self.scale_factor
        adjusted_y = canvas_y  # / self.scale_factor

        self.drag_chip_data["x"] = adjusted_x
        self.drag_chip_data["y"] = adjusted_y

        chip_params = self.current_dict_circuit[chip_id]
        self.drag_chip_data["initial_XY"] = chip_params["XY"]

        if "occupied_holes" in chip_params:
            # Store the previous occupied holes in case we need to restore them
            self.drag_chip_data["previous_occupied_holes"] = chip_params["occupied_holes"]
            for hole_id in chip_params["occupied_holes"]:
                self.matrix[hole_id]["state"] = FREE
            chip_params["occupied_holes"] = []

        print(f"Chip {chip_id} clicked at ({adjusted_x}, {adjusted_y})")

    def on_chip_click(self, event, chip_id):
        """
        Event handler for chip clicks.
        Initiates drag and stores the initial mouse position.
        """
        print(f"Chip clicked: {chip_id}")

        if self.delete_mode_active:
            print(f"Deleting chip {chip_id}")
            self.delete_chip(chip_id)
        else:
            print(f"Starting drag for chip {chip_id}")
            self.start_chip_drag(event, chip_id)

    def delete_chip(self, chip_id):
        """
        Deletes the chip from the canvas and updates the matrix.
        """
        chip_params = self.current_dict_circuit[chip_id]
        for tag in chip_params["tags"]:
            self.canvas.delete(tag)

        # Restore occupied holes
        for hole_id in chip_params["occupied_holes"]:
            self.matrix[hole_id]["state"] = FREE

        # Delete the chip from the dictionary
        del self.current_dict_circuit[chip_id]
        # TODO Khalid update the Circuit instance
        print(f"Chip {chip_id} deleted")

    def on_chip_drag(self, event):
        """
        Event handler for dragging the chip.
        Moves the chip based on mouse movement.
        """
        chip_id = self.drag_chip_data["chip_id"]
        if chip_id:
            # Convert event coordinates to canvas coordinates
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)

            # Adjust for scaling
            adjusted_x = canvas_x  # / self.scale_factor
            adjusted_y = canvas_y  # / self.scale_factor

            # Calculate movement delta
            dx = adjusted_x - self.drag_chip_data["x"]
            dy = adjusted_y - self.drag_chip_data["y"]

            # Move all items associated with the chip
            chip_params = self.current_dict_circuit[chip_id]

            # Update drag_chip_data
            self.drag_chip_data["x"] = adjusted_x
            self.drag_chip_data["y"] = adjusted_y

            # Update chip's position
            current_x, current_y = chip_params["XY"]
            # chip_params["XY"] = (current_x + dx, current_y + dy)

            model_chip = [(self.draw_chip, 1, {"id": chip_id, "XY": (current_x + dx, current_y + dy)})]
            self.circuit(current_x + dx, current_y + dy, model=model_chip)

            print(f"Chip {chip_id} moved to new position: ({current_x}, {current_y})")

    def on_stop_chip_drag(self, _):
        """
        Event handler for stopping chip drag.
        """

        chip_id = self.drag_chip_data["chip_id"]
        if chip_id:
            (x, y) = self.current_dict_circuit[chip_id]["pinUL_XY"]
            (real_x, real_y), (col, line) = self.find_nearest_grid_chip(x, y)
            print(f"Real x: {real_x}, Real y: {real_y}")
            print(f"Col: {col}, Line: {line}")

            # Get chip parameters
            chip_params = self.current_dict_circuit[chip_id]
            pin_count = chip_params["pinCount"]
            half_pin_count = pin_count // 2

            # Check if there's enough space to the right
            max_column = col + half_pin_count - 1
            if max_column > 63:
                # Not enough space, prevent placement and look for the nearest snap point on the left
                print("Not enough space to place the chip here.")
                col = 63 - half_pin_count + 1
                (x_o, y_o) = self.id_origins["xyOrigin"]
                real_x, real_y = self.get_xy(col, line, matrix=self.matrix)
                real_x += x_o
                real_y += y_o
                (real_x, real_y), (col, line) = self.find_nearest_grid_chip(real_x, real_y)

            # the previous position to reset if the placement is not allowed
            previous_x, previous_y = self.drag_chip_data["initial_XY"]

            # Check if new holes are free
            holes_available = True
            occupied_holes = []
            for i in range(half_pin_count):
                # Top row (line 7 or 21)
                hole_id_top = f"{col + i},{line}"
                # Bottom row (line 6 or 20)
                hole_id_bottom = f"{col + i},{line + 1}"

                hole_top = self.matrix.get(hole_id_top)
                hole_bottom = self.matrix.get(hole_id_bottom)

                if hole_top["state"] != FREE or hole_bottom["state"] != FREE:
                    holes_available = False
                    break

                occupied_holes.extend([hole_id_top, hole_id_bottom])

            if not holes_available:
                print("Holes are occupied. Cannot place the chip here.")
                # Re-mark the previous holes as used
                previous_occupied_holes = self.drag_chip_data.get("previous_occupied_holes", [])
                for hole_id in previous_occupied_holes:
                    self.matrix[hole_id]["state"] = USED
                chip_params["occupied_holes"] = previous_occupied_holes

                real_x = previous_x
                real_y = previous_y
            else:
                # Mark new holes as used
                for hole_id in occupied_holes:
                    self.matrix[hole_id]["state"] = USED
                chip_params["occupied_holes"] = occupied_holes

            pin_x, pin_y = self.xy_chip2pin(real_x, real_y)
            model_chip = [(self.draw_chip, 1, {"id": chip_id, "XY": (real_x, real_y), "pinUL_XY": (pin_x, pin_y)})]
            self.circuit(real_x, real_y, model=model_chip)
            # Reset drag_chip_data
            self.drag_chip_data["chip_id"] = None
            self.drag_chip_data["x"] = 0
            self.drag_chip_data["y"] = 0
            self.drag_chip_data["previous_occupied_holes"] = []

    def get_chip_holes(self, x, y, pin_count):
        """
        Given the chip's upper-left pin position (x, y) and pin count,
        compute the list of hole IDs that the chip occupies.
        """
        half_pin_count = pin_count // 2
        holes = []
        col, line = self.get_col_line(x, y, matrix=self.matrix)
        if line not in [7, 21]:
            return holes  # Chip not on correct lines
        for i in range(half_pin_count):
            hole_id_top = f"{col + i},{line}"
            hole_id_bottom = f"{col + i},{line + 1}"
            holes.extend([hole_id_top, hole_id_bottom])
        return holes

    def xy_hole2chip(self, x_hole, y_hole, scale=1):
        """
        Convert hole coordinates to chip coordinates.
        """
        space = 9 * scale
        return (x_hole - 2 * scale, y_hole + space)

    def xy_chip2pin(self, x_chip, y_chip, scale=1):
        """
        Convert chip coordinates to pin coordinates.
        """
        space = 9 * scale
        return (x_chip + 2 * scale, y_chip - space)

    def find_nearest_grid_wire(self, x, y, matrix=None):
        """
        Find the nearest grid point to the given x, y coordinates on lines 6 or 21 ('f' lines).

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            matrix (dict, optional): The grid matrix to use. Defaults to self.matrix.

        Returns:
            tuple: (nearest_x, nearest_y) coordinates of the nearest grid point.
        """
        if matrix is None:
            matrix = self.matrix

        min_distance = float("inf")

        (x_o, y_o) = self.id_origins["xyOrigin"]

        nearest_point = (0, 0)
        nearest_point_col_lin = (0, 0)
        for point in matrix.items():

            if point[1]["state"] == FREE:
                grid_x, grid_y = point[1]["xy"]
                distance = math.hypot(x - grid_x - x_o, y - grid_y - y_o)
                if distance < min_distance:

                    min_distance = distance
                    nearest_point = self.xy_hole2chip(grid_x + x_o, grid_y + y_o)
                    nearest_point_col_lin = point[1]["coord"]

        return nearest_point, nearest_point_col_lin

    def find_nearest_grid_chip(self, x, y, matrix=None):
        """
        Find the nearest grid point to the given x, y coordinates on lines 6 or 21 ('f' lines).

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            matrix (dict, optional): The grid matrix to use. Defaults to self.matrix.

        Returns:
            tuple: (nearest_x, nearest_y) coordinates of the nearest grid point.
        """
        if matrix is None:
            matrix = self.matrix

        min_distance = float("inf")

        (x_o, y_o) = self.id_origins["xyOrigin"]

        nearest_point = (0, 0)
        nearest_point_col_lin = (0, 0)
        for point in matrix.items():

            _, line = point[1]["coord"]
            if line in (7, 21):
                grid_x, grid_y = point[1]["xy"]
                distance = math.hypot(x - grid_x - x_o, y - grid_y - y_o)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = self.xy_hole2chip(grid_x + x_o, grid_y + y_o)
                    nearest_point_col_lin = point[1]["coord"]

        return nearest_point, nearest_point_col_lin

    def on_pin_io_click(self, event, pin_id):
        """
        Event handler for when a pin_io element is clicked.
        """
        print(f"pin_io clicked: {pin_id}")
        if self.delete_mode_active:
            print(f"Deleting pin_io {pin_id}")
            self.delete_pin_io(pin_id)
        else:
            self.pin_io_drag_data["pin_id"] = pin_id

            # Convert event coordinates to canvas coordinates
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)

            # Store initial positions
            self.pin_io_drag_data["x"] = canvas_x
            self.pin_io_drag_data["y"] = canvas_y

            # Highlight the pin_io to indicate selection using outline_tag
            outline_tag = self.current_dict_circuit[pin_id]["outline_tag"]
            print(f"Highlighting outline_tag: {outline_tag}")
            self.canvas.itemconfig(outline_tag, outline="red")

    def delete_pin_io(self, pin_id):
        """
        Deletes the pin_io element from the canvas and updates the matrix.
        """
        pin_io_params = self.current_dict_circuit[pin_id]
        for tag in pin_io_params["tags"]:
            self.canvas.delete(tag)
        # Restore occupied holes
        hole_id = f"{pin_io_params['coord'][0][0]},{pin_io_params['coord'][0][1]}"
        self.matrix[hole_id]["state"] = FREE

        # Delete the pin_io from the dictionary
        del self.current_dict_circuit[pin_id]
        # TODO Khalid update the Circuit instance
        print(f"Pin_io {pin_id} deleted")

    def on_pin_io_drag(self, event, pin_id):
        """
        Event handler for dragging a pin_io element.
        """
        if self.pin_io_drag_data["pin_id"] == pin_id:
            # Convert event coordinates to canvas coordinates
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)

            x_o = self.id_origins["xyOrigin"][0]
            y_o = self.id_origins["xyOrigin"][1]

            coord = self.current_dict_circuit[pin_id]["coord"]

            (_, _), (col, line) = self.find_nearest_grid_point(canvas_x, canvas_y, matrix=self.matrix)

            if self.matrix[f"{col},{line}"]["state"] == FREE:

                self.matrix[f"{coord[0][0]},{coord[0][1]}"]["state"] = FREE
                model_pin_io = [(self.draw_pin_io, 1, {"id": pin_id, "coord": [(col, line)], "matrix": self.matrix})]
                self.circuit(x_o, y_o, model=model_pin_io)

    def on_pin_io_release(self, _, pin_id):
        """
        Event handler for when the pin_io element is released.
        """
        if self.pin_io_drag_data["pin_id"] == pin_id:
            # Reset drag data
            self.pin_io_drag_data["pin_id"] = None

            # Remove highlight using outline_tag
            outline_tag = self.current_dict_circuit[pin_id]["outline_tag"]
            print(f"Removing highlight from outline_tag: {outline_tag}")
            self.canvas.itemconfig(outline_tag, outline="#404040")

    def rounded_rect(self, x: int, y: int, width: int, height: int, radius: int, thickness: int, **kwargs) -> None:
        """
        Draws a rounded rectangle on a given canvas.
        Parameters:
        x (int): The x-coordinate of the top-left corner of the rectangle.
        y (int): The y-coordinate of the top-left corner of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        radius (int): The radius of the corners.
        thickness (int): The thickness of the rectangle's border.
        **kwargs: Additional keyword arguments to customize the rectangle, such as:
            - fill (str): The fill color of the rectangle.
            - tags (str): Tags to associate with the rectangle.
            - outline (str): The outline color of the rectangle.
        Returns:
        None
        """

        x2 = x + width
        y2 = y + height
        points = [
            x + radius,
            y,
            x2 - radius,
            y,
            x2,
            y + radius,
            x2,
            y2 - radius,
            x2 - radius,
            y2,
            x + radius,
            y2,
            x,
            y2 - radius,
            x,
            y + radius,
        ]
        tag = kwargs.get("tags", "")
        fill = kwargs.get("fill", "")
        thickness = kwargs.get("thickness", 1)

        # Draw four arcs for corners
        self.canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, style=tk.PIESLICE, **kwargs)
        self.canvas.create_arc(x2 - 2 * radius, y, x2, y + 2 * radius, start=0, extent=90, style=tk.PIESLICE, **kwargs)
        self.canvas.create_arc(
            x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs
        )
        self.canvas.create_arc(
            x, y2 - 2 * radius, x + 2 * radius, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs
        )
        # kwargs["outline"] = fill
        self.canvas.create_polygon(points, smooth=False, **kwargs)
        self.canvas.create_line(x + radius, y, x, y + radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x2 - radius, y, x2, y + radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x2 - radius, y2, x2, y2 - radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x, y2 - radius, x + radius, y2, fill=fill, width=thickness, tags=tag)

    def set_xy_origin(self, x_distance, y_distance, *_, **kwargs):
        """
        Set the origin of the XY coordinate system.
        """
        x_origin, y_origin = x_distance, y_distance
        id_origin = kwargs.get("id_origin", "xyOrigin")

        self.id_origins[id_origin] = (x_distance, y_distance)

        return (x_origin, y_origin)

    def go_xy(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Move the drawer to the given coordinates. # TODO check doc
        """
        line = kwargs.get("line", 0)
        column = kwargs.get("column", 0)
        id_origin = kwargs.get("id_origin", "xyOrigin")

        x_origin, y_origin = self.id_origins[id_origin]

        return (x_origin + column * 15 * scale, y_origin + line * 15 * scale)

    def draw_char(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a character at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        angle = kwargs.get("angle", 90)
        color = kwargs.get("color", "#000000")
        text = kwargs.get("text", "-")
        delta_y = kwargs.get("deltaY", 0)
        scale_char = kwargs.get("scaleChar", 1)
        anchor = kwargs.get("anchor", "center")
        tags = kwargs.get("tags", "")
        fira_code_font = font.Font(family="FiraCode-Bold.ttf", size=int(15 * scale * scale_char))

        if angle != 0:
            fira_code_font = font.Font(family="FiraCode-Light", size=int(15 * scale_char * scale))
            self.canvas.create_text(
                x_distance,
                y_distance + delta_y * space,
                text=text,
                font=fira_code_font,
                fill=color,
                anchor=anchor,
                angle=angle,
                tags=tags,
            )
        else:
            self.canvas.create_text(
                x_distance, y_distance, text=text, font=fira_code_font, fill=color, anchor=anchor, tags=tags
            )

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_char_iter(self, x_distance, y_distance, scale=1, width=-1, direction=VERTICAL_END_HORIZONTAL, **kwargs):
        """
        Draw a series of characters at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        begin_char = kwargs.get("beginChar", "A")
        num_chars = kwargs.get("numChars", 26)

        x = x_distance
        y = y_distance
        s = direction
        if direction == VERTICAL_END_HORIZONTAL:
            s = VERTICAL
        for i in range(num_chars):
            text = chr(ord(begin_char) + num_chars - i - 1)
            (x, y) = self.draw_char(x, y, scale, width, s, text=text, **kwargs)

        if direction == VERTICAL_END_HORIZONTAL:
            direction = HORIZONTAL

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space * num_chars

        return (x_distance, y_distance)

    def draw_num_iter(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a series of numbers at the given coordinates
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        begin_num = kwargs.get("beginNum", 0)
        end_num = kwargs.get("endNum", 9)

        x = x_distance + 3 * scale
        y = y_distance

        for i in range(begin_num, end_num + 1):
            text = str(i)
            (x, y) = self.draw_char(x, y, scale, width, direction=direction, text=text, scaleChar=0.7, **kwargs)

        if direction == HORIZONTAL:
            x_distance += inter_space * (end_num - begin_num)
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_square_hole(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a square hole at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale

        dark_color, light_color, hole_color = kwargs.get("colors", ["#c0c0c0", "#f6f6f6", "#484848"])

        self.canvas.create_polygon(
            x_distance,
            y_distance + space,
            x_distance,
            y_distance,
            x_distance + space,
            y_distance,
            fill=dark_color,
            outline=dark_color,
        )
        self.canvas.create_polygon(
            x_distance,
            y_distance + space,
            x_distance + space,
            y_distance + space,
            x_distance + space,
            y_distance,
            fill=light_color,
            outline=light_color,
        )
        self.canvas.create_rectangle(
            x_distance + space // 3,
            y_distance + space // 3,
            x_distance + 2 * space // 3,
            y_distance + 2 * space // 3,
            fill=hole_color,
            outline=hole_color,
        )

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_round_hole(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a round hole at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        dark_color, light_color, hole_color = kwargs.get("colors", ["#c0c0c0", "#f6f6f6", "#484848"])

        self.canvas.create_arc(
            x_distance,
            y_distance,
            x_distance + space,
            y_distance + space,
            start=45,
            extent=225,
            style=tk.PIESLICE,
            fill=dark_color,
            outline=dark_color,
        )
        self.canvas.create_arc(
            x_distance,
            y_distance,
            x_distance + space,
            y_distance + space,
            start=225,
            extent=45,
            style=tk.PIESLICE,
            fill=light_color,
            outline=light_color,
        )
        self.canvas.create_oval(
            x_distance + space // 3,
            y_distance + space // 3,
            x_distance + 2 * space // 3,
            y_distance + 2 * space // 3,
            fill=hole_color,
            outline=hole_color,
        )

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_hole(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a hole at the given coordinates with the appropriate hole function.
        """
        return self.hole_func(x_distance, y_distance, scale, width, direction, **kwargs)

    def sethole_func(self, x_distance, y_distance, *_, **kwargs):
        """
        Set the hole function to be used for drawing holes.
        """
        function = kwargs.get("function", self.draw_square_hole)

        self.hole_func = function

        return x_distance, y_distance

    def draw_blank(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **_):
        """
        Draw a blank space at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_half_blank(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **_):
        """
        Draw a half blank space at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        if direction == HORIZONTAL:
            x_distance += inter_space / 2
        elif direction == VERTICAL:
            y_distance += inter_space / 2

        return (x_distance, y_distance)

    def draw_rail(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a rail at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0
        color = kwargs.get("color", "black")

        inter_space = 15 * scale
        thickness = 2 * scale
        self.canvas.create_line(
            x_distance + inter_space // 3,
            y_distance + inter_space // 2,
            x_distance + inter_space * 1.5,
            y_distance + inter_space // 2,
            fill=color,
            width=thickness,
        )

        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_red_rail(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **_):
        """
        Draw a red rail at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        (x, _) = self.draw_rail(x_distance, y_distance - inter_space // 2, scale, width, direction, color="red")

        return (x, y_distance)

    def draw_board(self, x_distance=0, y_distance=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
        """
        Draw a board at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale
        thickness = 1 * scale

        dim = BOARD_830_PTS_PARAMS.copy()
        dim["dimLine"] = kwargs.get("dimLine", dim["dimLine"])
        dim["dimColumn"] = kwargs.get("dimColumn", dim["dimColumn"])
        color = kwargs.get("color", "#F5F5DC")
        sep_alim = kwargs.get("sepAlim", dim["sepAlim"])
        sep_distrib = kwargs.get("sepDistribution", dim["sepDistribution"])
        radius = kwargs.get("radius", 5)

        thickness = 1 * scale
        dim_line = dim["dimLine"] * inter_space
        dim_column = dim["dimColumn"] * inter_space
        self.id_origins["bottomLimit"] = (dim_line + x_distance, y_distance + dim_column)
        self.rounded_rect(
            x_distance, y_distance, dim_line, dim_column, radius, outline=color, fill=color, thickness=thickness
        )
        for sep in sep_alim:
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1],
                x_distance - inter_space * sep[0] + dim_line,
                y_distance + inter_space * sep[1],
                fill="#707070",
                width=thickness,
            )
        darkness_factor = 0.9
        r = int(color[1:3], 16) * (darkness_factor + 0.06)
        r = int(max(0, min(255, r)))
        g = int(color[3:5], 16) * (darkness_factor + 0.06)
        g = int(max(0, min(255, g)))
        b = int(color[5:7], 16) * (darkness_factor + 0.06)
        b = int(max(0, min(255, b)))
        c = [f"#{r:02x}{g:02x}{b:02x}"]
        r = int(color[1:3], 16) * (darkness_factor)
        r = int(max(0, min(255, r)))
        g = int(color[3:5], 16) * (darkness_factor)
        g = int(max(0, min(255, g)))
        b = int(color[5:7], 16) * (darkness_factor)
        b = int(max(0, min(255, b)))
        c.append(f"#{r:02x}{g:02x}{b:02x}")
        r *= darkness_factor
        g *= darkness_factor
        b *= darkness_factor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append(f"#{r:02x}{g:02x}{b:02x}")
        r *= darkness_factor
        g *= darkness_factor
        b *= darkness_factor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append(f"#{r:02x}{g:02x}{b:02x}")
        r *= darkness_factor
        g *= darkness_factor
        b *= darkness_factor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append(f"#{r:02x}{g:02x}{b:02x}")
        for sep in sep_distrib:
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1],
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1],
                fill=c[1],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + thickness,
                fill=c[2],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + 2 * thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + 2 * thickness,
                fill=c[3],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + 3 * thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + 3 * thickness,
                fill=c[4],
                width=thickness,
            )
            for dy in range(4, 11):
                self.canvas.create_line(
                    x_distance + inter_space * sep[0],
                    y_distance + inter_space * sep[1] + dy * thickness,
                    x_distance + dim_line - inter_space * sep[0],
                    y_distance + inter_space * sep[1] + dy * thickness,
                    fill=c[0],
                    width=thickness,
                )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 4 * thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 4 * thickness,
                fill=c[1],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 3 * thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 3 * thickness,
                fill=c[2],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 2 * thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - 2 * thickness,
                fill=c[3],
                width=thickness,
            )
            self.canvas.create_line(
                x_distance + inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - thickness,
                x_distance + dim_line - inter_space * sep[0],
                y_distance + inter_space * sep[1] + inter_space - thickness,
                fill=c[4],
                width=thickness,
            )

        return (x_distance, y_distance)

    ################ BOITIERS DIP ####################################

    def draw_pin(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a pin at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        tag = kwargs.get("tags", "")

        self.canvas.create_line(
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_line(
            x_distance - 18 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 18 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            x_distance - 18 * inter_space // 15,
            y_distance + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

    def draw_label_pin(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a label pin at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        tag = kwargs.get("tags", "")
        color = kwargs.get("color", "#ffffff")

        self.canvas.create_rectangle(
            x_distance,
            y_distance,
            x_distance + 4 * inter_space // 15,
            y_distance + orientation * 4 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )
        self.canvas.create_polygon(
            x_distance,
            y_distance + orientation * 4 * inter_space // 15,
            x_distance + 4 * inter_space // 15,
            y_distance + orientation * 4 * inter_space // 15,
            x_distance + 2 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )

    def draw_symb(self, logic_fn_name: str) -> Callable | None:
        """
        Return the sketcher function for the given logic function name.
        """
        logic_func_sketchers = {
            "NandGate": self.symb_nand,
            "NorGate": self.symb_nor,
            "AndGate": self.symb_and,
            "OrGate": self.symb_or,
            "NotGate": self.symb_not,
        }
        if logic_fn_name in logic_func_sketchers:
            return logic_func_sketchers[logic_fn_name]
        return None

    def draw_inv(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw an inverter at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        tag = kwargs.get("tags", "")
        color = kwargs.get("color", "#ffffff")
        color = "#ffffff"

        self.canvas.create_oval(
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 2.5 * inter_space // 15,
            x_distance + 11 * inter_space // 15,
            y_distance + orientation * 4.5 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )

    def draw_or(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw an OR gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        tag = kwargs.get("tags", "")

        self.canvas.create_rectangle(
            x_distance,
            y_distance,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )

        self.canvas.create_line(
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_arc(
            x_distance - 3 * inter_space // 15,
            y_distance,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            start=270,
            extent=180,
            fill="#000000",
            outline="#000000",
            tags=tag,
        )
        self.canvas.create_arc(
            x_distance - 3 * inter_space // 15,
            y_distance,
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            start=-90,
            extent=180,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )

    def symb_or(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw an OR gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        self.draw_or(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_pin(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def symb_nor(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a NOR gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        self.draw_or(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_inv(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_pin(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_aop(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a AOP at the given coordinates. # TODO what is this lol
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        tag = kwargs.get("tags", "")
        color = kwargs.get("color", "#ffffff")

        self.canvas.create_polygon(
            x_distance,
            y_distance,
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance,
            y_distance + orientation * 7 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )

    def symb_not(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a NOT gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        self.draw_aop(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_inv(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )

        self.draw_pin(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def draw_and(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw an AND gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        tag = kwargs.get("tags", "")

        self.canvas.create_rectangle(
            x_distance,
            y_distance,
            x_distance + 6 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )
        self.canvas.create_line(
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            x_distance + 12 * inter_space // 15,
            y_distance + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            x_distance - 3 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            x_distance + 3 * inter_space // 15,
            y_distance + orientation * 2 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_arc(
            x_distance + 6 * inter_space // 15 - 3 * inter_space // 15,
            y_distance,
            x_distance + 9 * inter_space // 15,
            y_distance + orientation * 7 * inter_space // 15,
            start=270,
            extent=180,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )

    def symb_and(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw an AND gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        self.draw_and(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_pin(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def symb_nand(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        """
        Draw a NAND gate at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        self.draw_and(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_inv(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        self.draw_pin(
            x_distance, y_distance, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs
        )
        if direction == HORIZONTAL:
            x_distance += inter_space
        elif direction == VERTICAL:
            y_distance += inter_space

        return (x_distance, y_distance)

    def internal_func(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw an internal function at the given coordinates.
        """
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        logic_function = kwargs.get("logicFunction", None)
        io = kwargs.get("io", [])
        pin_count = kwargs.get("pinCount", 14)
        chip_width = kwargs.get("chipWidth", 2.4)
        dim_column = chip_width * inter_space

        if logic_function is None:
            return
        for pin in io:
            p = pin[1][0]
            orientation = 1 - 2 * ((p - 1) * 2 // pin_count)
            if p > pin_count // 2:
                p = 15 - p
            x = x_distance + 2 * scale + space // 2 + (p - 2) * inter_space + 3 * inter_space // 15
            y = y_distance + dim_column // 2 + orientation * 0.2 * inter_space
            logic_function(x, y, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)

    def on_switch(self, _, tag, element_id, num_btn):
        """
        Handle the switch in the menu.
        """
        params = self.current_dict_circuit.get(element_id)
        if params:
            btn = params["btnMenu"][num_btn - 1]
            if btn > 0:
                btn = abs(btn - 2) + 1
                params["btnMenu"][num_btn - 1] = btn
                if btn == 1:
                    color = "#ff0000"
                    pos = LEFT
                    if num_btn == 1:
                        self.canvas.itemconfig("chipCover" + element_id, state="normal")
                else:
                    color = "#00ff00"
                    pos = RIGHT
                    if num_btn == 1:
                        self.canvas.itemconfig("chipCover" + element_id, state="hidden")
                self.canvas.move(tag, pos * 40 - 20, 0)
                self.canvas.itemconfig(tag, fill=color)

    def draw_switch(
        self,
        x1,
        y1,
        fill_support="#fffffe",
        fill_switch="#ff0000",
        out_switch="#000000",
        pos_switch=LEFT,
        tag=None,
        num_btn=1,
    ):
        """
        Draw a switch at the given coordinates.
        """
        self.canvas.create_arc(
            x1, y1, x1 + 20, y1 + 20, start=90, extent=180, fill=fill_support, outline=fill_support, tags=tag
        )
        self.canvas.create_arc(
            x1 + 20, y1, x1 + 40, y1 + 20, start=270, extent=180, fill=fill_support, outline=fill_support, tags=tag
        )
        self.canvas.create_rectangle(x1 + 10, y1, x1 + 30, y1 + 20, fill=fill_support, outline=fill_support, tags=tag)
        self.canvas.create_oval(
            x1 + 3 + pos_switch * 20,
            y1 + 3,
            x1 + 17 + pos_switch * 20,
            y1 + 17,
            fill=fill_switch,
            outline=out_switch,
            tags="btn" + str(num_btn) + "_" + tag,
        )
        self.canvas.addtag_withtag(tag, "btn" + str(num_btn) + "_" + tag)

    def on_drag_menu(self, event, tag):
        """
        Handle the drag of the menu.
        """
        self.canvas.move(tag, event.x - self.drag_mouse[0], event.y - self.drag_mouse[1])
        self.drag_mouse[0], self.drag_mouse[1] = event.x, event.y

    def on_start_drag_menu(self, event, tag):
        """
        Handle the start of the drag of the menu.
        """
        self.drag_mouse[0], self.drag_mouse[1] = event.x, event.y
        self.canvas.itemconfig(tag, fill="red")

    def on_stop_drag_menu(self, _, tag):
        """
        Handle the stop of the drag of the menu.
        """
        self.canvas.itemconfig(tag, fill="#ffffff")

    def on_cross_over(self, _, tag):
        """
        Handle the cross over the menu.
        """
        self.canvas.itemconfig("crossBg_" + tag, fill="#008000")

    def on_cross_leave(self, _, tag):
        """
        Handle the leave of the cross over the menu.
        """
        self.canvas.itemconfig("crossBg_" + tag, fill="")

    def on_cross_click(self, _, tag_menu, tag_ref):
        """
        Handle the click on the cross over the menu.
        """
        self.canvas.itemconfig(tag_menu, state="hidden")
        self.canvas.itemconfig(tag_ref, outline="")

    def draw_menu(self, x_menu, y_menu, thickness, label, tag, element_id):
        """
        Draw a menu at the given coordinates.
        """
        fill_menu = "#48484c"
        out_menu = "#909098"
        color_cross = "#e0e0e0"
        params = self.current_dict_circuit.get(element_id)
        if params:
            [btn1, btn2, btn3] = params["btnMenu"]
            if btn1 == 0:
                color1 = "#808080"
                pos1 = LEFT
            elif btn1 == 1:
                color1 = "#ff0000"
                pos1 = LEFT
            else:
                color1 = "#00ff00"
                pos1 = RIGHT
            if btn2 == 0:
                color2 = "#808080"
                pos2 = LEFT
            elif btn2 == 1:
                color2 = "#ff0000"
                pos2 = LEFT
            else:
                color2 = "#00ff00"
                pos2 = RIGHT
            if btn3 == 0:
                color3 = "#808080"
                pos3 = LEFT
            elif btn3 == 1:
                color3 = "#ff0000"
                pos3 = LEFT
            else:
                color3 = "#00ff00"
                pos3 = RIGHT

            self.rounded_rect(
                x_menu, y_menu, 128, 128, 10, outline=out_menu, fill=fill_menu, thickness=thickness, tags=tag
            )
            self.canvas.create_rectangle(
                x_menu, y_menu, x_menu + 114, y_menu + 17, fill="", outline="", tags="drag_" + tag
            )
            self.canvas.create_line(
                x_menu, y_menu + 17, x_menu + 127, y_menu + 17, fill=out_menu, width=thickness, tags=tag
            )
            self.canvas.create_rectangle(
                x_menu + 110, y_menu + 1, x_menu + 125, y_menu + 16, fill="", outline="", tags="crossBg_" + tag
            )
            self.canvas.create_line(
                x_menu + 115,
                y_menu + 5,
                x_menu + 120,
                y_menu + 12,
                fill=color_cross,
                width=thickness * 2,
                tags="cross_" + tag,
            )
            self.canvas.create_line(
                x_menu + 115,
                y_menu + 12,
                x_menu + 120,
                y_menu + 5,
                fill=color_cross,
                width=thickness * 2,
                tags="cross_" + tag,
            )
            self.draw_char(
                x_menu + 63,
                y_menu + 8,
                scaleChar=0.8,
                angle=0,
                text=label,
                color="#ffffff",
                anchor="center",
                tags="title_" + tag,
            )
            self.draw_switch(
                x_menu + 10, y_menu + 27, fill_switch=color1, pos_switch=pos1, tag="switch_" + tag, num_btn=1
            )
            self.canvas.tag_bind(
                "btn1_switch_" + tag,
                "<Button-1>",
                lambda event: self.on_switch(event, "btn1_switch_" + tag, element_id, 1),
            )
            self.draw_aop(x_menu + 82, y_menu + 32, scale=2, color="#000000", tags=tag)
            self.draw_aop(x_menu + 80, y_menu + 30, scale=2, tags=tag)
            self.draw_switch(
                x_menu + 10, y_menu + 60, fill_switch=color2, pos_switch=pos2, tag="switch_" + tag, num_btn=2
            )
            self.canvas.tag_bind(
                "btn2_switch_" + tag,
                "<Button-1>",
                lambda event: self.on_switch(event, "btn2_switch_" + tag, element_id, 2),
            )
            self.draw_label_pin(x_menu + 68, y_menu + 65, scale=2, color="#000000", tags=tag)
            self.draw_label_pin(x_menu + 65, y_menu + 62, scale=2, color="#faa000", tags=tag)
            self.draw_label_pin(x_menu + 88, y_menu + 65, scale=2, color="#000000", tags=tag)
            self.draw_label_pin(x_menu + 85, y_menu + 62, scale=2, color="#faa000", tags=tag)
            self.draw_label_pin(x_menu + 108, y_menu + 65, scale=2, color="#000000", tags=tag)
            self.draw_label_pin(x_menu + 105, y_menu + 62, scale=2, color="#faa000", tags=tag)
            self.draw_switch(
                x_menu + 10, y_menu + 93, fill_switch=color3, pos_switch=pos3, tag="switch_" + tag, num_btn=3
            )

            self.canvas.tag_bind(
                "btn3_switch_" + tag,
                "<Button-1>",
                lambda event: self.on_switch(event, "btn3_switch_" + tag, element_id, 3),
            )
            self.canvas.tag_raise("drag_" + tag)
            self.canvas.addtag_withtag(tag, "title_" + tag)
            self.canvas.addtag_withtag(tag, "crossBg_" + tag)
            self.canvas.addtag_withtag(tag, "cross_" + tag)
            self.canvas.addtag_withtag(tag, "btn_" + tag)
            self.canvas.addtag_withtag(tag, "drag_" + tag)
            self.canvas.addtag_withtag(tag, "switch_" + tag)
            self.canvas.addtag_withtag("componentMenu", tag)
            self.canvas.tag_bind("drag_" + tag, "<B1-Motion>", lambda event: self.on_drag_menu(event, tag))
            self.canvas.tag_bind(
                "drag_" + tag, "<Button-1>", lambda event: self.on_start_drag_menu(event, "title_" + tag)
            )
            self.canvas.tag_bind("cross_" + tag, "<Enter>", lambda event: self.on_cross_over(event, tag))
            self.canvas.tag_bind("cross_" + tag, "<Leave>", lambda event: self.on_cross_leave(event, tag))
            self.canvas.tag_bind(
                "cross_" + tag, "<Button-1>", lambda event: self.on_cross_click(event, tag, "activeArea" + element_id)
            )
            self.canvas.tag_bind(
                "drag_" + tag, "<ButtonRelease-1>", lambda event: self.on_stop_drag_menu(event, "title_" + tag)
            )
            self.canvas.itemconfig(tag, state="hidden")

    def on_menu(self, _, tag_menu, tag_all, tag_reg, color_out="#60d0ff"):
        """
        Handle the menu.
        """
        self.canvas.tag_raise(tag_menu)
        self.canvas.itemconfig(tag_all, state="hidden")
        self.canvas.itemconfig(tag_menu, state="normal")
        self.canvas.itemconfig("componentActiveArea", outline="")
        self.canvas.itemconfig(tag_reg, outline=color_out)

    def change_hole_state(self, col, line, pin_count, state):
        """
        Change the state of the holes at (col, line).
        """
        for i in range(pin_count // 2):
            self.matrix[f"{col+i},{line}"]["state"] = state
            self.matrix[f"{col+i},{line+1}"]["state"] = state

    def draw_chip(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a chip at the given coordinates. Also handles putting it in the dict, among other stuff.
        """
        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale
        space = 9 * scale
        thickness = 1 * scale

        dim = DIP14_PARAMS.copy()
        dim["pinCount"] = kwargs.get("pinCount", dim["pinCount"])
        dim["chipWidth"] = kwargs.get("chipWidth", dim["chipWidth"])
        dim["label"] = kwargs.get("label", dim["label"])
        dim["internalFunc"] = kwargs.get("internalFunc", None)
        dim["pwr"] = kwargs.get("pwr", None)

        logic_function_name = kwargs.get("logicFunctionName", None)

        cover_open = kwargs.get("open", NO)
        chip_id = kwargs.get("id", None)
        tags = kwargs.get("tags", [])
        chip_type = kwargs.get("type", "chip")

        dim_line = (dim["pinCount"] - 0.30) * inter_space / 2
        dim_column = dim["chipWidth"] * inter_space

        params = {}
        if chip_id:
            if self.current_dict_circuit.get(chip_id):
                params = self.current_dict_circuit[chip_id]
                tags = params["tags"]
        else:
            if chip_type not in self.id_type:
                self.id_type[chip_type] = 0
            if "chip" not in self.id_type:
                self.id_type["chip"] = 0
            self.id_type[chip_type] += 1
            chip_id = "_chip_" + str(self.id_type["chip"])
            self.current_dict_circuit["last_id"] = chip_id
            self.id_type["chip"] += 1
            _, (col, line) = self.find_nearest_grid_point(x_distance, y_distance)
            self.change_hole_state(col, line, dim["pinCount"], USED)

        if not tags:
            params["id"] = chip_id
            params["XY"] = (x_distance, y_distance)
            params["pinUL_XY"] = (x_distance + 2 * scale, y_distance - space * scale)
            params["chipWidth"] = dim["chipWidth"]
            params["pinCount"] = dim["pinCount"]
            dim_line = (dim["pinCount"] - 0.30) * inter_space / 2
            dim_column = dim["chipWidth"] * inter_space
            label = dim["label"] + "-" + str(self.id_type[chip_type])
            params["label"] = label
            params["type"] = chip_type
            params["btnMenu"] = [1, 1, 0]
            params["pwr"] = dim["pwr"]
            num_pins_per_side = dim["pinCount"] // 2
            tag_base = "base" + chip_id
            tag_menu = "menu" + chip_id
            tag_cover = "chipCover" + chip_id
            tag_mouse = "activeArea" + chip_id

            params["tags"] = [tag_base, tag_mouse]

            for i in range(dim["pinCount"]):
                self.canvas.create_rectangle(
                    x_distance + 2 * scale + (i % num_pins_per_side) * inter_space,
                    y_distance - (0 - (i // num_pins_per_side) * (dim_column + 0)),
                    x_distance + 11 * scale + (i % num_pins_per_side) * inter_space,
                    y_distance - (3 * scale - (i // num_pins_per_side) * (dim_column + 6 * scale)),
                    fill="#909090",
                    outline="#000000",
                    tags=tag_base,
                )
                self.canvas.create_polygon(
                    x_distance + 2 * scale + (i % num_pins_per_side) * inter_space,
                    y_distance - space // 3 - (0 - (i // num_pins_per_side) * (dim_column + 2 * space // 3)),
                    x_distance + space // 3 + 2 * scale + (i % num_pins_per_side) * inter_space,
                    y_distance - (2 * space) // 3 - (0 - (i // num_pins_per_side) * (dim_column + (4 * space) // 3)),
                    x_distance + (2 * space) // 3 + 2 * scale + (i % num_pins_per_side) * inter_space,
                    y_distance - (2 * space) // 3 - (0 - (i // num_pins_per_side) * (dim_column + (4 * space) // 3)),
                    x_distance + (11 + (i % num_pins_per_side) * 15) * scale,
                    y_distance - space // 3 - (0 - (i // num_pins_per_side) * (dim_column + 2 * space // 3)),
                    fill="#b0b0b0",
                    outline="#000000",
                    smooth=False,
                    tags=tag_base,
                )

            params["pinUL_XY"] = (x_distance + 2 * scale, y_distance - space)
            self.canvas.create_rectangle(
                x_distance + 2 * scale,
                y_distance - space,
                x_distance + 3 * scale,
                y_distance - space + 1,
                fill="#0000ff",
                outline="#0000ff",
                tags=tag_base,
            )

            self.rounded_rect(
                x_distance,
                y_distance,
                dim_line,
                dim_column,
                5,
                outline="#343434",
                fill="#343434",
                thickness=thickness,
                tags=tag_base,
            )

            self.canvas.create_rectangle(
                x_distance + 2 * scale,
                y_distance + 2 * scale,
                x_distance - 2 * scale + dim_line,
                y_distance - 2 * scale + dim_column,
                fill="#000000",
                outline="#000000",
                tags=tag_base,
            )
            # FIXME false so it is never called, rework is for the future
            if False and "internalFunc" in dim and dim["internalFunc"] is not None:
                dim["internalFunc"](x_distance, y_distance, scale=scale, tags=tag_base, **kwargs)

            self.rounded_rect(
                x_distance,
                y_distance,
                dim_line,
                dim_column,
                5,
                outline="#343434",
                fill="#343434",
                thickness=thickness,
                tags=tag_cover,
            )
            self.canvas.create_line(
                x_distance,
                y_distance + 1 * space // 3,
                x_distance + dim_line,
                y_distance + 1 * space // 3,
                fill="#b0b0b0",
                width=thickness,
                tags=tag_cover,
            )
            self.canvas.create_line(
                x_distance,
                y_distance + dim_column - 1 * space // 3,
                x_distance + dim_line,
                y_distance + dim_column - 1 * space // 3,
                fill="#b0b0b0",
                width=thickness,
                tags=tag_cover,
            )
            self.canvas.create_oval(
                x_distance + 4 * scale,
                y_distance + dim_column - 1 * space // 3 - 6 * scale,
                x_distance + 8 * scale,
                y_distance + dim_column - 1 * space // 3 - 2 * scale,
                fill="#ffffff",
                outline="#ffffff",
                tags=tag_cover,
            )
            self.canvas.create_arc(
                x_distance - 5 * scale,
                y_distance + dim_column // 2 - 5 * scale,
                x_distance + 5 * scale,
                y_distance + dim_column // 2 + 5 * scale,
                start=270,
                extent=180,
                fill="#000000",
                outline="#505050",
                style=tk.PIESLICE,
                tags=tag_cover,
            )
            self.draw_char(
                x_distance + dim_line // 2,
                y_distance + dim_column // 2,
                scale=scale,
                angle=0,
                text=label,
                color="#ffffff",
                anchor="center",
                tags=tag_cover,
            )
            self.canvas.create_rectangle(
                x_distance + 2 * scale,
                y_distance + 2 * scale,
                x_distance - 2 * scale + dim_line,
                y_distance - 2 * scale + dim_column,
                fill="",
                outline="",
                tags=tag_mouse,
            )
            self.canvas.tag_raise(tag_cover)
            self.canvas.tag_raise(tag_mouse)
            self.canvas.addtag_withtag("componentActiveArea", tag_mouse)
            if cover_open:
                self.canvas.itemconfig(tag_cover, state="hidden")
            else:
                params["tags"].append(tag_cover)
            self.current_dict_circuit[chip_id] = params
            self.draw_menu(
                x_distance + dim_line + 2.3 * scale + space * 0, y_distance - space, thickness, label, tag_menu, chip_id
            )
            # Only bind a tag to the menu if it has an internal function
            # FIXME (maybe?)
            # FIXME: false so it is never bound, rework is for the future
            if (
                False
                and "internalFunc" in dim
                and dim["internalFunc"] is not None
                and "logicFunction" in kwargs
                and kwargs["logicFunction"] is not None
            ):
                self.canvas.tag_bind(
                    tag_mouse, "<Button-3>", lambda event: self.on_menu(event, tag_menu, "componentMenu", tag_mouse)
                )
            # Bind left-click to initiate drag
            self.canvas.tag_bind(
                tag_mouse, "<Button-1>", lambda event, chip_id=chip_id: self.on_chip_click(event, chip_id)
            )

            # Bind drag and release events to the activeArea tag
            self.canvas.tag_bind(tag_mouse, "<B1-Motion>", self.on_chip_drag)
            self.canvas.tag_bind(tag_mouse, "<ButtonRelease-1>", self.on_stop_chip_drag)
        else:
            x, y = params["XY"]
            d_x = x_distance - x
            d_y = y_distance - y
            params["XY"] = (x_distance, y_distance)
            params["pinUL_XY"] = (x_distance + 2 * scale, y_distance - space * scale)
            for tg in tags:
                self.canvas.move(tg, d_x, d_y)

        return x_distance + dim_line + 2.3 * scale, y_distance

    def get_col_line(self, x, y, scale=1, **kwargs):
        """
        Get the column and line of the given coordinates.
        """
        matrix = self.matrix
        point_col_lin = (-1, -1)

        for point in matrix.items():
            grid_x, grid_y = point[1]["xy"]

            if (grid_x, grid_y) == (x, y):
                point_col_lin = point[1]["coord"]

        return point_col_lin

    def get_xy(self, column, line, scale=1, **kwargs):
        """
        Get the x and y coordinates of the given column and line.
        """
        matrix = self.matrix

        element_id = str(column) + "," + str(line)
        x, y = matrix[element_id]["xy"]

        return x * scale, y * scale

    def draw_wire(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw a wire at the given coordinates. Also handles putting it in the dict, among other stuff.
        """
        if width != -1:
            scale = width / 9.0

        color = kwargs.get("color", (0, 0, 0))
        mode = kwargs.get("mode", AUTO)
        coord = kwargs.get("coord", [])
        matrix = self.matrix
        wire_id = kwargs.get("id", None)
        (xs, ys, xe, ye) = kwargs.get("XY", [(0, 0, 0, 0)])[0]
        multipoints = kwargs.get("multipoints", [])
        thickness = 1 * scale

        params = {}
        if wire_id:  # If the wire already exists, delete it and redraw
            if self.current_dict_circuit.get(wire_id):
                params = self.current_dict_circuit[wire_id]
                params["mode"] = mode
                params["coord"] = coord
                params["multipoints"] = multipoints
                x_start, y_start, x_end, y_end = coord[0]
                if x_start != -1:
                    x_start, y_start = self.get_xy(x_start, y_start, scale=scale, matrix=matrix)
                else:
                    x_start, y_start = xs, ys
                if x_end != -1:
                    x_end, y_end = self.get_xy(x_end, y_end, scale=scale, matrix=matrix)
                else:
                    x_end, y_end = xe, ye
                x1_old, y1_old, x2_old, y2_old = params["XY"]
                dx1, dy1 = x_start - x1_old, y_start - y1_old
                dx2, dy2 = x_end - x2_old, y_end - y2_old
                params["XY"] = (x_start, y_start, x_end, y_end)
                params["color"] = color
                encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"
                wire_body_tag = f"{wire_id}_body"
                wire_body_shadow_tag = f"{wire_id}_body_shadow"
                start_endpoint_tag = f"{wire_id}_start"
                end_endpoint_tag = f"{wire_id}_end"
                select_start_tag = f"{wire_id}_select_start"
                select_end_tag = f"{wire_id}_select_end"
                multipoints = [x_start, y_start] + multipoints + [x_end, y_end]
                multipoints = [
                    val + 5 * scale + (x_distance if i % 2 == 0 else y_distance) for i, val in enumerate(multipoints)
                ]
                self.canvas.coords(wire_body_tag, multipoints)
                self.canvas.coords(wire_body_shadow_tag, multipoints)
                self.canvas.move(start_endpoint_tag, dx1, dy1)
                self.canvas.move(end_endpoint_tag, dx2, dy2)
                self.canvas.move(select_start_tag, dx1, dy1)
                self.canvas.move(select_end_tag, dx2, dy2)
        else:
            if "wire" not in self.id_type:
                self.id_type["wire"] = 0
            wire_id = "_wire_" + str(self.id_type["wire"])
            self.current_dict_circuit["last_id"] = wire_id
            self.id_type["wire"] += 1
            params["id"] = wire_id
            params["mode"] = mode
            params["coord"] = coord
            params["multipoints"] = multipoints
            x_start, y_start, x_end, y_end = coord[0]

            if x_start != -1:
                x_start, y_start = self.get_xy(x_start, y_start, scale=scale, matrix=matrix)
            else:
                x_start, y_start = xs, ys
            if x_end != -1:
                x_end, y_end = self.get_xy(x_end, y_end, scale=scale, matrix=matrix)
            else:
                x_end, y_end = xe, ye

            params["XY"] = (x_start, y_start, x_end, y_end)
            params["color"] = color
            encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"

            # Define unique tags for the wire components
            wire_body_tag = f"{wire_id}_body"
            wire_body_shadow_tag = f"{wire_id}_body_shadow"
            start_endpoint_tag = f"{wire_id}_start"
            end_endpoint_tag = f"{wire_id}_end"
            select_start_tag = f"{wire_id}_select_start"
            select_end_tag = f"{wire_id}_select_end"
            self.canvas.create_oval(
                x_distance + x_start + 2 * scale,
                y_distance + y_start + 2 * scale,
                x_distance + x_start + 7 * scale,
                y_distance + y_start + 7 * scale,
                fill="#dfdfdf",
                outline="#404040",
                width=1 * thickness,
                tags=(wire_id, start_endpoint_tag),
            )
            self.canvas.create_oval(
                x_distance + x_start - 2 * scale,
                y_distance + y_start - 2 * scale,
                x_distance + x_start + 9 * scale,
                y_distance + y_start + 9 * scale,
                fill="",
                outline="",
                width=1 * thickness,
                tags=(wire_id, select_start_tag),
            )
            self.canvas.create_oval(
                x_distance + x_end + 2 * scale,
                y_distance + y_end + 2 * scale,
                x_distance + x_end + 7 * scale,
                y_distance + y_end + 7 * scale,
                fill="#dfdfdf",
                outline="#404040",
                width=1 * thickness,
                tags=(wire_id, end_endpoint_tag),
            )
            self.canvas.create_oval(
                x_distance + x_end - 2 * scale,
                y_distance + y_end - 2 * scale,
                x_distance + x_end + 9 * scale,
                y_distance + y_end + 9 * scale,
                fill="",
                outline="",
                width=1 * thickness,
                tags=(wire_id, select_end_tag),
            )

            multipoints = [x_start, y_start] + multipoints + [x_end, y_end]
            multipoints = [
                val + 5 * scale + (x_distance if i % 2 == 0 else y_distance) for i, val in enumerate(multipoints)
            ]
            self.canvas.create_line(
                multipoints, fill=contour, width=8 * thickness, tags=(wire_id, wire_body_shadow_tag)
            )
            self.canvas.create_line(multipoints, fill=encre, width=4 * thickness, tags=(wire_id, wire_body_tag))
            # Store tags and positions in params
            params["tags"] = [wire_id, wire_body_tag, start_endpoint_tag, end_endpoint_tag]
            params["wire_body_tag"] = wire_body_tag
            params["endpoints"] = {
                "start": {"position": (x_distance + x_start, y_distance + y_start), "tag": start_endpoint_tag},
                "end": {"position": (x_distance + x_end, y_distance + y_end), "tag": end_endpoint_tag},
            }
            self.canvas.tag_raise(select_start_tag)
            self.canvas.tag_raise(select_end_tag)
            # Bind events to the endpoints for drag-and-drop

            self.canvas.tag_bind(
                wire_body_tag, "<Enter>", lambda event, wire_id=wire_id: self.on_wire_body_enter(event, wire_id)
            )
            self.canvas.tag_bind(
                wire_body_tag, "<Leave>", lambda event, wire_id=wire_id: self.on_wire_body_leave(event, wire_id)
            )
            self.canvas.tag_bind(
                wire_body_tag, "<Button-1>", lambda event, wire_id=wire_id: self.on_wire_body_click(event, wire_id)
            )
            self.canvas.tag_bind(
                wire_body_tag, "<Button-3>", lambda event, wire_id=wire_id: self.on_wire_body_left_click(event, wire_id)
            )
            self.canvas.tag_bind(
                wire_body_tag, "<B1-Motion>", lambda event, wire_id=wire_id: self.on_wire_body_drag(event, wire_id)
            )

            self.canvas.tag_bind(
                wire_body_tag,
                "<ButtonRelease-1>",
                lambda event, wire_id=wire_id: self.on_wire_body_release(event, wire_id),
            )

            self.canvas.tag_bind(
                select_start_tag,
                "<Button-1>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_click(event, wire_id, "start"),
            )
            self.canvas.tag_bind(
                select_end_tag,
                "<Button-1>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_click(event, wire_id, "end"),
            )

            self.canvas.tag_bind(
                select_start_tag,
                "<B1-Motion>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_drag(event, wire_id, "start"),
            )
            self.canvas.tag_bind(
                select_end_tag,
                "<B1-Motion>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_drag(event, wire_id, "end"),
            )

            self.canvas.tag_bind(
                select_start_tag,
                "<ButtonRelease-1>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_release(event, wire_id, "start"),
            )
            self.canvas.tag_bind(
                select_end_tag,
                "<ButtonRelease-1>",
                lambda event, wire_id=wire_id: self.on_wire_endpoint_release(event, wire_id, "end"),
            )

        matrix[f"{coord[0][0]},{coord[0][1]}"]["state"] = USED
        matrix[f"{coord[0][2]},{coord[0][3]}"]["state"] = USED

        self.current_dict_circuit[wire_id] = params

        return x_distance, y_distance

    def draw_pin_io(self, x_distance, y_distance, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        """
        Draw an input/output pin at the given coordinates. Also handles putting it in the dict, among other stuff.
        """
        if width != -1:
            scale = width / 9.0
        matrix = self.matrix
        element_id = kwargs.get("id", None)
        coord = kwargs.get("coord", [])
        element_type = kwargs.get("type", INPUT)
        color = kwargs.get("color", "#479dff")
        thickness = 1 * scale

        if element_id and self.current_dict_circuit.get(element_id):
            params = self.current_dict_circuit[element_id]
            old_x, old_y = params["XY"]
            params["coord"] = coord
            x_origin, y_origin = coord[0]
            x_origin, y_origin = self.get_xy(x_origin, y_origin, scale=scale, matrix=matrix)
            dx = x_origin - old_x
            dy = y_origin - old_y

            self.canvas.move(element_id, dx, dy)
            params["XY"] = (x_origin, y_origin)
            params["color"] = color

        else:
            if "io" not in self.id_type:
                self.id_type["io"] = 0
            element_id = "_io_" + str(self.id_type["io"])
            self.id_type["io"] += 1
            params = {}
            params["id"] = element_id
            params["tags"] = []
            params["coord"] = coord
            x_origin, y_origin = coord[0]
            x_origin, y_origin = self.get_xy(x_origin, y_origin, scale=scale, matrix=matrix)
            params["XY"] = (x_origin, y_origin)
            params["controller_pin"] = "IO"
            params["type"] = element_type
            params["color"] = color

            # tags here
            pin_tag = f"pin_io_{element_id}"
            outline_tag = f"pin_io_outline_{element_id}"
            interactive_tag = f"pin_io_interactive_{element_id}"
            params["outline_tag"] = outline_tag
            params["tag"] = pin_tag

            # Draw the vertical line
            line_id = self.canvas.create_line(
                x_distance + x_origin + 5 * scale,
                y_distance + y_origin - 3 * scale,
                x_distance + x_origin + 5 * scale,
                y_distance + y_origin + 2 * scale,
                fill=color,
                width=4 * thickness,
                tags=(element_id, pin_tag, interactive_tag),
            )
            params["tags"].append(line_id)

            # Draw the circle at the bottom
            oval_id = self.canvas.create_oval(
                x_distance + x_origin + 2 * scale,
                y_distance + y_origin + 2 * scale,
                x_distance + x_origin + 7 * scale,
                y_distance + y_origin + 7 * scale,
                fill="#dfdfdf",
                outline="#404040",
                width=1 * thickness,
                tags=(element_id, pin_tag, interactive_tag, outline_tag),
            )
            params["tags"].append(oval_id)

            # Draw the larger rhombus on top of the line (supports outline)
            polygon_id = self.canvas.create_polygon(
                x_distance + x_origin - 10 * scale,
                y_distance + y_origin - 18 * scale,
                x_distance + x_origin + 5 * scale,
                y_distance + y_origin - 33 * scale,
                x_distance + x_origin + 20 * scale,
                y_distance + y_origin - 18 * scale,
                x_distance + x_origin + 5 * scale,
                y_distance + y_origin - 3 * scale,
                fill=color,
                outline="#404040",
                width=1 * thickness,
                tags=(element_id, pin_tag, interactive_tag, outline_tag),
            )
            params["tags"].append(polygon_id)

            # Bring the rhombus to the front
            self.canvas.tag_raise(element_id)

            # take the last number of the element_id as the pin number as an integer
            pin_number = element_id.rsplit("_", maxsplit=1)[-1]

            label_x = (x_distance + x_origin + 5 * scale,)
            label_y = (y_distance + y_origin - 17 * scale,)

            label_tag = f"{element_id}_label"
            text_id = self.canvas.create_text(
                label_x,
                label_y,
                text=pin_number,
                font=("FiraCode-Bold", int(7 * scale)),
                fill="#000000",
                anchor="center",
                tags=(element_id, label_tag),
            )
            params["label_tag"] = label_tag
            params["tags"].append(text_id)

            if element_type == INPUT:
                # Arrow pointing down
                # arrow_line_id = self.canvas.create_line(
                #     x_distance + x_origin + 5 * scale,
                #     y_distance + y_origin - 23 * scale,
                #     x_distance + x_origin + 5 * scale,
                #     y_distance + y_origin - 13 * scale,
                #     fill="#404040",
                #     width=2 * thickness,
                #     tags=(element_id, interactive_tag),
                # )
                # params["tags"].append(arrow_line_id)

                arrow_head_id = self.canvas.create_polygon(
                    x_distance + x_origin + 0 * scale,
                    y_distance + y_origin - 13 * scale,
                    x_distance + x_origin + 10 * scale,
                    y_distance + y_origin - 13 * scale,
                    x_distance + x_origin + 5 * scale,
                    y_distance + y_origin - 8 * scale,
                    fill="#404040",
                    outline="#404040",
                    tags=(element_id, interactive_tag, outline_tag),
                )
                params["tags"].append(arrow_head_id)
            elif element_type == OUTPUT:
                # Arrow pointing up
                # arrow_line_id = self.canvas.create_line(
                #     x_distance + x_origin + 5 * scale,
                #     y_distance + y_origin - 23 * scale,
                #     x_distance + x_origin + 5 * scale,
                #     y_distance + y_origin - 13 * scale,
                #     fill="#000000",
                #     width=2 * thickness,
                #     tags=(element_id, interactive_tag),
                # )
                # params["tags"].append(arrow_line_id)

                arrow_head_id = self.canvas.create_polygon(
                    x_distance + x_origin + 0 * scale,
                    y_distance + y_origin - 23 * scale,
                    x_distance + x_origin + 10 * scale,
                    y_distance + y_origin - 23 * scale,
                    x_distance + x_origin + 5 * scale,
                    y_distance + y_origin - 28 * scale,
                    fill="#404040",
                    outline="#404040",
                    tags=(element_id, interactive_tag, outline_tag),
                )
                params["tags"].append(arrow_head_id)

            self.current_dict_circuit[element_id] = params

            print("coord : " + str(coord[0][0]) + "," + str(coord[0][1]))

            self.canvas.tag_bind(
                interactive_tag, "<Button-1>", lambda event, pin_id=element_id: self.on_pin_io_click(event, pin_id)
            )
            self.canvas.tag_bind(
                interactive_tag, "<B1-Motion>", lambda event, pin_id=element_id: self.on_pin_io_drag(event, pin_id)
            )
            self.canvas.tag_bind(
                interactive_tag,
                "<ButtonRelease-1>",
                lambda event, pin_id=element_id: self.on_pin_io_release(event, pin_id),
            )

        matrix[f"{coord[0][0]},{coord[0][1]}"]["state"] = USED

        return x_distance, y_distance

    def clear_board(self):
        """Clear the board of all drawn components."""
        for item in self.current_dict_circuit.values():
            if "tags" not in item:
                continue
            for tag in item["tags"]:
                self.canvas.delete(tag)
        for key in self.id_type:
            self.id_type[key] = 0
        self.current_dict_circuit.clear()
        # TODO Khalid update the Circuit instance
