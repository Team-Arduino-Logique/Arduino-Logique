def drawPinIO(self, xD, yD, scale=1, width=-1, direction=HORIZONTAL, **kwargs):
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
            if key == "coords":
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
                
#################    ICI TON CODE PRIMITIVES GRAPHIQUE SI LA PIN EST DÉJÀ PLACÉE  ####################
        else:
            id = "_wire_" + str(num_id)
            num_id += 1
            params["id"] = id
#################    ICI TON CODE PRIMITIVES GRAPHIQUE SI LA PIN N'EST PAS ENCORE PRÉSENTE ####################

    current_dict_circuit[id] = params

    return xD, yD 