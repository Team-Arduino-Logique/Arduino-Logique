"""
breadboard.py
This module provides a Breadboard class for circuit design using the Tkinter Canvas library.
It includes methods for mouse tracking, and matrix filling 
for breadboards with 830 and 1260 points. Additionally, it provides a method for generating circuit layouts 
on the canvas.
"""

from tkinter import Canvas

from component_sketch import ComponentSketcher
from dataCDLT import (
    FREE,
    HORIZONTAL,
    PERSO,
    VERTICAL,
    USED,
)


class Breadboard:
    """
    A class to represent a breadboard for circuit design.
    Attributes
    ----------
    canvas : Canvas
        The canvas on which the breadboard is drawn.
    sketcher : ComponentSketcher
        The ComponentSketcher instance used to draw the circuit.
    """

    def __init__(self, canvas: Canvas, sketcher: ComponentSketcher):
        self.canvas = canvas
        self.sketcher = sketcher
        self.canvas.config(cursor="")

    def fill_matrix_830_pts(self, col_distance=1, line_distance=1):
        """
        Fills a matrix representing an 830-point breadboard with initial values.
        This method populates the matrix with coordinates and states for each point on the breadboard.
        The breadboard is divided into sections, and each point is assigned an ID, coordinates, state,
        and link information.
        Args:
            col_distance (int, optional): The distance between columns. Defaults to 1.
            line_distance (int, optional): The distance between lines. Defaults to 1.
        Returns:
            None
        """

        inter_space = 15

        matrix = self.sketcher.matrix

        for i in range(50):
            id_top_plus = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(1 + line_distance)
            id_bot_plus = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(13 + line_distance)
            id_top_minus = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(line_distance)
            id_bot_minus = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(12 + line_distance)
            matrix[id_top_minus] = {
                "id": ["ph", "plus haut", "1"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (1.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, line_distance),
                "state": FREE,
                "link": [(2 + col_distance,  line_distance, 60 + col_distance, line_distance)],
            }
            matrix[id_top_plus] = {
                "id": ["mh", "moins haut", "2"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (2.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 1 + line_distance),
                "state": FREE,
                "link": [(2 + col_distance, 1 + line_distance, 60 + col_distance, 1 + line_distance)],
            }
            matrix[id_bot_minus] = {
                "id": ["pb", "plus bas", "13"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (19.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 12 + line_distance),
                "state": FREE,
                "link": [(2 + col_distance, 12 + line_distance, 60 + col_distance, 12 + line_distance)],
            }
            matrix[id_bot_plus] = {
                "id": ["mb", "moins bas", "14"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (20.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 13 + line_distance),
                "state": FREE,
                "link": [(2 + col_distance, 13 + line_distance, 60 + col_distance, 13 + line_distance)],
            }
        for l in range(5):
            for c in range(63):
                id_in_matrix = str(c + col_distance) + "," + str(l + 2 + line_distance)
                matrix[id_in_matrix] = {
                    "id": [id_in_matrix, str(l + 2 + line_distance)],
                    "xy": (
                        0.5 * inter_space + (c + col_distance) * inter_space,
                        (5.5 + l + 22.2 * (line_distance // 15)) * inter_space,
                    ),
                    "coord": (c + col_distance, l + 2 + line_distance),
                    "state": FREE,
                    "link": [(c + col_distance, 2 + line_distance, c + col_distance, 6 + line_distance)],
                }
                id_in_matrix = str(c + col_distance) + "," + str(l + 7 + line_distance)
                matrix[id_in_matrix] = {
                    "id": [id_in_matrix, str(l + 7 + line_distance)],
                    "xy": (
                        0.5 * inter_space + (c + col_distance) * inter_space,
                        (12.5 + l + 22.2 * (line_distance // 15)) * inter_space,
                    ),
                    "coord": (c + col_distance, l + 7 + line_distance),
                    "state": FREE,
                    "link": [(c + col_distance, 7 + line_distance, c + col_distance, 11 + line_distance)],
                }

    def fill_matrix_1260_pts(self):
        """
        Fills a 1260-point matrix by calling the fill_matrix_830_pts method twice.
        The first call to fill_matrix_830_pts fills the matrix with default parameters.
        The second call fills the matrix with a specified line distance of 15.
        Parameters:
        None
        Returns:
        None
        """

        self.fill_matrix_830_pts()
        self.fill_matrix_830_pts(line_distance=15)

    def draw_matrix_points(self, scale=1):  # used to debug the matrix
        """
        Draw all points in the matrix on the canvas, center snap points in yellow, others in orange.
        """
        for id_in_matrix, point in self.sketcher.matrix.items():
            x, y = point["xy"]

            # Adjust for the origin
            x += self.sketcher.id_origins["xyOrigin"][0]
            y += self.sketcher.id_origins["xyOrigin"][1]
            # Adjust for scaling
            x *= scale
            y *= scale
            # Determine color
            if id_in_matrix.startswith("snap,"):
                color = "yellow"
            else:
                color = "orange"
            # Draw a small circle at (x, y) with the specified color
            radius = 2 * scale  # Adjust size as needed
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="")

    def draw_blank_board_model(self, x_origin: int = 50, y_origin: int = 10, battery_pos_wire_end=None, battery_neg_wire_end=None):
        """
        Draws a blank breadboard model on the canvas.
        """
        line_distribution = [(self.sketcher.draw_hole, 63)]
        power_block = [(self.sketcher.draw_hole, 5), (self.sketcher.draw_blank, 1)]
        neg_power_rail = [
            (self.sketcher.draw_blank, 1),
            (self.sketcher.draw_char, 1, {"deltaY": 1.3, "scaleChar": 2}),
            (self.sketcher.draw_rail, 60),
            (self.sketcher.draw_half_blank, 1),
            (self.sketcher.draw_blank, 1),
            (self.sketcher.draw_char, 1, {"deltaY": 1.3, "scaleChar": 2}),
        ]
        pos_power_rail = [
            (self.sketcher.draw_blank, 1),
            (self.sketcher.draw_char, 1, {"color": "#ff0000", "text": "+", "deltaY": -0.6, "scaleChar": 2}),
            (self.sketcher.draw_red_rail, 60),
            (self.sketcher.draw_blank, 1),
            (self.sketcher.draw_half_blank, 1),
            (self.sketcher.draw_char, 1, {"color": "#ff0000", "text": "+", "deltaY": -0.6, "scaleChar": 2}),
        ]
        power_line = [(self.sketcher.draw_blank, 3), (power_block, 10, {"direction": HORIZONTAL})]
        power_strip = [
            (neg_power_rail, 1, {"direction": VERTICAL}),
            (power_line, 2, {"direction": VERTICAL}),
            (pos_power_rail, 1, {"direction": VERTICAL}),
        ]
        strip_distribution = [(line_distribution, 5, {"direction": VERTICAL})]
        numbering = [
            (self.sketcher.draw_blank, 1),
            (self.sketcher.draw_num_iter, 1, {"beginNum": 1, "endNum": 63, "direction": HORIZONTAL, "deltaY": -1.5}),
        ]

        board830pts = [
            (self.sketcher.set_xy_origin, 1, {"id_origin": "bboard830"}),
            (self.sketcher.draw_board, 1),
            (self.sketcher.draw_half_blank, 1, {"direction": HORIZONTAL}),
            (self.sketcher.draw_half_blank, 1, {"direction": VERTICAL}),
            (power_strip, 1, {"direction": VERTICAL}),
            (numbering, 1, {"direction": VERTICAL}),
            (self.sketcher.go_xy, 1, {"line": 5.5, "column": 0.5, "id_origin": "bboard830"}),
            (self.sketcher.draw_char_iter, 1, {"beginChar": "f", "numChars": 5, "anchor": "center", "deltaY": 0.7}),
            (strip_distribution, 1, {"direction": VERTICAL}),
            (self.sketcher.go_xy, 1, {"line": 5.5, "column": 64.5, "id_origin": "bboard830"}),
            (self.sketcher.draw_half_blank, 1),
            (self.sketcher.draw_char_iter, 1, {"beginChar": "f", "numChars": 5, "direction": VERTICAL, "deltaY": 0.7}),
            (self.sketcher.go_xy, 1, {"line": 12.5, "column": 0.5, "id_origin": "bboard830"}),
            (self.sketcher.draw_char_iter, 1, {"beginChar": "a", "numChars": 5, "deltaY": 0.7}),
            (strip_distribution, 1, {"direction": VERTICAL}),
            (self.sketcher.go_xy, 1, {"line": 12.5, "column": 64.5, "id_origin": "bboard830"}),
            (self.sketcher.draw_half_blank, 1),
            (self.sketcher.draw_char_iter, 1, {"beginChar": "a", "numChars": 5, "direction": VERTICAL, "deltaY": 0.7}),
            (self.sketcher.go_xy, 1, {"line": 18.8, "column": 0.5, "id_origin": "bboard830"}),
            (numbering, 1, {"direction": VERTICAL}),
            (self.sketcher.go_xy, 1, {"line": 18.5, "column": 0.5, "id_origin": "bboard830"}),
            (power_strip, 1, {"direction": VERTICAL}),
        ]

        board1260pts = [(board830pts, 2, {"direction": PERSO, "dXY": (0, 1.3)})]
        blank_board_model = [
            (self.sketcher.set_xy_origin, 1, {"id_origin": "circTest"}),
            (board1260pts, 1),
            (self.sketcher.go_xy, 1, {"line": 10.1, "column": 1.4, "id_origin": "circTest"}),
            (self.sketcher.go_xy, 1, {"line": 0, "column": 0, "id_origin": "circTest"}),
        ]
        self.sketcher.circuit(x_origin, y_origin, scale=self.sketcher.scale_factor, model=blank_board_model)

        battery_x = x_origin + 1200  # Adjust as needed for proper positioning
        battery_y = y_origin + 300   # Adjust as needed for proper positioning

        # Reset all matrix elements' states to FREE
        for key in self.sketcher.matrix:
            self.sketcher.matrix[key]['state'] = FREE

        self.sketcher.draw_battery(
            battery_x,
            battery_y,
            pos_wire_end=battery_pos_wire_end,
            neg_wire_end=battery_neg_wire_end,
        )
        if battery_pos_wire_end:
            allowed_positions = self.sketcher.get_power_line_last_pins()
            nearest_point, nearest_point_coord = self.sketcher.find_nearest_allowed_grid_point(battery_pos_wire_end[0], battery_pos_wire_end[1], allowed_positions)
            col, line = nearest_point_coord
            self.sketcher.matrix[f'{col},{line}']['state'] = USED

        