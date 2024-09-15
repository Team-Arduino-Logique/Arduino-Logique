PERSO                       = 0
HORIZONTAL                  = 1 
VERTICAL                    = 2 
VERTICAL_END_HORIZONTAL     = 3
AUTO                        = 0
DIRECT                      = 1
FREE                        = 0
USED                        = 1
NO                          = 0
YES                         = 1
LEFT                        = 0
RIGHT                      = 1
NOTHING                        = (0, 0)
ICO_PDF                     = {"path":"Icones/pdf-icon-png-2079.png", "imageId": None}


img_save = []
id_origins = {"xyOrigin":(0,0)}
cursorCur = None
cursor_save = None
base_dict_circuit = {}
id_type = {}
current_dict_circuit = base_dict_circuit
num_id = 1
mouse_x, mouse_y = 0,0
drag_mouse_x, drag_mouse_y = 0,0

image_ico_pdf = None

matrix830pts = {}
matrix1260pts = {}

id_type.update({"dip14":0,"74HC00":0,"74HC02":0,"74HC08":0,"74HC04":0,"74HC32":0})