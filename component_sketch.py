import tkinter as tk
from tkinter import font
import math


from dataCDLT import (
    HORIZONTAL,
    RIGHT,
    VERTICAL,
    VERTICAL_END_HORIZONTAL,
    LEFT,
    PERSO,
    YES,
    NO,
    AUTO,
    id_origins,
    current_dict_circuit,
    id_type,
    num_id,
    matrix1260pts,
    matrix830pts,
    drag_mouse_x,
    drag_mouse_y,
    selector_dx_ul, 
    selector_dy_ul,
    selector_dx_br, 
    selector_dy_br,
    FREE,
    USED,
)
from component_params import BOARD_830_PTS_PARAMS, DIP14_PARAMS

class ComponentSketcher:
    def __init__(self, canvas):
        self.canvas = canvas
        self.funcHole = {"function": self.drawSquareHole}
        self.scale_factor = 1.0
        self.drag_selector = False
        self.nearest_multipoint = -1
        

        self.drag_chip_data = {
            "chip_id": None,
            "x": 0,
            "y": 0
        }

        self.wire_drag_data = {
            "wire_id": None,
            "endpoint": None,
            "x": 0,
            "y": 0
        }
        


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

        # component_data = ComponentData(self.sketcher)
        Hole = [(self.drawHole, 1)] #model specified by default in case of no model

        model = Hole
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

    def on_wire_endpoint_click(self, event, wire_id, endpoint):
        """
        Event handler for when a wire endpoint is clicked.
        """
        self.wire_drag_data["wire_id"] = wire_id
        self.wire_drag_data["endpoint"] = endpoint

        endpoint_tag = current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
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

            color = current_dict_circuit[wire_id]["color"] 
            coords = current_dict_circuit[wire_id]["coord"]
            multipoints = current_dict_circuit[wire_id]["multipoints"]
            x_o , y_o = id_origins["xyOrigin"]
            (xn,yn), (cn,ln) = self.find_nearest_grid_wire(canvas_x, canvas_y, matrix=matrix1260pts)
            if endpoint == "start":
                coords = [(cn, ln, coords[0][2], coords[0][3])]
            else:
                coords = [(coords[0][0], coords[0][1], cn, ln)]
            
            model_wire = [(self.drawWire, 1, {"id": wire_id,"color":color, "coord": coords,"multipoints":multipoints,
                                               "matrix": matrix1260pts})]
            self.circuit(x_o , y_o , model = model_wire)


    def on_wire_endpoint_release(self, event, wire_id, endpoint):
        """
        Event handler for when a wire endpoint is released.
        """
        if self.wire_drag_data["wire_id"] == wire_id and self.wire_drag_data["endpoint"] == endpoint:
            # Reset drag data
            self.wire_drag_data["wire_id"] = None
            self.wire_drag_data["endpoint"] = None

            # Snap to nearest grid point
####################    MODIF KH 25/10/2024  ##################################
            #self.snap_wire_endpoint_to_grid(event, wire_id, endpoint)
####################    FIN MODIF KH 25/10/2024  ##################################

            # Remove highlight
            endpoint_tag = current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
            self.canvas.itemconfig(endpoint_tag, outline="#404040", fill="#dfdfdf")
            self.drag_selector = False

    def update_wire_body(self, wire_id):
        """
        Updates the wire body based on the positions of the endpoints.
        """
        params = current_dict_circuit[wire_id]
        start_pos = self.canvas.coords(params["endpoints"]["start"]["tag"])
        end_pos = self.canvas.coords(params["endpoints"]["end"]["tag"])

        # Calculate center positions of the endpoints
        start_x = (start_pos[0] + start_pos[2]) / 2
        start_y = (start_pos[1] + start_pos[3]) / 2
        end_x = (end_pos[0] + end_pos[2]) / 2
        end_y = (end_pos[1] + end_pos[3]) / 2

        # Update wire body coordinates
        self.canvas.coords(
            params["wire_body_tag"],
            start_x, start_y,
            end_x, end_y
        )
        
    def snap_wire_endpoint_to_grid(self, event, wire_id, endpoint):
        """
        Snaps the wire endpoint to the nearest grid point, excluding central points.
        """
        # Get current position of the endpoint
        ############## MODIF KH 25/10/2024 #######################
        endpoint_tag = current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
        pos = self.canvas.coords(endpoint_tag)
        # x = (pos[0] + pos[2]) / 2
        # y = (pos[1] + pos[3]) / 2
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        adjusted_x = canvas_x - id_origins["xyOrigin"][0]
        adjusted_y = canvas_y - id_origins["xyOrigin"][1]

        dx = adjusted_x -  self.wire_drag_data["x"]
        dy = adjusted_y -  self.wire_drag_data["y"]


        # Find nearest grid point
        x_o , y_o = id_origins["xyOrigin"]
        #nearest_x, nearest_y = self.find_nearest_grid_point(x, y)
        
        coords = current_dict_circuit[wire_id]["coord"]
        XY = [current_dict_circuit[wire_id]["XY"] ]
        color = current_dict_circuit[wire_id]["color"] 
        if endpoint == "start":
            x =  canvas_x # pos[0] # + dx
            y =  canvas_y # pos[1] # + dy
            (real_x,real_y),(col,line) = self.find_nearest_grid_chip(x,y)
            coords = [(col, line, coords[0][2], coords[0][3])]
            # print(f"snap ({canvas_x},{canvas_y}) - ({x},{y})({self.wire_drag_data["x"]},{self.wire_drag_data["y"]}) - deb - col proche:{col} - ligne p: {line}")
        else:
            x = canvas_x # pos[2] # + dx
            y = canvas_y # pos[3] # + dy
            (real_x,real_y),(col,line) = self.find_nearest_grid_wire(x,y)
            coords = [(coords[0][0], coords[0][1], col, line)]
            # print(f"snap ({canvas_x},{canvas_y}) - ({x},{y})({self.wire_drag_data["x"]},{self.wire_drag_data["y"]}) - fin - col proche:{col} - ligne p: {line}")
        model_wire = [(self.drawWire, 1, {"id": wire_id,"color":color, "coord": coords, "XY":XY, "matrix": matrix1260pts})]
        self.circuit(x_o , y_o , model = model_wire)
        # Calculate movement delta
        #dx = nearest_x - x
        #dy = nearest_y - y

        # Move endpoint to the nearest grid point
        #self.canvas.move(endpoint_tag, dx, dy)

        # Update endpoint position in params
        #current_dict_circuit[wire_id]["endpoints"][endpoint]["position"] = (nearest_x, nearest_y)

        # Update the wire body
        #self.update_wire_body(wire_id)
        ############## FIN MODIF KH 25/10/2024 #######################

    def find_nearest_grid_point(self, x, y, matrix=None):
        """
        Finds the nearest grid point to (x, y).
        """
        if matrix is None:
            matrix = matrix1260pts

        min_distance = float('inf')
        nearest_point = (x, y)
        nearest_point_col_lin = (0, 0)
        for id_in_matrix, point in matrix.items():
            grid_x, grid_y = point["xy"]
            distance = math.hypot(x - grid_x - id_origins["xyOrigin"][0], y - grid_y - id_origins["xyOrigin"][1])
            if distance < min_distance:
                min_distance = distance
                nearest_point = (grid_x, grid_y)
                nearest_point_col_lin = point["coord"]

        return nearest_point, nearest_point_col_lin
    
    def find_nearest_multipoint(self, x,y,wire_id):
        nearest_point = -1
        multipoint = current_dict_circuit[wire_id]["multipoints"]
        [(xO, yO, xF, yF)] = current_dict_circuit[wire_id]["coord"]
        xO, yO = self.getXY(xO, yO, matrix=matrix1260pts)   
        xF, yF = self.getXY(xF, yF, matrix=matrix1260pts)  
        i = 0  
        while (nearest_point == -1 and i < len(multipoint) ):
            if math.hypot(x-multipoint[i], y - multipoint[i+1]) <= 15:
                nearest_point = i
            i+=2  
        insert_point = False  
        if nearest_point == -1:
            x1, y1 = xO, yO
            i = 0
            while (nearest_point == -1 and i<len(multipoint)):
                dx, dy = multipoint[i] - x1, multipoint[i+1] - y1
                t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
                proj_x = x1 + t * dx
                proj_y = y1 + t * dy
                dist_segment = math.hypot(x - proj_x, y - proj_y)
                if dist_segment <=10:
                    nearest_point = i
                # if x > min(x1-5,multipoint[i] - 5)  and x < max(multipoint[i]+5, x1 + 5):
                #     if y > min(y1-5, multipoint[i + 1] - 5) and y < max(multipoint[i + 1]+5, y1 + 5):
                        
                #         dx, dy = multipoint[i] - x1, multipoint[i+1] - y1
                #         if dx ==0 or dy == 0:
                #             nearest_point = i
                #         else:
                #              deltay = math.fabs( y - (y1 + (x - x1)*(dy/dx)) )
                #              if deltay <=5:
                #                 nearest_point = i
                x1, y1 = multipoint[i] , multipoint[i+1]
                i+=2
            if nearest_point == -1:
                nearest_point = len(multipoint)
            insert_point = True
        #multipoint.insert(nearest_point, x)    
        #multipoint.insert(nearest_point + 1, y)   
        current_dict_circuit[wire_id]["multipoints"] = multipoint
        return nearest_point , insert_point     

    def on_wire_body_enter(self,event, wire_id):
        if  not self.drag_selector:
            x, y = event.x, event.y
            color = current_dict_circuit[wire_id]["color"]
            encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"  
            self.canvas.itemconfig("selector_cable", fill=contour, outline = encre)      
            #self.canvas.coords("selector_cable", [x-10,y-10,x,y])
            self.canvas.itemconfig("selector_cable", state="normal")
            #self.canvas.tag_raise("selector_cable")
        
    def on_wire_body_leave(self, event, wire_id):
        if  not self.drag_selector:
            self.canvas.itemconfig("selector_cable", state="hidden")
            
    def on_wire_body_click(self,event, wire_id):
        self.wire_drag_data["wire_id"] = wire_id
        self.wire_drag_data["endpoint"] = "selector_cable"
        endpoint_tag = "selector_cable"
        x, y = event.x, event.y

        color = current_dict_circuit[wire_id]["color"]
        encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}" 
        x_o, y_o = id_origins["xyOrigin"]
        #endpoint_tag = current_dict_circuit[wire_id]["endpoints"][endpoint]["tag"]
        self.canvas.itemconfig(endpoint_tag, outline=contour, fill=encre)
        self.nearest_multipoint, insert_point = self.find_nearest_multipoint(x - x_o, y - y_o, wire_id)
        if insert_point:
            multipoints = current_dict_circuit[wire_id]["multipoints"]
            multipoints.insert(self.nearest_multipoint, x - x_o,)    
            multipoints.insert(self.nearest_multipoint + 1, y - y_o)  
            current_dict_circuit[wire_id]["multipoints"] = multipoints
                
    def on_wire_body_drag(self,event, wire_id):
        #self.wire_drag_data["wire_id"] = wire_id
        #self.wire_drag_data["endpoint"] = "selector_cable"
        endpoint_tag = "selector_cable"
        x_o, y_o = id_origins["xyOrigin"]
        x, y = event.x - x_o, event.y-y_o
        multipoints = current_dict_circuit[wire_id]["multipoints"]
        coords = current_dict_circuit[wire_id]["coord"]
        XY = [current_dict_circuit[wire_id]["XY"] ]
        color = current_dict_circuit[wire_id]["color"] 
        multipoints[self.nearest_multipoint] = x 
        multipoints[self.nearest_multipoint + 1] = y
        model_wire = [(self.drawWire, 1, {"id": wire_id,"multipoints":multipoints, "coord":coords,"color":color, "XY":XY,
                                               "matrix": matrix1260pts})]
        self.circuit(x_o , y_o , model = model_wire)        

            
    def on_wire_body_release(self, event, wire_id):
        self.wire_drag_data["wire_id"] = None
        self.wire_drag_data["endpoint"] = None    
        self.nearest_multipoint = -1
        self.canvas.itemconfig("selector_cable", state="hidden")

    def on_chip_click(self, event, chip_id):
        """
        Event handler for chip clicks.
        Initiates drag and stores the initial mouse position.
        """
        print(f"Chip clicked: {chip_id}")
        # Initiate drag by setting drag_chip_data
        self.drag_chip_data["chip_id"] = chip_id

        #Convert event coordinates to canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)


        

        # Adjust for scaling
        adjusted_x = canvas_x #/ self.scale_factor
        adjusted_y = canvas_y #/ self.scale_factor

        self.drag_chip_data["x"] = adjusted_x
        self.drag_chip_data["y"] = adjusted_y


        chip_params = current_dict_circuit[chip_id]
        self.drag_chip_data["initial_XY"] = chip_params["XY"]

        if "occupied_holes" in chip_params:
            # Store the previous occupied holes in case we need to restore them
            self.drag_chip_data["previous_occupied_holes"] = chip_params["occupied_holes"]
            for hole_id in chip_params["occupied_holes"]:
                matrix1260pts[hole_id]["etat"] = FREE
            chip_params["occupied_holes"] = []


        print(f"Chip {chip_id} clicked at ({adjusted_x}, {adjusted_y})")

        # # Correct tag name
        # tagSouris = "activeArea" + chip_id

        # # Change outline to indicate selection
        # self.canvas.itemconfig(tagSouris, outline="red")
        # self.canvas.tag_raise(tagSouris)
        # print(f"Chip {chip_id} outline changed to red")

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
            adjusted_x = canvas_x #/ self.scale_factor
            adjusted_y = canvas_y #/ self.scale_factor

            # Calculate movement delta
            dx = adjusted_x - self.drag_chip_data["x"]
            dy = adjusted_y - self.drag_chip_data["y"]

            # Move all items associated with the chip
            chip_params = current_dict_circuit[chip_id]
            # for tag in chip_params["tags"]:
            #     self.canvas.move(tag, dx, dy)

            # Update drag_chip_data
            self.drag_chip_data["x"] = adjusted_x
            self.drag_chip_data["y"] = adjusted_y

            # Update chip's position
            current_x, current_y = chip_params["XY"]
            # chip_params["XY"] = (current_x + dx, current_y + dy)

            model_chip = [(self.drawChip, 1, {"id": chip_id, "XY": (current_x + dx, current_y + dy)})]
            self.circuit(current_x + dx, current_y + dy,model=model_chip)

            print(f"Chip {chip_id} moved to new position: ({current_x}, {current_y})")

            # **Update chip's center position**
            # center_x, center_y = chip_params["center"]
            # chip_params["center"] = (center_x + dx, center_y + dy)

            # Update pin positions
            # for pin_info in chip_params["pins"]:
            #     pin_x, pin_y = pin_info['position']
            #     pin_info['position'] = (pin_x + dx, pin_y + dy)

    def on_stop_chip_drag(self, event):
        chip_id = self.drag_chip_data["chip_id"]
        if chip_id:
            # MODIF KH POUR DRAG-DROP 23/10/2024
            # (x, y) = current_dict_circuit[chip_id]["XY"]
            (x, y) = current_dict_circuit[chip_id]["pinUL_XY"]
            # FIN MODIF KH
            (real_x,real_y),(col,line) = self.find_nearest_grid_chip(x,y)
            print(f"Real x: {real_x}, Real y: {real_y}")
            print(f"Col: {col}, Line: {line}")

            # Get chip parameters
            chip_params = current_dict_circuit[chip_id]
            pin_count = chip_params["pinCount"]
            half_pin_count = pin_count // 2

            # Check if there's enough space to the right
            max_column = col + half_pin_count - 1
            if max_column > 63:
                # Not enough space, prevent placement and look for the nearest snap point on the left
                print("Not enough space to place the chip here.")
                col = 63 - half_pin_count + 1
                (x_o, y_o) = id_origins["xyOrigin"]
                real_x, real_y = self.getXY(col, line, matrix=matrix1260pts)
                real_x += x_o
                real_y += y_o
                (real_x,real_y),(col,line) = self.find_nearest_grid_chip(real_x,real_y)

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

                hole_top = matrix1260pts.get(hole_id_top)
                hole_bottom = matrix1260pts.get(hole_id_bottom)

                if hole_top["etat"] != FREE or hole_bottom["etat"] != FREE:
                    holes_available = False
                    break
                else:
                    occupied_holes.extend([hole_id_top, hole_id_bottom])

            if not holes_available:
                print("Holes are occupied. Cannot place the chip here.")
                # Re-mark the previous holes as used
                previous_occupied_holes = self.drag_chip_data.get("previous_occupied_holes", [])
                for hole_id in previous_occupied_holes:
                    matrix1260pts[hole_id]["etat"] = USED
                chip_params["occupied_holes"] = previous_occupied_holes
                

                real_x = previous_x
                real_y = previous_y
            else:
                # Mark new holes as used
                for hole_id in occupied_holes:
                    matrix1260pts[hole_id]["etat"] = USED
                chip_params["occupied_holes"] = occupied_holes

            

            

            # AJOUT KH DRAG-DROP 23/10/2024
            pin_x, pin_y = self.xy_chip2pin(real_x, real_y)
            # FIN AJOUT KH
            model_chip = [(self.drawChip, 1, {"id": chip_id, "XY": (real_x,real_y), "pinUL_XY":(pin_x, pin_y)})]
            self.circuit(real_x, real_y,model=model_chip)
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
        # Adjust x and y for the origin
        (x_o, y_o) = id_origins["xyOrigin"]
        col, line = self.getColLine(x, y, matrix=matrix1260pts)
        if line not in [7, 21]:
            return holes  # Chip not on correct lines
        for i in range(half_pin_count):
            hole_id_top = f"{col + i},{line}"
            hole_id_bottom = f"{col + i},{line + 1}"
            holes.extend([hole_id_top, hole_id_bottom])
        return holes

    # def find_nearest_snap_point(self, x, y, matrix):
    #     """
    #     Find the nearest snap point to the given x, y coordinates.

    #     Parameters:
    #         x (float): The x-coordinate.
    #         y (float): The y-coordinate.
    #         matrix (dict): The matrix containing snap points.

    #     Returns:
    #         tuple: (nearest_x, nearest_y) coordinates of the nearest snap point.
    #     """
    #     min_distance = float('inf')
    #     nearest_point = (x, y)
    #     for id_in_matrix, point in matrix.items():
    #         if id_in_matrix.startswith("snap,"):
    #             grid_x, grid_y = point["xy"]
    #             distance = math.hypot(x - grid_x, y - grid_y)
    #             print(f"Checking snap point {id_in_matrix} at ({grid_x}, {grid_y}), distance: {distance}")
    #             if distance < min_distance:
    #                 min_distance = distance
    #                 nearest_point = (grid_x, grid_y)
    #     print(f"Nearest snap point to ({x}, {y}) is at ({nearest_point[0]}, {nearest_point[1]})")
    #     return nearest_point

    
# AJOUT KH POUR DRAG_DROP 23/10/2024
    def xy_hole2chip(self,xH, yH, scale=1):
        space = 9*scale
        return (xH - 2*scale, yH + space)
    
    def xy_chip2pin(self,xC, yC, scale=1):
        space = 9*scale
        return (xC + 2*scale, yC - space)
# FIN AJOUT KH DRAG_DROP 23/10/2024        

    def find_nearest_grid_wire(self, x, y, matrix=None):
        """
        Find the nearest grid point to the given x, y coordinates on lines 6 or 21 ('f' lines).

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            matrix (dict, optional): The grid matrix to use. Defaults to matrix1260pts.

        Returns:
            tuple: (nearest_x, nearest_y) coordinates of the nearest grid point.
        """
        if matrix is None:
            matrix = matrix1260pts

        min_distance = float('inf')

        (x_o, y_o) = id_origins["xyOrigin"]
        
        nearest_point = (0, 0)
        nearest_point_col_lin = (0, 0)
        for point in matrix.items():
            
            # Consider only lines 6 and 21 ('f' lines)
            # if line_num == 7 or line_num == 22:
            if point[1]["etat"]== FREE:
                grid_x, grid_y = point[1]["xy"]
                # MODIF KH DRAG-DROP 23/10/2024
                # distance = math.hypot(x - grid_x , y - grid_y)
                distance = math.hypot(x - grid_x - x_o, y - grid_y - y_o)
                # FIN MODIF KH
                if distance < min_distance:
                    
                    min_distance = distance
                    # MODIF KH DRAG_DROP 23/10/2024
                    # nearest_point = (grid_x, grid_y)
                    nearest_point = self.xy_hole2chip(grid_x + x_o, grid_y + y_o)
                    # FIN MODIF KH
                    nearest_point_col_lin = point[1]["coord"]

        return nearest_point, nearest_point_col_lin

    def find_nearest_grid_chip(self, x, y, matrix=matrix1260pts):
        """
        Find the nearest grid point to the given x, y coordinates on lines 6 or 21 ('f' lines).

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            matrix (dict, optional): The grid matrix to use. Defaults to matrix1260pts.

        Returns:
            tuple: (nearest_x, nearest_y) coordinates of the nearest grid point.
        """
        if matrix is None:
            matrix = matrix1260pts

        min_distance = float('inf')

        (x_o, y_o) = id_origins["xyOrigin"]
        
        nearest_point = (0, 0)
        nearest_point_col_lin = (0, 0)
        for point in matrix.items():
            
            # Consider only lines 7 and 21 ('f' lines)
            col, line = point[1]["coord"]
            if line == 7 or line == 21:
                # mettre is_XY_free4Chip(x,y)
                
                grid_x, grid_y = point[1]["xy"]
                    
                # MODIF KH DRAG-DROP 23/10/2024
                # distance = math.hypot(x - grid_x , y - grid_y)
                distance = math.hypot(x - grid_x - x_o, y - grid_y - y_o)
                # FIN MODIF KH
                if distance < min_distance:
                        
                    min_distance = distance
                    # MODIF KH DRAG_DROP 23/10/2024
                    # nearest_point = (grid_x, grid_y)
                    nearest_point = self.xy_hole2chip(grid_x + x_o, grid_y + y_o)
                    # FIN MODIF KH
                    nearest_point_col_lin = point[1]["coord"]

        return nearest_point, nearest_point_col_lin

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
        tag = ""
        for key, value in kwargs.items():
            if key == "tags":
                tag = value
            if key == "fill":
                fill = value
            if key == "thickness":
                thickness = value

        # Draw four arcs for corners
        self.canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, style=tk.PIESLICE, **kwargs)
        self.canvas.create_arc(x2 - 2 * radius, y, x2, y + 2 * radius, start=0, extent=90, style=tk.PIESLICE, **kwargs)
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs)
        self.canvas.create_arc(x, y2 - 2 * radius, x + 2 * radius, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs)
        # kwargs["outline"] = fill
        self.canvas.create_polygon(points, smooth=False, **kwargs)
        self.canvas.create_line(x + radius, y, x, y + radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x2 - radius, y, x2, y + radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x2 - radius, y2, x2, y2 - radius, fill=fill, width=thickness, tags=tag)
        self.canvas.create_line(x, y2 - radius, x + radius, y2, fill=fill, width=thickness, tags=tag)


    def setXYOrigin(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        xO, yO = xD, yD
        id_origin = "xyOrigin"
        for key, value in kwargs.items():
            if key == "id_origin":
                id_origin = value
            # if key == "xyOrigin": xO, yO       = value

        id_origins[id_origin] = (xD, yD)
        
        return (xO, yO)


    def goXY(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        id_origin = "xyOrigin"
        for key, value in kwargs.items():
            if key == "line":
                line = value
            if key == "column":
                column = value
            if key == "id_origin":
                id_origin = value

        xO, yO = id_origins[id_origin]

        return (xO + column * 15 * scale, yO + line * 15 * scale)


    def drawChar(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        angle = 90
        for key, value in kwargs.items():
            if key == "angle":
                angle = value
        color = "#000000"
        text = "-"
        deltaY = 0
        scaleChar = 1
        size = (int(inter_space * 1), int(inter_space * 1))
        anchor = "center"
        tags = ""
        for key, value in kwargs.items():
            if key == "color":
                color = value
            elif key == "text":
                text = value
            elif key == "deltaY":
                deltaY = value
            elif key == "scaleChar":
                scaleChar = value
            elif key == "anchor":
                anchor = value
            elif key == "tags":
                tags = value

        size = (int(scaleChar * inter_space * len(text)), int(scaleChar * inter_space))
        firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=int(15 * scale * scaleChar))
        if angle != 0:
            firaCodeFont = font.Font(family="FiraCode-Light", size=int(15 * scaleChar * scale))
            self.canvas.create_text(
                xD, yD + deltaY * space, text=text, font=firaCodeFont, fill=color, anchor=anchor, angle=angle, tags=tags
            )
        else:
            self.canvas.create_text(xD, yD, text=text, font=firaCodeFont, fill=color, anchor=anchor, tags=tags)

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawCharIter(self, xD, yD, scale=1, width=-1, direction=VERTICAL_END_HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale

        for key, value in kwargs.items():
            if key == "beginChar":
                beginChar = value
            elif key == "numChars":
                numChars = value

        x = xD
        y = yD
        s = direction
        if direction == VERTICAL_END_HORIZONTAL:
            s = VERTICAL
        for i in range(numChars):
            text = chr(ord(beginChar) + numChars - i - 1)
            (x, y) = self.drawChar(x, y, scale, width, s, text=text, **kwargs)

        if direction == VERTICAL_END_HORIZONTAL:
            direction = HORIZONTAL

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space * numChars

        return (xD, yD)


    def drawNumIter(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale

        for key, value in kwargs.items():
            if key == "beginNum":
                beginNum = value
            elif key == "endNum":
                endNum = value
        x = xD + 3 * scale
        y = yD

        for i in range(beginNum, endNum + 1):
            text = str(i)
            (x, y) = self.drawChar(x, y, scale, width, direction=direction, text=text, scaleChar=0.7, **kwargs)

        if direction == HORIZONTAL:
            xD += inter_space * (endNum - beginNum)
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawSquareHole(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale

        darkColor, lightColor, holeColor = "#c0c0c0", "#f6f6f6", "#484848"
        for key, value in kwargs.items():
            if key == "colors":
                darkColor, lightColor, holeColor = value

        self.canvas.create_polygon(xD, yD + space, xD, yD, xD + space, yD, fill=darkColor, outline=darkColor)
        self.canvas.create_polygon(xD, yD + space, xD + space, yD + space, xD + space, yD, fill=lightColor, outline=lightColor)
        self.canvas.create_rectangle(
            xD + space // 3, yD + space // 3, xD + 2 * space // 3, yD + 2 * space // 3, fill=holeColor, outline=holeColor
        )

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawRoundHole(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale

        darkColor, lightColor, holeColor = "#c0c0c0", "#f6f6f6", "#484848"
        for key, value in kwargs.items():
            if key == "colors":
                darkColor, lightColor, holeColor = value

        self.canvas.create_arc(
            xD, yD, xD + space, yD + space, start=45, extent=225, style=tk.PIESLICE, fill=darkColor, outline=darkColor
        )  # x, y2 - 2*radius, x + 2*radius, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs
        self.canvas.create_arc(
            xD, yD, xD + space, yD + space, start=225, extent=45, style=tk.PIESLICE, fill=lightColor, outline=lightColor
        )
        self.canvas.create_oval(
            xD + space // 3, yD + space // 3, xD + 2 * space // 3, yD + 2 * space // 3, fill=holeColor, outline=holeColor
        )

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    funcHole = {"function": drawSquareHole}


    def drawHole(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        return self.funcHole["function"](xD, yD, scale, width, direction, **kwargs)


    def setfuncHole(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        function = self.drawSquareHole
        for key, value in kwargs.items():
            if key == "function":
                function = value

        self.funcHole = {"function": function}

        return xD, yD


    def drawBlank(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawHalfBlank(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale

        if direction == HORIZONTAL:
            xD += inter_space / 2
        elif direction == VERTICAL:
            yD += inter_space / 2

        return (xD, yD)


    def drawRail(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        color = "black"
        for key, value in kwargs.items():
            if key == "color":
                color = value
        inter_space = 15 * scale
        thickness = 2 * scale
        self.canvas.create_line(
            xD + inter_space // 3,
            yD + inter_space // 2,
            xD + inter_space * 1.5,
            yD + inter_space // 2,
            fill=color,
            width=thickness,
        )

        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawredRail(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        inter_space = 15 * scale
        # thickness = 2*scale

        (x, y) = self.drawRail(xD, yD - inter_space // 2, scale, width, direction, color="red")

        return (x, yD)


    def drawBoard(self, xD=0, yD=0, scale=1, width=-1, direction=VERTICAL, **kwargs):
        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale
        thickness = 1 * scale

        dim = BOARD_830_PTS_PARAMS
        color = "#F5F5DC"
        sepAlim = dim["sepAlim"]
        sepDist = dim["sepDistribution"]
        radius = 5
        for key, value in kwargs.items():
            if key == "dimLine":
                dim["dimLine"] = value
            if key == "dimColumn":
                dim["dimColumn"] = value
            if key == "color":
                color = value
            if key == "sepAlim":
                sepAlim = value
            if key == "sepDistribution":
                sepDist = value
            if key == "radius":
                radius = value

        thickness = 1 * scale
        dimLine = dim["dimLine"] * inter_space
        dimColumn = dim["dimColumn"] * inter_space
        id_origins["bottomLimit"] = (dimLine + xD, yD + dimColumn)
        # sepAlim =  [] if not dim.get("sepAlim") else dim.get("sepAlim")
        # sepDistribution =  [] if not dim.get("sepDistribution") else dim.get("sepDistribution")
        self.rounded_rect(xD, yD, dimLine, dimColumn, radius, outline=color, fill=color, thickness=thickness)
        for sepA in sepAlim:
            self.canvas.create_line(
                xD + inter_space * sepA[0],
                yD + inter_space * sepA[1],
                xD - inter_space * sepA[0] + dimLine,
                yD + inter_space * sepA[1],
                fill="#707070",
                width=thickness,
            )
        darknessFactor = 0.9
        r = int(color[1:3], 16) * (darknessFactor + 0.06)
        r = int(max(0, min(255, r)))
        g = int(color[3:5], 16) * (darknessFactor + 0.06)
        g = int(max(0, min(255, g)))
        b = int(color[5:7], 16) * (darknessFactor + 0.06)
        b = int(max(0, min(255, b)))
        c = ["#{:02x}{:02x}{:02x}".format(r, g, b)]
        r = int(color[1:3], 16) * (darknessFactor)
        r = int(max(0, min(255, r)))
        g = int(color[3:5], 16) * (darknessFactor)
        g = int(max(0, min(255, g)))
        b = int(color[5:7], 16) * (darknessFactor)
        b = int(max(0, min(255, b)))
        c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
        r *= darknessFactor
        g *= darknessFactor
        b *= darknessFactor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
        r *= darknessFactor
        g *= darknessFactor
        b *= darknessFactor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
        r *= darknessFactor
        g *= darknessFactor
        b *= darknessFactor
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
        for sepD in sepDist:
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1],
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1],
                fill=c[1],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + thickness,
                fill=c[2],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + 2 * thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + 2 * thickness,
                fill=c[3],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + 3 * thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + 3 * thickness,
                fill=c[4],
                width=thickness,
            )
            for dy in range(4, 11):
                self.canvas.create_line(
                    xD + inter_space * sepD[0],
                    yD + inter_space * sepD[1] + dy * thickness,
                    xD + dimLine - inter_space * sepD[0],
                    yD + inter_space * sepD[1] + dy * thickness,
                    fill=c[0],
                    width=thickness,
                )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 4 * thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 4 * thickness,
                fill=c[1],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 3 * thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 3 * thickness,
                fill=c[2],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 2 * thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - 2 * thickness,
                fill=c[3],
                width=thickness,
            )
            self.canvas.create_line(
                xD + inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - thickness,
                xD + dimLine - inter_space * sepD[0],
                yD + inter_space * sepD[1] + inter_space - thickness,
                fill=c[4],
                width=thickness,
            )
        # self.canvas.create_line(xD , yD+inter_space*11+inter_space//3, xD + dimLine, yD + inter_space*11+inter_space//3, fill="#c0c0c0", width=(3*inter_space)//5)
        # if direction == HORIZONTAL:
        #     xD += dimLine
        # else: yD += dimColumn

        return (xD, yD)


    ################ BOITIERS DIP ####################################


    def drawPin(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.canvas.create_line(
            xD + 9 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD + 12 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD + 12 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD + 12 * inter_space // 15,
            yD + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_line(
            xD - 18 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD - 18 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            xD - 18 * inter_space // 15,
            yD + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        # self.canvas.create_line(xD - inter_space//2, yD + 8*inter_space//15, xD - inter_space//2, yD + 13*inter_space//15, fill="#ffffff", width=1)
        # self.canvas.create_line(xD - inter_space//2, yD + 13*inter_space//15, xD , yD + 13*inter_space//15, fill="#ffffff", width=1)
        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            xD - 3 * inter_space // 15,
            yD + orientation * inter_space,
            fill="#ffffff",
            width=1,
            tags=tag,
        )


    def drawLabelPin(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        color = "#ffffff"
        for key, value in kwargs.items():
            if key == "tags":
                tag = value
            if key == "color":
                color = value

        self.canvas.create_rectangle(
            xD,
            yD,
            xD + 4 * inter_space // 15,
            yD + orientation * 4 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )
        self.canvas.create_polygon(
            xD,
            yD + orientation * 4 * inter_space // 15,
            xD + 4 * inter_space // 15,
            yD + orientation * 4 * inter_space // 15,
            xD + 2 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )


    def drawInv(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        color = "#ffffff"
        for key, value in kwargs.items():
            if key == "tags":
                tag = value
            if key == "color":
                color = value

        self.canvas.create_oval(
            xD + 9 * inter_space // 15,
            yD + orientation * 2.5 * inter_space // 15,
            xD + 11 * inter_space // 15,
            yD + orientation * 4.5 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )  # canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')


    def drawOR(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.canvas.create_rectangle(
            xD,
            yD,
            xD + 3 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )
        # self.canvas.create_line(xD + 1*inter_space//2, yD, xD + 1*inter_space//2, yD + 2*inter_space//3, fill="#ffffff", width=1)
        self.canvas.create_line(
            xD + 9 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD + 12 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )

        self.canvas.create_arc(
            xD - 3 * inter_space // 15,
            yD,
            xD + 3 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            start=270,
            extent=180,
            fill="#000000",
            outline="#000000",
            tags=tag,
        )
        self.canvas.create_arc(
            xD - 3 * inter_space // 15,
            yD,
            xD + 9 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            start=-90,
            extent=180,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )


    def symbOR(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.drawOR(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawPin(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def symbNOR(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.drawOR(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawInv(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawPin(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawAOP(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        color = "#ffffff"
        for key, value in kwargs.items():
            if key == "tags":
                tag = value
            if key == "color":
                color = value

        self.canvas.create_polygon(
            xD,
            yD,
            xD + 9 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD,
            yD + orientation * 7 * inter_space // 15,
            fill=color,
            outline=color,
            tags=tag,
        )
        self.canvas.create_line(
            xD + 9 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD + 12 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            fill=color,
            width=1,
            tags=tag,
        )


    def symbNOT(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.drawAOP(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawInv(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)

        self.drawPin(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def drawAND(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.canvas.create_rectangle(
            xD,
            yD,
            xD + 6 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )
        self.canvas.create_line(
            xD + 9 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            xD + 12 * inter_space // 15,
            yD + orientation * 3.5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 5 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_line(
            xD - 3 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            xD + 3 * inter_space // 15,
            yD + orientation * 2 * inter_space // 15,
            fill="#ffffff",
            width=1,
            tags=tag,
        )
        self.canvas.create_arc(
            xD + 6 * inter_space // 15 - 3 * inter_space // 15,
            yD,
            xD + 9 * inter_space // 15,
            yD + orientation * 7 * inter_space // 15,
            start=270,
            extent=180,
            fill="#ffffff",
            outline="#ffffff",
            tags=tag,
        )


    def symbAND(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.drawAND(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawPin(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def symbNAND(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, orientation=1, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        for key, value in kwargs.items():
            if key == "tags":
                tag = value

        self.drawAND(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawInv(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        self.drawPin(xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
        if direction == HORIZONTAL:
            xD += inter_space
        elif direction == VERTICAL:
            yD += inter_space

        return (xD, yD)


    def internalFunc(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        if width != -1:
            scale = width / 9.0

        space = 9 * scale
        inter_space = 15 * scale
        io = []
        for key, value in kwargs.items():
            if key == "logicFunction":
                logicFunction = value
            if key == "io":
                io = value
            if key == "pinCount":
                pinCount = value
            if key == "chipWidth":
                chipWidth = value
        dimColumn = chipWidth * inter_space
        for pin in io:
            p = pin[1][0]
            orientation = 1 - 2 * ((p - 1) * 2 // pinCount)
            if p > pinCount // 2:
                p = 15 - p
            x = xD + 2 * scale + space // 2 + (p - 2) * inter_space + 3 * inter_space // 15
            y = yD + dimColumn // 2 + orientation * 0.2 * inter_space
            logicFunction(x, y, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)


    def onSwitch(self, event, tag, id, numBtn):
        params = current_dict_circuit.get(id)
        if params:
            btn = params["btnMenu"][numBtn - 1]
            if btn > 0:
                btn = abs(btn - 2) + 1
                params["btnMenu"][numBtn - 1] = btn
                if btn == 1:
                    color = "#ff0000"
                    pos = LEFT
                    if numBtn == 1:
                        self.canvas.itemconfig("chipCover" + id, state="normal")
                else:
                    color = "#00ff00"
                    pos = RIGHT
                    if numBtn == 1:
                        self.canvas.itemconfig("chipCover" + id, state="hidden")
                self.canvas.move(tag, pos * 40 - 20, 0)
                self.canvas.itemconfig(tag, fill=color)


    def drawSwitch(
        self, x1, y1, fillSupport="#fffffe", fillSwitch="#ff0000", outSwitch="#000000", posSwitch=LEFT, tag=None, numBtn=1
    ):
        self.canvas.create_arc(x1, y1, x1 + 20, y1 + 20, start=90, extent=180, fill=fillSupport, outline=fillSupport, tags=tag)
        self.canvas.create_arc(
            x1 + 20, y1, x1 + 40, y1 + 20, start=270, extent=180, fill=fillSupport, outline=fillSupport, tags=tag
        )
        self.canvas.create_rectangle(x1 + 10, y1, x1 + 30, y1 + 20, fill=fillSupport, outline=fillSupport, tags=tag)
        self.canvas.create_oval(
            x1 + 3 + posSwitch * 20,
            y1 + 3,
            x1 + 17 + posSwitch * 20,
            y1 + 17,
            fill=fillSwitch,
            outline=outSwitch,
            tags="btn" + str(numBtn) + "_" + tag,
        )
        self.canvas.addtag_withtag(tag, "btn" + str(numBtn) + "_" + tag)


    def onDragMenu(self, event, tag):
        global xSouris, ySouris, drag_mouse_x, drag_mouse_y

        self.canvas.move(tag, event.x - drag_mouse_x, event.y - drag_mouse_y)
        drag_mouse_x, drag_mouse_y = event.x, event.y


    def onStartDragMenu(self, event, tag):
        global drag_mouse_x, drag_mouse_y

        drag_mouse_x, drag_mouse_y = event.x, event.y
        self.canvas.itemconfig(tag, fill="red")


    def onStopDragMenu(self, event, tag):
        self.canvas.itemconfig(tag, fill="#ffffff")


    def onCrossOver(self, event, tag):
        self.canvas.itemconfig("crossBg_" + tag, fill="#008000")


    def onCrossLeave(self, event, tag):
        self.canvas.itemconfig("crossBg_" + tag, fill="")


    def onCrossClick(self, event, tagMenu, tagRef):
        self.canvas.itemconfig(tagMenu, state="hidden")
        self.canvas.itemconfig(tagRef, outline="")


    def drawMenu(self, xMenu, yMenu, thickness, label, tag, id):
        global image_ico_pdf

        rgba_color = (0, 0, 0, 255)
        fillMenu = "#48484c"
        outMenu = "#909098"
        colorCross = "#e0e0e0"
        params = current_dict_circuit.get(id)
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

            self.rounded_rect(xMenu, yMenu, 128, 128, 10, outline=outMenu, fill=fillMenu, thickness=thickness, tags=tag)
            self.canvas.create_rectangle(xMenu, yMenu, xMenu + 114, yMenu + 17, fill="", outline="", tags="drag_" + tag)
            self.canvas.create_line(xMenu, yMenu + 17, xMenu + 127, yMenu + 17, fill=outMenu, width=thickness, tags=tag)
            self.canvas.create_rectangle(
                xMenu + 110, yMenu + 1, xMenu + 125, yMenu + 16, fill="", outline="", tags="crossBg_" + tag
            )
            self.canvas.create_line(
                xMenu + 115, yMenu + 5, xMenu + 120, yMenu + 12, fill=colorCross, width=thickness * 2, tags="cross_" + tag
            )
            self.canvas.create_line(
                xMenu + 115, yMenu + 12, xMenu + 120, yMenu + 5, fill=colorCross, width=thickness * 2, tags="cross_" + tag
            )
            self.drawChar(
                xMenu + 63,
                yMenu + 8,
                scaleChar=0.8,
                angle=0,
                text=label,
                color="#ffffff",
                anchor="center",
                tags="title_" + tag,
            )
            self.drawSwitch(xMenu + 10, yMenu + 27, fillSwitch=color1, posSwitch=pos1, tag="switch_" + tag, numBtn=1)
            self.canvas.tag_bind(
                "btn1_switch_" + tag, "<Button-1>", lambda event: self.onSwitch(event, "btn1_switch_" + tag, id, 1)
            )
            self.drawAOP(xMenu + 82, yMenu + 32, scale=2, color="#000000", tags=tag)
            self.drawAOP(xMenu + 80, yMenu + 30, scale=2, tags=tag)
            self.drawSwitch(xMenu + 10, yMenu + 60, fillSwitch=color2, posSwitch=pos2, tag="switch_" + tag, numBtn=2)
            self.canvas.tag_bind(
                "btn2_switch_" + tag, "<Button-1>", lambda event: self.onSwitch(event, "btn2_switch_" + tag, id, 2)
            )
            self.drawLabelPin(xMenu + 68, yMenu + 65, scale=2, color="#000000", tags=tag)
            self.drawLabelPin(xMenu + 65, yMenu + 62, scale=2, color="#faa000", tags=tag)
            self.drawLabelPin(xMenu + 88, yMenu + 65, scale=2, color="#000000", tags=tag)
            self.drawLabelPin(xMenu + 85, yMenu + 62, scale=2, color="#faa000", tags=tag)
            self.drawLabelPin(xMenu + 108, yMenu + 65, scale=2, color="#000000", tags=tag)
            self.drawLabelPin(xMenu + 105, yMenu + 62, scale=2, color="#faa000", tags=tag)
            self.drawSwitch(xMenu + 10, yMenu + 93, fillSwitch=color3, posSwitch=pos3, tag="switch_" + tag, numBtn=3)
            # img_save.append(canvas.create_image(xMenu + 85, yMenu + 105, image=image_ico_pdf, tags=tag, anchor="center"))
            self.canvas.tag_bind(
                "btn3_switch_" + tag, "<Button-1>", lambda event: self.onSwitch(event, "btn3_switch_" + tag, id, 3)
            )
            self.canvas.tag_raise("drag_" + tag)
            self.canvas.addtag_withtag(tag, "title_" + tag)
            self.canvas.addtag_withtag(tag, "crossBg_" + tag)
            self.canvas.addtag_withtag(tag, "cross_" + tag)
            self.canvas.addtag_withtag(tag, "btn_" + tag)
            self.canvas.addtag_withtag(tag, "drag_" + tag)
            self.canvas.addtag_withtag(tag, "switch_" + tag)
            self.canvas.addtag_withtag("componentMenu", tag)
            self.canvas.tag_bind("drag_" + tag, "<B1-Motion>", lambda event: self.onDragMenu(event, tag))
            self.canvas.tag_bind("drag_" + tag, "<Button-1>", lambda event: self.onStartDragMenu(event, "title_" + tag))
            self.canvas.tag_bind("cross_" + tag, "<Enter>", lambda event: self.onCrossOver(event, tag))
            self.canvas.tag_bind("cross_" + tag, "<Leave>", lambda event: self.onCrossLeave(event, tag))
            self.canvas.tag_bind("cross_" + tag, "<Button-1>", lambda event: self.onCrossClick(event, tag, "activeArea" + id))
            self.canvas.tag_bind("drag_" + tag, "<ButtonRelease-1>", lambda event: self.onStopDragMenu(event, "title_" + tag))
            self.canvas.itemconfig(tag, state="hidden")


    def onEnter(self, tag):
        global xSouris, ySouris

        space = 9
        tagCoords = self.canvas.coords(tag)
        self.canvas.move(tag, xSouris - tagCoords[0] - space, 0)
        self.canvas.tag_raise(tag)
        self.canvas.itemconfig(tag, state="normal")


    def onMenu(self, event, tagMenu, tagAll, tagRef, colorOut="#60d0ff"):
        self.canvas.tag_raise(tagMenu)
        self.canvas.itemconfig(tagAll, state="hidden")
        self.canvas.itemconfig(tagMenu, state="normal")
        self.canvas.itemconfig("componentActiveArea", outline="")
        self.canvas.itemconfig(tagRef, outline=colorOut)


    # Fonction pour réinitialiser le curseur lorsqu'il sort de la zone
    def onLeave(self, tag):
        self.canvas.itemconfig("bg_" + tag, state="hidden")
        self.canvas.itemconfig("symb_" + tag, state="hidden")
        self.canvas.itemconfig("pin_" + tag, state="hidden")
        self.canvas.itemconfig(tag, state="hidden")
        
    def change_hole_state(x,y,nbBroche,state):
        pass

    def drawChip(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        global num_id

        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale
        space = 9 * scale
        thickness = 1 * scale

        dim = DIP14_PARAMS
        open = NO
        internalFunc = None
        cursorOver = ""
        id = None
        tags = []
        for key, value in kwargs.items():
            if key == "pinCount":
                dim["pinCount"] = value
            if key == "chipWidth":
                dim["chipWidth"] = value
            if key == "label":
                dim["label"] = value
            if key == "internalFunc":
                dim["internalFunc"] = value
            if key == "open":
                open = value
            if key == "cursorOver":
                cursorOver = value
            if key == "id":
                id = value
            if key == "tags":
                tags = value
            if key == "type":
                type = value
            if key == "io":
                io = value
            if key == "symbScript":
                symbScript = value

        dimLine = (dim["pinCount"] - 0.30) * inter_space / 2
        dimColumn = dim["chipWidth"] * inter_space

        params = {}
        if id:
            if current_dict_circuit.get(id):
                params = current_dict_circuit[id]
                tags = params["tags"]
        else:
            id_type[type] += 1
            id = "_chip_" + str(num_id)
            current_dict_circuit["last_id"] = id
            num_id += 1

        if not tags:
            params["id"] = id
            params["XY"] = (xD, yD)
            params["pinUL_XY"] = (xD + 2*scale, yD - space*scale)  
            params["chipWidth"] = dim["chipWidth"]
            params["pinCount"] = dim["pinCount"]
            dimLine = (dim["pinCount"] - 0.30) * inter_space / 2
            dimColumn = dim["chipWidth"] * inter_space
            label = dim["label"] + "-" + str(id_type[type])
            params["label"] = label
            params["type"] = type
            params["btnMenu"] = [1, 1, 0]
            params["symbScript"] = symbScript
            params["io"] = io
            nbBrocheParCote = dim["pinCount"] // 2
            #self.change_hole_state(xD,yD,nbBrocheParCote,USED)
            tagBase = "base" + id
            tagMenu = "menu" + id
            tagCapot = "chipCover" + id
            tagSouris = "activeArea" + id

            params["tags"] = [tagBase, tagSouris]

            

            for i in range(dim["pinCount"]):
                self.canvas.create_rectangle(
                    xD + 2 * scale + (i % nbBrocheParCote) * inter_space,
                    yD - (0 - (i // nbBrocheParCote) * (dimColumn + 0)),
                    xD + 11 * scale + (i % nbBrocheParCote) * inter_space,
                    yD - (3 * scale - (i // nbBrocheParCote) * (dimColumn + 6 * scale)),
                    fill="#909090",
                    outline="#000000",
                    tags=tagBase,
                )
                self.canvas.create_polygon(
                    xD + 2 * scale + (i % nbBrocheParCote) * inter_space,
                    yD - space // 3 - (0 - (i // nbBrocheParCote) * (dimColumn + 2 * space // 3)),
                    xD + space // 3 + 2 * scale + (i % nbBrocheParCote) * inter_space,
                    yD - (2 * space) // 3 - (0 - (i // nbBrocheParCote) * (dimColumn + (4 * space) // 3)),
                    xD + (2 * space) // 3 + 2 * scale + (i % nbBrocheParCote) * inter_space,
                    yD - (2 * space) // 3 - (0 - (i // nbBrocheParCote) * (dimColumn + (4 * space) // 3)),
                    xD + (11 + (i % nbBrocheParCote) * 15) * scale,
                    yD - space // 3 - (0 - (i // nbBrocheParCote) * (dimColumn + 2 * space // 3)),
                    fill="#b0b0b0",
                    outline="#000000",
                    smooth=False,
                    tags=tagBase,
                )
                # AJOUT KH PR DRAG-DROP 23/10/2024
            params["pinUL_XY"] = (xD + 2*scale, yD - space)
            self.canvas.create_rectangle(
                xD + 2 * scale,
                yD - space ,
                xD + 3 * scale ,
                yD - space  + 1,
                fill="#0000ff",
                outline="#0000ff",
                tags=tagBase,
            )            
            # FIN AJOUT KH
            self.rounded_rect(xD, yD, dimLine, dimColumn, 5, outline="#343434", fill="#343434", thickness=thickness, tags=tagBase)
            
            self.canvas.create_rectangle(
                xD + 2 * scale,
                yD + 2 * scale,
                xD - 2 * scale + dimLine,
                yD - 2 * scale + dimColumn,
                fill="#000000",
                outline="#000000",
                tags=tagBase,
            )
            if dim["internalFunc"] is not None:
                dim["internalFunc"](xD, yD, scale=scale, tags=tagBase, **kwargs)

            self.rounded_rect(
                xD, yD, dimLine, dimColumn, 5, outline="#343434", fill="#343434", thickness=thickness, tags=tagCapot
            )
            self.canvas.create_line(
                xD, yD + 1 * space // 3, xD + dimLine, yD + 1 * space // 3, fill="#b0b0b0", width=thickness, tags=tagCapot
            )
            self.canvas.create_line(
                xD,
                yD + dimColumn - 1 * space // 3,
                xD + dimLine,
                yD + dimColumn - 1 * space // 3,
                fill="#b0b0b0",
                width=thickness,
                tags=tagCapot,
            )
            self.canvas.create_oval(
                xD + 4 * scale,
                yD + dimColumn - 1 * space // 3 - 6 * scale,
                xD + 8 * scale,
                yD + dimColumn - 1 * space // 3 - 2 * scale,
                fill="#ffffff",
                outline="#ffffff",
                tags=tagCapot,
            )
            self.canvas.create_arc(
                xD - 5 * scale,
                yD + dimColumn // 2 - 5 * scale,
                xD + 5 * scale,
                yD + dimColumn // 2 + 5 * scale,
                start=270,
                extent=180,
                fill="#000000",
                outline="#505050",
                style=tk.PIESLICE,
                tags=tagCapot,
            )
            self.drawChar(
                xD + dimLine // 2,
                yD + dimColumn // 2,
                scale=scale,
                angle=0,
                text=label,
                color="#ffffff",
                anchor="center",
                tags=tagCapot,
            )  # xD + 30*scale,yD - 10*scale
            self.canvas.create_rectangle(
                xD + 2 * scale,
                yD + 2 * scale,
                xD - 2 * scale + dimLine,
                yD - 2 * scale + dimColumn,
                fill="",
                outline="",
                tags=tagSouris,
            )
            self.canvas.tag_raise(tagCapot)
            self.canvas.tag_raise(tagSouris)
            self.canvas.addtag_withtag("componentActiveArea", tagSouris)
            if open:
                self.canvas.itemconfig(tagCapot, state="hidden")
            else:
                params["tags"].append(tagCapot)
            current_dict_circuit[id] = params
            self.drawMenu(xD + dimLine + 2.3 * scale + space * 0, yD - space, thickness, label, tagMenu, id)
            self.canvas.tag_bind(
                tagSouris, "<Button-2>", lambda event: self.onMenu(event, tagMenu, "componentMenu", tagSouris)
            )
             # Bind left-click to initiate drag
            self.canvas.tag_bind(tagSouris, "<Button-1>", lambda event, chip_id=id: self.on_chip_click(event, chip_id))

            # Bind drag and release events to the activeArea tag
            self.canvas.tag_bind(tagSouris, "<B1-Motion>", self.on_chip_drag)
            self.canvas.tag_bind(tagSouris, "<ButtonRelease-1>", self.on_stop_chip_drag)
        else:
            X, Y = params["XY"]
            dX = xD - X
            dY = yD - Y
            params["XY"] = (xD, yD)
                # AJOUT KH PR DRAG-DROP 23/10/2024
            params["pinUL_XY"] = (xD + 2*scale, yD - space*scale)            
            for tg in tags:
                self.canvas.move(tg, dX, dY)


        return xD + dimLine + 2.3 * scale, yD




################## AJOUT KH 25/10/2024 ######################################
    def getColLine(self, x, y, scale=1, **kwargs):
        inter_space = 15 * scale
        space = 9 * scale
        thickness = 1 * scale
        matrix = matrix830pts
        point_col_lin = (-1,-1)
        for key, value in kwargs.items():
            if key == "matrix":
                matrix = value
        
        for point in matrix.items():
            grid_x, grid_y = point[1]["xy"]
                    
            if (grid_x, grid_y) == (x,y) :
                point_col_lin = point[1]["coord"]

        return point_col_lin            
################## FIN AJOUT KH 25/10/2024 ######################################



    def getXY(self, column, line, scale=1, **kwargs):
        inter_space = 15 * scale
        space = 9 * scale
        thickness = 1 * scale
        matrix = matrix830pts
        for key, value in kwargs.items():
            if key == "matrix":
                matrix = value

        id = str(column) + "," + str(line)
        x, y = matrix[id]["xy"]

        return x * scale, y * scale


    def drawWire(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
        global num_id

        if width != -1:
            scale = width / 9.0
        inter_space = 15 * scale
        space = 9 * scale
        thickness = 1 * scale
        matrix = matrix830pts
        mode= AUTO
        id = None
        multipoints = []
        for key, value in kwargs.items():
            if key == "color":
                color = value
            if key == "mode":
                mode = value
            if key == "coord":
                coords = value
            if key == "matrix":
                matrix = value
            if key == "id":
                id = value
            if key == "tags":
                tags = value
            if key == "XY":
                [(xs,ys,xe,ye)] = value
            if key == "multipoints":
                multipoints = value

        params = {}
        if id:  # If the wire already exists, delete it and redraw
            if current_dict_circuit.get(id):
                params = current_dict_circuit[id]
                tags = params["tags"]
                params["mode"] = mode
                params["coord"] = coords
                params["multipoints"] = multipoints
                xO, yO, xF, yF = coords[0]
                if xO != -1:
                    xO, yO = self.getXY(xO, yO, scale=scale, matrix=matrix)
                else: 
                    xO, yO = xs, ys
                    #print(f"({xO+xD},{yO+yD}) - deb - col proche:{cn} - ligne p: {ln}")
                if xF != -1:     
                    xF, yF = self.getXY(xF, yF, scale=scale, matrix=matrix)
                else: 
                    xF, yF = xe, ye
                    #print(f"({xF+xD},{yF+yD}) - fin - col proche:{cn} - ligne p: {ln}")
                x1_old,y1_old,x2_old,y2_old = params["XY"]
                dx1, dy1 = xO - x1_old, yO - y1_old
                dx2, dy2 = xF - x2_old, yF - y2_old
                params["XY"] = (xO, yO, xF, yF)
                params["color"] = color
                encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"
                wire_body_tag = f"{id}_body"
                wire_body_shadow_tag = f"{id}_body_shadow"
                start_endpoint_tag = f"{id}_start"
                end_endpoint_tag = f"{id}_end"
                select_start_tag = f"{id}_select_start"
                select_end_tag = f"{id}_select_end"
                #divY  = yF - yO if yF != yO else 0.000001
                # xDiff = (space/2)*(1 - math.cos(math.atan((xF-xO)/divY)))
                # yDiff = (space/2)*(1 - math.sin(math.atan((xF-xO)/divY)))
                # p1    = ( xD + (xO + xDiff), yD + (yO + space - yDiff))
                # p2    = ( xD + (xF + xDiff), yD + (yF + space - yDiff))
                # p3    = ( xD + (xF + space - xDiff), yD + (yF + yDiff))
                # p4    = ( xD + (xO+ space - xDiff), yD + (yO + yDiff))
                # flat_coords = [coord for point in [p1, p2, p3, p4] for coord in point]
                multipoints = [xO, yO] + multipoints + [xF, yF]
                #multipoints = [xO + 1*scale, yO + 1*scale] + multipoints + [xF - 1*scale, yF- 1*scale]
                multipoints = [val + 5*scale + (xD if i % 2 == 0 else yD) for i, val in enumerate(multipoints)]
                # self.canvas.create_line(multipoints, fill=contour, width=8*thickness , 
                #                 tags=(id, wire_body_tag))
                # self.canvas.create_line(multipoints, fill=encre, width=6*thickness, 
                #                 tags=(id, wire_body_tag))
                self.canvas.coords(wire_body_tag, multipoints)
                self.canvas.coords(wire_body_shadow_tag, multipoints)
                self.canvas.move(start_endpoint_tag, dx1, dy1)
                self.canvas.move(end_endpoint_tag, dx2, dy2)
                self.canvas.move(select_start_tag, dx1, dy1)
                self.canvas.move(select_end_tag, dx2, dy2)
        else:
            id = "_wire_" + str(num_id)
            current_dict_circuit["last_id"] = id
            num_id += 1
            params["id"] = id
            params["mode"] = mode
            params["coord"] = coords
            params["multipoints"] = multipoints
            xO, yO, xF, yF = coords[0]
    ############ MODIF KH 25/10/2024 ###############################
            if xO != -1:
                xO, yO = self.getXY(xO, yO, scale=scale, matrix=matrix)
            else: xO, yO = xs, ys
            if xF != -1:     
                xF, yF = self.getXY(xF, yF, scale=scale, matrix=matrix)
            else: xF, yF = xe, ye
    ############ FIN MODIF KH 25/10/2024 ###############################
            params["XY"] = (xO, yO, xF, yF)
            params["color"] = color
            encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"

            # Define unique tags for the wire components
            wire_body_tag = f"{id}_body"
            wire_body_shadow_tag = f"{id}_body_shadow"
            start_endpoint_tag = f"{id}_start"
            end_endpoint_tag = f"{id}_end"
            select_start_tag = f"{id}_select_start"
            select_end_tag = f"{id}_select_end"
            
            # # Create the wire body as a line
            # self.canvas.create_line(
            #     xD + xO, yD + yO,
            #     xD + xF, yD + yF,
            #     fill=encre,
            #     width=6 * thickness,
            #     tags=(id, wire_body_tag),
            # )

            # Create endpoints as separate items
            endpoint_radius = 3 * scale  # Adjust size as needed

            # Starting endpoint
            # MODIF KH DRAG 23/10/2024
            # self.canvas.create_oval(
            #     xD + xO - endpoint_radius,
            #     yD + yO - endpoint_radius,
            #     xD + xO + endpoint_radius,
            #     yD + yO + endpoint_radius,
            #     fill="#dfdfdf",
            #     outline="#404040",
            #     width=1 * thickness,
            #     tags=(id, start_endpoint_tag),
            # )
            self.canvas.create_oval(
                xD + xO + 2*scale,
                yD + yO + 2*scale,
                xD + xO + 7*scale,
                yD + yO + 7*scale,
                fill="#dfdfdf",
                outline="#404040",
                width=1 * thickness,
                tags=(id,start_endpoint_tag), 
            )
            self.canvas.create_oval(
                xD + xO - 2*scale,
                yD + yO - 2*scale,
                xD + xO + 9*scale,
                yD + yO + 9*scale,
                fill="",
                outline="",
                width=1 * thickness,
                tags=(id, select_start_tag), 
            )
        
            
            # Ending endpoint
            # self.canvas.create_oval(
            #     xD + xF - endpoint_radius,
            #     yD + yF - endpoint_radius,
            #     xD + xF + endpoint_radius,
            #     yD + yF + endpoint_radius,
            #     fill="#dfdfdf",
            #     outline="#404040",
            #     width=1 * thickness,
            #     tags=(id, end_endpoint_tag),
            # )
            self.canvas.create_oval(
                xD + xF + 2*scale,
                yD + yF + 2*scale,
                xD + xF + 7*scale,
                yD + yF + 7*scale,
                fill="#dfdfdf",
                outline="#404040",
                width=1 * thickness,
                tags=(id, end_endpoint_tag),
            )
            self.canvas.create_oval(
                xD + xF - 2*scale,
                yD + yF - 2*scale,
                xD + xF + 9*scale,
                yD + yF + 9*scale,
                fill="",
                outline="",
                width=1 * thickness,
                tags=(id, select_end_tag),
            )
            
            
            # Create the wire body as a line
            # self.canvas.create_line(
            #     xD + xO + 5*scale, yD + yO + 5*scale,
            #     xD + xF + 5*scale, yD + yF + 5*scale,
            #     fill=encre,
            #     width=6 * thickness,
            #     tags=(id, wire_body_tag),
            # )
##############   MODIF KH MULTIPOINTS 27/10/2024  #########################
            # divY  = yF - yO if yF != yO else 0.000001
            # xDiff = (space/2)*(1 - math.cos(math.atan((xF-xO)/divY)))
            # yDiff = (space/2)*(1 - math.sin(math.atan((xF-xO)/divY)))
            # p1    = ( (xO + xDiff), (yO + space - yDiff))
            # p2    = ( (xF + xDiff), (yF + space - yDiff))
            # p3    = ( (xF + space - xDiff), (yF + yDiff))
            # p4    = ( (xO+ space - xDiff), (yO + yDiff))
            # self.canvas.create_polygon(xD + p1[0], yD + p1[1], xD + p2[0], yD + p2[1], \
            #                     xD + p3[0], yD + p3[1], xD + p4[0], yD + p4[1], \
            #                     fill=encre, outline=contour, width=1*thickness, 
            #                     tags=(id, wire_body_tag) )  
            
            #multipoints = [xO + 1*scale, yO + 1*scale] + multipoints + [xF - 1*scale, yF- 1*scale]
            #multipoints = [x + xD + 5*scale, y + yD + 5*scale for (x, y) in multipoints]
            multipoints = [xO, yO] + multipoints + [xF, yF]
            multipoints = [val  + 5*scale + (xD if i % 2 == 0 else yD) for i, val in enumerate(multipoints)]
            self.canvas.create_line(multipoints, fill=contour, width=8*thickness , 
                                tags=(id,  wire_body_shadow_tag))
            self.canvas.create_line(multipoints, fill=encre, width=4*thickness, 
                                tags=(id, wire_body_tag))
##############  FIN MODIF KH MULTIPOINTS 27/10/2024  #########################
            # Store tags and positions in params
            params["tags"] = [id, wire_body_tag, start_endpoint_tag, end_endpoint_tag]
            params["wire_body_tag"] = wire_body_tag
            params["endpoints"] = {
                "start": {"position": (xD + xO, yD + yO), "tag": start_endpoint_tag},
                "end": {"position": (xD + xF, yD + yF), "tag": end_endpoint_tag},
            }
            self.canvas.tag_raise(select_start_tag)
            self.canvas.tag_raise(select_end_tag)
            self.canvas.tag_raise("selector_cable")
            # Bind events to the endpoints for drag-and-drop
            
            self.canvas.tag_bind(wire_body_tag, "<Enter>", lambda event, wire_id=id: self.on_wire_body_enter(event, wire_id))
            self.canvas.tag_bind(wire_body_tag, "<Leave>", lambda event, wire_id=id: self.on_wire_body_leave(event, wire_id))
            self.canvas.tag_bind(wire_body_tag, "<Button-1>", lambda event, wire_id=id: self.on_wire_body_click(event, wire_id))
            self.canvas.tag_bind(wire_body_tag, "<B1-Motion>", lambda event, wire_id=id: self.on_wire_body_drag(event, wire_id))
            
            self.canvas.tag_bind(wire_body_tag, "<Button-1>", lambda event, wire_id=id: self.on_wire_body_click(event, wire_id))
            self.canvas.tag_bind(select_start_tag, "<Button-1>", lambda event, wire_id=id: self.on_wire_endpoint_click(event, wire_id, 'start'))
            self.canvas.tag_bind(select_end_tag, "<Button-1>", lambda event, wire_id=id: self.on_wire_endpoint_click(event, wire_id, 'end'))

            self.canvas.tag_bind(select_start_tag, "<B1-Motion>", lambda event, wire_id=id: self.on_wire_endpoint_drag(event, wire_id, 'start'))
            self.canvas.tag_bind(select_end_tag, "<B1-Motion>", lambda event, wire_id=id: self.on_wire_endpoint_drag(event, wire_id, 'end'))

            self.canvas.tag_bind(select_start_tag, "<ButtonRelease-1>", lambda event, wire_id=id: self.on_wire_endpoint_release(event, wire_id, 'start'))
            self.canvas.tag_bind(select_end_tag, "<ButtonRelease-1>", lambda event, wire_id=id: self.on_wire_endpoint_release(event, wire_id, 'end'))

        current_dict_circuit[id] = params

        return xD, yD

    def clear_board(self):
        """Clear the board of all drawn components."""
        for item in current_dict_circuit.values():
            if "tags" not in item:
                continue
            for tag in item["tags"]:
                self.canvas.delete(tag)
        for key in id_type:
            id_type[key] = 0
        current_dict_circuit.clear()
        # TODO Khalid update the Circuit instance