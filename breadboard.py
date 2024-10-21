"""
This module provides a Breadboard class for circuit design using the Tkinter Canvas library.
It includes methods for mouse tracking, and matrix filling 
for breadboards with 830 and 1260 points. Additionally, it provides a method for generating circuit layouts 
on the canvas.
Classes:
    Breadboard: A class to represent a breadboard for circuit design.
Attributes:
    canvas (Canvas): The canvas on which the breadboard is drawn.
    id_origin (dict): A dictionary to store the origin coordinates.
    current_cursor (None): The current cursor state.
    cursor_save (None): The saved cursor state.
    id_type (dict): A dictionary to store the types of components.
    current_dict_circuit (dict): The current dictionary for the circuit.
    num_id (int): The current ID number.
    mouse_x (int): The current x-coordinate of the mouse.
    mouse_y (int): The current y-coordinate of the mouse.
    drag_mouse_x (int): The x-coordinate of the mouse during drag.
    drag_mouse_y (int): The y-coordinate of the mouse during drag.
    matrix (dict): The matrix representing the breadboard.
Methods:
    follow_mouse(event): Updates the mouse coordinates based on the event.
    fill_matrix_830_pts(col_distance=1, line_distance=1, **kwargs): Fills the breadboard matrix with 830 points.
    fill_matrix_1260_pts(): Fills the breadboard matrix with 1260 points.
    circuit(x_distance=0, y_distance=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
"""

from tkinter import Canvas


from component_sketch import ComponentSketcher
from dataCDLT import matrix830pts, matrix1260pts, VERTICAL, HORIZONTAL, FREE
from dataComponent import ComponentData


class Breadboard:
    """
    A class to represent a breadboard for circuit design.
    Attributes
    ----------
    canvas : Canvas
        The canvas on which the breadboard is drawn.
    id_origin : dict
        A dictionary to store the origin coordinates.
    current_cursor : None
        The current cursor state.
    cursor_save : None
        The saved cursor state.
    id_type : dict
        A dictionary to store the types of components.
    current_dict_circuit : dict
        The current dictionary for the circuit.
    num_id : int
        The current ID number.
    mouse_x : int
        The current x-coordinate of the mouse.
    mouse_y : int
        The current y-coordinate of the mouse.
    drag_mouse_x : int
        The x-coordinate of the mouse during drag.
    drag_mouse_y : int
        The y-coordinate of the mouse during drag.
    matrix : dict
        The matrix representing the breadboard.
    Methods
    -------
    follow_mouse(event):
        Updates the mouse coordinates based on the event.
    fill_matrix_830_pts(colD=1, lineD=1, **kwargs):
        Fills the breadboard matrix with 830 points.
    fill_matrix_1260_pts(colD=1, lineD=1, **kwargs):
        Fills the breadboard matrix with 1260 points.
    circuit(xD=0, yD=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
        Draws a circuit on the breadboard based on the given model.
    """

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.current_cursor = None
        self.cursor_save = None
        self.id_type = {}
        self.current_dict_circuit = {}
        self.num_id = 1
        self.mouse_x, self.mouse_y = 0, 0
        self.drag_mouse_x, self.drag_mouse_y = 0, 0
        self.id_type.update(
            {"DIP14": 0, "74HC00": 0, "74HC02": 0, "74HC08": 0, "74HC04": 0, "74HC32": 0, "id_circuit": 0}
        )

        self.canvas.config(cursor="")

        canvas.bind("<Motion>", self.follow_mouse)
        self.sketcher = ComponentSketcher(canvas)

    def follow_mouse(self, event):
        """
        Updates the mouse coordinates based on the given event.
        Args:
            event: An event object that contains the current mouse position.
        """
        self.mouse_x, self.mouse_y = event.x, event.y

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

        matrix = matrix830pts
        for key, value in kwargs.items():
            if key == "matrix":
                matrix = value

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
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 1),
                "etat": FREE,
                "lien": None,
                
            }
            matrix[id_top_plus] = {
                "id": ["mh", "moins haut", "2"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (2.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 2),
                "etat": FREE,
                "lien": None,
            }
            matrix[id_bot_minus] = {
                "id": ["pb", "plus bas", "13"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (19.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 13),
                "etat": FREE,
                "lien": None,
            }
            matrix[id_bot_plus] = {
                "id": ["mb", "moins bas", "14"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (20.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "coord": (2 + (i % 5) + col_distance + (i // 5) * 6, 14),
                "etat": FREE,
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
                    "etat": FREE,
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
                    "etat": FREE,
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

    def calculate_center_y(self, line_distance, inter_space):
        # The center line between 'e' and 'f' is at line 7.5
        
        center_line = line_distance + 10.5
        center_y = center_line * inter_space
        return center_y

    
    def draw_matrix_points(self, scale=1): # used to debug the matrix
        """
        Draw all points in the matrix on the canvas, center snap points in yellow, others in orange.
        """
        for id_in_matrix, point in matrix1260pts.items():
            x, y = point["xy"]
            # Adjust for scaling
            x *= scale
            y *= scale
            # Determine color
            if id_in_matrix.startswith('snap,'):
                color = 'yellow'
            else:
                color = 'orange'
            # Draw a small circle at (x, y) with the specified color
            radius = 2 * scale  # Adjust size as needed
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=color, outline='')
