#from dataComponent import *


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


imgSave = []
idOrigins = {"xyOrigin":(0,0)}
cursorCur = None
cursorSave = None
baseDictCircuit = {}
idType = {}
curDictCircuit = baseDictCircuit
numID = 1
mouseX, mouseY = 0,0
dragMouseX, dragMouseY = 0,0

imageIcoPdf = None

matrix830pts = {}
matrix1260pts = {}

idType.update({"dip14":0,"74HC00":0,"74HC02":0,"74HC08":0,"74HC04":0,"74HC32":0})