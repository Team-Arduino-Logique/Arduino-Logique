"""
This module provides a Breadboard class for circuit design using the Tkinter Canvas library.
It includes methods for mouse tracking, and matrix filling 
for breadboards with 830 and 1260 points. Additionally, it provides a method for generating circuit layouts 
on the canvas.
"""

from tkinter import Canvas

from dataCDLT import (
    matrix830pts,
    matrix1260pts,
    FREE,
    id_origins,
)


class Breadboard:
    """
    A class to represent a breadboard for circuit design.
    Attributes
    ----------
    canvas : Canvas
        The canvas on which the breadboard is drawn.
    id_origin : dict
        A dictionary to store the origin coordinates.
    matrix : dict
        The matrix representing the breadboard.
    """

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.selector()
        self.canvas.config(cursor="")
        canvas.bind("<Motion>", self.follow_mouse)

    def follow_mouse(self, event):
        """
        Updates the mouse coordinates based on the given event.
        Args:
            event: An event object that contains the current mouse position.
        """
        # FIXME fixing the coords crashes the app
        self.canvas.coords("selector_cable", [event.x - 10, event.y - 10, event.x + 0, event.y + 0])

    def selector(self):
        """
        Create the round selector cable movement
        """
        self.canvas.create_oval(
            100,
            100,
            110,
            110,
            fill="#dfdfdf",
            outline="#404040",
            width=1,
            tags=("selector_cable"),
        )
        self.canvas.itemconfig("selector_cable", state="hidden")

    def fill_matrix_830_pts(self, col_distance=1, line_distance=1, **kwargs):
        """
        Fills a matrix representing an 830-point breadboard with initial values.
        This method populates the matrix with coordinates and states for each point on the breadboard.
        The breadboard is divided into sections, and each point is assigned an ID, coordinates, state,
        and link information.
        Args:
            col_distance (int, optional): The distance between columns. Defaults to 1.
            line_distance (int, optional): The distance between lines. Defaults to 1.
            **kwargs: Additional keyword arguments. If 'matrix' is provided in kwargs, it will be used
                      as the matrix to be filled. Otherwise, the default matrix830pts will be used.
        Keyword Args:
            matrix (dict): A dictionary representing the matrix to be filled. If not provided,
                           matrix830pts is used.
        Returns:
            None
        """

        inter_space = 15

        matrix = kwargs.get("matrix", matrix830pts)

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
                "lien": None,
            }
            matrix[id_top_plus] = {
                "id": ["mh", "moins haut", "2"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (2.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 1 + line_distance),
                "state": FREE,
                "lien": None,
            }
            matrix[id_bot_minus] = {
                "id": ["pb", "plus bas", "13"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (19.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 12 + line_distance),
                "state": FREE,
                "lien": None,
            }
            matrix[id_bot_plus] = {
                "id": ["mb", "moins bas", "14"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (20.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 13 + line_distance),
                "state": FREE,
                "lien": None,
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
                    "lien": None,
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
                    "lien": None,
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

        self.fill_matrix_830_pts(matrix=matrix1260pts)
        self.fill_matrix_830_pts(line_distance=15, matrix=matrix1260pts)

    def draw_matrix_points(self, scale=1):  # used to debug the matrix
        """
        Draw all points in the matrix on the canvas, center snap points in yellow, others in orange.
        """
        for id_in_matrix, point in matrix1260pts.items():
            x, y = point["xy"]

            # Adjust for the origin
            x += id_origins["xyOrigin"][0]
            y += id_origins["xyOrigin"][1]
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
