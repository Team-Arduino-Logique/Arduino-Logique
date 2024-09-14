import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageGrab

import math
from dataCDLT import *
from ElectroComponent import *
from dataComponent import *


def setDictCircuit(dico = baseDictCircuit, **kwargs):
    curDictCircuit = dico    

def followMouse(event, canvas):
    global mouseX, mouseY 

    mouseX, mouseY = event.x, event.y
    
        
def init(canvas):
    global curCursor, imageIcoPdf, idOrigin, cursorSave, idType, curDictCircuit, numID, mouseX, mouseY, dragMouseX, dragMouseY
    
    imgSave = []
    idOrigin = {"xyOrigin":(0,0)}
    curCursor = None
    cursorSave = None
    baseDictCircuit = {}
    #idType = {}
    curDictCircuit = baseDictCircuit
    numID = 1
    mouseX, mouseY = 0,0
    dragMouseX, dragMouseY = 0,0
    idType.update({"dip14":0,"74HC00":0,"74HC02":0,"74HC08":0,"74HC04":0,"74HC32":0, "idCircuit":0})

    canvas.config(cursor="")

    image       = Image.open(ICO_PDF["path"])
    
    imageIcoPdf  = ImageTk.PhotoImage(image.resize((32,32)))    
    #canvas.itemconfig(curseur["imageId"] , state='normal')   
    #curCursor = curseur["imageId"]
    canvas.bind("<Motion>", lambda event:  followMouse(event, canvas))
    
def captureCanvasArea(canvas, x1, y1, x2, y2):
    # Convertir les coordonnées canvas en coordonnées de l'écran
    x1 = canvas.winfo_rootx() + x1
    y1 = canvas.winfo_rooty() + y1
    x2 = canvas.winfo_rootx() + x2
    y2 = canvas.winfo_rooty() + y2
    
    # Capturer la zone spécifiée directement à partir de l'écran
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    return image

def text2Img(text, angle=90, fontPath="FiraCode-Light", fontSize=15, color=(0, 0, 0, 255), size=(15,15) ):

    police = ImageFont.truetype(fontPath, fontSize)

    #imgTemp = Image.new('RGBA', (1, 1))
    #draw = ImageDraw.Draw(imgTemp)

    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    draw.text((0, 0), text, font=police, fill=color)
    
    imageRot = image.rotate(angle, expand=1)
    
    return ImageTk.PhotoImage(imageRot)
    

def fillMatrix830pts(colD=1,  lineD = 1, **kwargs):
    interSpace = 15

    matrix = matrix830pts
    for key, value in kwargs.items():
        if key == "matrix": matrix =value
        
    for i in range(50):
        idph = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(1 + lineD) 
        idpb = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(13 + lineD)
        idmh = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str( lineD)
        idmb = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(12 + lineD)
        matrix[idmh]={"id":["ph", "plus haut", "1"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (1.5 + 22.2*(lineD//15))*interSpace ), "etat":FREE, "lien":None }
        matrix[idph]={"id":["mh", "moins haut", "2"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (2.5+ 22.2*(lineD//15))*interSpace), "etat":FREE, "lien":None }
        matrix[idmb]={"id":["pb", "plus bas", "13"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (19.5 + 22.2*(lineD//15))*interSpace), "etat":FREE, "lien":None }
        matrix[idpb]={"id":["mb", "moins bas", "14"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (20.5+ 22.2*(lineD//15))*interSpace), "etat":FREE, "lien":None }
    for l in range(5):
        for c in range(63):
            id = str(c + colD) + "," + str(l + 2 + lineD) 
            matrix[id]={"id":[id, str(l + 2 + lineD)], "xy":(0.5*interSpace + (c + colD)*interSpace, (5.5 + l + 22.2*(lineD//15))*interSpace), "etat":FREE, "lien":None }
            id = str(c + colD)+ "," + str(l + 7 + lineD) 
            matrix[id]={"id":[id, str(l + 7 + lineD)], "xy":(0.5*interSpace +  (c + colD)*interSpace, (12.5 + l + 22.2*(lineD//15))*interSpace), "etat":FREE, "lien":None }
            
def fillMatrix1260pts(colD=1,  lineD = 1, **kwargs):
    interSpace = 15
    
    matrix = matrix1260pts            
    for key, value in kwargs.items():
        if key == "matrix": matrix =value

    fillMatrix830pts(matrix=matrix1260pts)
    fillMatrix830pts(lineD=15, matrix=matrix1260pts)


def circuit(canvas, xD=0, yD=0, scale=1, width = -1,  direction = VERTICAL, **kwargs):
    if (width !=-1):
        scale = width / 9.0
    interSpace = 15*scale  
    
    #xO=yO=-1
    model = lineDistribution
    idCircuit = ""
    for key, value in kwargs.items():
        if key == "model":     model          = value
        if key == "dXY":        dX, dY          = value
        if key == "idCircuit":  idCircuit       = value
        
    #if xO == -1: xO, yO = xD,yD
    x, y = xD,yD
    for element in model:
        if callable(element[0]) and isinstance(element[1],int):
            for _ in range(element[1]):
                if len(element) == 3:
                    (x, y, *retour) = element[0](canvas, x, y, scale, width,**element[2])
                else : (x, y, *retour) = element[0](canvas, x, y, scale, width)
        elif isinstance(element[0],list) and isinstance(element[1],int) :
            for _ in range(element[1]):
                if len(element) == 3:
                    (x,y, *retour) = circuit(canvas,x,y,scale,width, model=element[0], **element[2] )
                else : (x,y, *retour) = circuit(canvas,x,y,scale,width,model=element[0])
        else: raise ValueError("L'argument modele de rail doit être un tuple (fonction(), int, [int]) ou (list, int, [int]).")
        

    if direction == HORIZONTAL :  xD = x
    elif direction == VERTICAL :  yD = y + interSpace 
    elif direction == PERSO    :  
        yD = y - interSpace*dY
        #xD = x - interSpace*dX
    
                
    return (xD, yD )


