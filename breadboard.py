"""
This module provides a Breadboard class for circuit design using the Tkinter Canvas and PIL libraries.
It includes methods for mouse tracking, canvas area capture, text-to-image conversion, and matrix filling 
for breadboards with 830 and 1260 points. Additionally, it provides a method for generating circuit layouts 
on the canvas.
Classes:
    Breadboard: A class to represent a breadboard for circuit design.
Attributes:
    canvas (Canvas): The canvas on which the breadboard is drawn.
    img_save (list): A list to save images.
    id_origin (dict): A dictionary to store the origin coordinates.
    current_cursor (None): The current cursor state.
    cursor_save (None): The saved cursor state.
    base_dict_circuit (dict): The base dictionary for the circuit.
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
    capture_canvas_area(x1, y1, x2, y2): Captures a specified area of the canvas.
    text_to_img(text, angle=90, font_path="FiraCode-Light", font_size=15, color=(0, 0, 0, 255), size=(15, 15)):
    fill_matrix_830_pts(col_distance=1, line_distance=1, **kwargs): Fills the breadboard matrix with 830 points.
    fill_matrix_1260_pts(): Fills the breadboard matrix with 1260 points.
    circuit(x_distance=0, y_distance=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
"""

from tkinter import Canvas
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageGrab

from dataCDLT import matrix830pts, matrix1260pts, base_dict_circuit, ICO_PDF, VERTICAL, HORIZONTAL, PERSO, FREE
from dataComponent import line_distribution


class Breadboard:
    """
    A class to represent a breadboard for circuit design.
    Attributes
    ----------
    canvas : Canvas
        The canvas on which the breadboard is drawn.
    img_save : list
        A list to save images.
    id_origin : dict
        A dictionary to store the origin coordinates.
    current_cursor : None
        The current cursor state.
    cursor_save : None
        The saved cursor state.
    base_dict_circuit : dict
        The base dictionary for the circuit.
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
    captureCanvasArea(x1, y1, x2, y2):
        Captures a specified area of the canvas.
    text2Img(text, angle=90, fontPath="FiraCode-Light", fontSize=15, color=(0, 0, 0, 255), size=(15, 15)):
        Converts text to an image with specified properties.
    fill_matrix_830_pts(colD=1, lineD=1, **kwargs):
        Fills the breadboard matrix with 830 points.
    fill_matrix_1260_pts(colD=1, lineD=1, **kwargs):
        Fills the breadboard matrix with 1260 points.
    circuit(xD=0, yD=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
        Draws a circuit on the breadboard based on the given model.
    """

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.img_save = []
        self.id_origin = {"xyOrigin": (0, 0)}
        self.current_cursor = None
        self.cursor_save = None
        self.base_dict_circuit = {}
        self.id_type = {}
        self.current_dict_circuit = base_dict_circuit
        self.num_id = 1
        self.mouse_x, self.mouse_y = 0, 0
        self.drag_mouse_x, self.drag_mouse_y = 0, 0
        self.id_type.update(
            {"dip14": 0, "74HC00": 0, "74HC02": 0, "74HC08": 0, "74HC04": 0, "74HC32": 0, "id_circuit": 0}
        )

        self.canvas.config(cursor="")

        self.image = Image.open(ICO_PDF["path"])

        self.image_ico_pdf = ImageTk.PhotoImage(self.image.resize((32, 32)))
        canvas.bind("<Motion>", self.follow_mouse)

    def follow_mouse(self, event):
        """
        Updates the mouse coordinates based on the given event.
        Args:
            event: An event object that contains the current mouse position.
        """
        self.mouse_x, self.mouse_y = event.x, event.y

    def capture_canvas_area(self, x1, y1, x2, y2):
        """
        Capture a specified area of the canvas and return it as an image.
        This method converts the given canvas coordinates to screen coordinates
        and captures the specified area directly from the screen.
        Args:
            x1 (int): The x-coordinate of the top-left corner of the area to capture.
            y1 (int): The y-coordinate of the top-left corner of the area to capture.
            x2 (int): The x-coordinate of the bottom-right corner of the area to capture.
            y2 (int): The y-coordinate of the bottom-right corner of the area to capture.
        Returns:
            Image: An image object representing the captured area.
        """

        # Convertir les coordonnées canvas en coordonnées de l'écran
        x1 = self.canvas.winfo_rootx() + x1
        y1 = self.canvas.winfo_rooty() + y1
        x2 = self.canvas.winfo_rootx() + x2
        y2 = self.canvas.winfo_rooty() + y2

        # Capturer la zone spécifiée directement à partir de l'écran
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        return image

    def text_to_img(
        self, text, angle=90, font_path="FiraCode-Light", font_size=15, color=(0, 0, 0, 255), size=(15, 15)
    ):
        """
        Converts a given text to an image with specified properties and rotates it.
        Args:
            text (str): The text to be converted into an image.
            angle (int, optional): The angle to rotate the image. Default is 90 degrees.
            font_path (str, optional): The path to the font file to be used. Default is "FiraCode-Light".
            font_size (int, optional): The size of the font. Default is 15.
            color (tuple, optional): The color of the text in RGBA format. Default is (0, 0, 0, 255).
            size (tuple, optional): The size of the image in pixels (width, height). Default is (15, 15).
        Returns:
            ImageTk.PhotoImage: The resulting image with the text, rotated by the specified angle.
        """

        police = ImageFont.truetype(font_path, font_size)

        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=police, fill=color)

        image_rotation = image.rotate(angle, expand=1)

        return ImageTk.PhotoImage(image_rotation)

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
            idph = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(1 + line_distance)
            idpb = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(13 + line_distance)
            idmh = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(line_distance)
            idmb = str(2 + (i % 5) + col_distance + (i // 5) * 6) + "," + str(12 + line_distance)
            matrix[idmh] = {
                "id": ["ph", "plus haut", "1"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (1.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "etat": FREE,
                "lien": None,
            }
            matrix[idph] = {
                "id": ["mh", "moins haut", "2"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (2.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "etat": FREE,
                "lien": None,
            }
            matrix[idmb] = {
                "id": ["pb", "plus bas", "13"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (19.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
                "etat": FREE,
                "lien": None,
            }
            matrix[idpb] = {
                "id": ["mb", "moins bas", "14"],
                "xy": (
                    0.5 * inter_space + (2 + (i % 5) + col_distance + (i // 5) * 6) * inter_space,
                    (20.5 + 22.2 * (line_distance // 15)) * inter_space,
                ),
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

        model = line_distribution
        for key, value in kwargs.items():
            if key == "model":
                model = value
            if key == "dXY":
                _, delta_y = value

        x, y = x_distance, y_distance
        for element in model:
            if callable(element[0]) and isinstance(element[1], int):
                for _ in range(element[1]):
                    if len(element) == 3:
                        (x, y) = element[0](self.canvas, x, y, scale, width, **element[2])
                    else:
                        (x, y) = element[0](self.canvas, x, y, scale, width)
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
