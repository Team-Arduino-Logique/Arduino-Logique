from dataCDLT import *
import tkinter as tk 
from tkinter import font
import math


def roundedRect(canvas, x, y, width, height, radius,thickness, **kwargs):
    x2 = x + width
    y2 = y + height
    points = [
        x + radius, y,
        x2 - radius, y,
      #  x2, y,
        x2, y + radius,
        x2, y2 - radius,
    #    x2, y2,
        x2 - radius, y2,
        x + radius, y2,
    #    x, y2,
        x, y2 - radius,
        x, y + radius,
    #    x, y
    ]
    tag=""
    for key, value in kwargs.items():
        if key == "tags"           : tag            = value
        if key == "fill"           : fill           = value
        if key == "thickness"          : thickness      = value
        
   
    # Draw four arcs for corners
    canvas.create_arc(x, y, x + 2*radius, y + 2*radius, start=90, extent=90, style=tk.PIESLICE, **kwargs)
    canvas.create_arc(x2 - 2*radius, y, x2, y + 2*radius, start=0, extent=90, style=tk.PIESLICE, **kwargs)
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, style=tk.PIESLICE,  **kwargs)
    canvas.create_arc(x, y2 - 2*radius, x + 2*radius, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs)
    #kwargs["outline"] = fill
    canvas.create_polygon(points, smooth=False, **kwargs)
    canvas.create_line(x + radius, y,x, y + radius,fill=fill, width=thickness, tags=tag)
    canvas.create_line(x2 - radius, y, x2, y + radius, fill=fill, width=thickness, tags=tag)
    canvas.create_line(x2 - radius, y2, x2 , y2 - radius, fill=fill, width=thickness, tags=tag)
    canvas.create_line(x, y2 - radius, x + radius, y2, fill=fill, width=thickness, tags=tag)


def setXYOrigin(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    xO, yO = xD, yD
    idOrigin = "xyOrigin"
    for key, value in kwargs.items():
        if key == "idOrigin": idOrigin    = value
        #if key == "xyOrigin": xO, yO       = value
        
    idOrigins[idOrigin]=(xD,yD)
    return (xO , yO )

def goXY(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    idOrigin = "xyOrigin"
    for key, value in kwargs.items():
        if key == "line":  line    = value
        if key == "column": column = value
        if key == "idOrigin": idOrigin    = value
        
    xO, yO = idOrigins[idOrigin]
       
    return (xO + column*15*scale, yO + line*15*scale)
    
def drawChar(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    global imgText
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    angle = 90
    for key, value in kwargs.items():
        if key == "angle": angle = value 
    color = "#000000"
    text = "-"
    deltaY = 0
    scaleChar=1
    size = (int(interSpace*1),int( interSpace*1))
    anchor = "center"
    tags=""
    for key, value in kwargs.items():
        if   key == "color"       : color       = value 
        elif key == "text"         : text         = value 
        elif key == "deltaY"        : deltaY        = value 
        elif key == "scaleChar"    : scaleChar    = value
        elif key == "anchor"        : anchor        = value
        elif key == "tags"          : tags          = value
        
    size = (int(scaleChar*interSpace*len(text)),int(scaleChar*interSpace)) 
    firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=int(15*scale*scaleChar))
    if angle !=0:
        firaCodeFont = font.Font(family="FiraCode-Light", size=int(15*scaleChar*scale))
        canvas.create_text(xD , yD + deltaY*space , text=text, font=firaCodeFont, fill=color, anchor=anchor,angle=angle, tags=tags)
    else: canvas.create_text(xD , yD , text=text, font=firaCodeFont, fill=color, anchor=anchor, tags=tags)

    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)


def drawCharIter(canvas, xD,yD,scale=1,width=-1, direction = VERTICAL_END_HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    
    for key, value in kwargs.items():
        if key == "beginChar"          : beginChar      = value 
        elif key == "numChars"         : numChars       = value 
        
    x = xD
    y = yD
    s = direction
    if direction == VERTICAL_END_HORIZONTAL: s = VERTICAL
    for i in range(numChars):
        text = chr(ord(beginChar) + numChars - i-1)
        (x, y) = drawChar (canvas, x,y,scale,width, s , text=text, **kwargs )

    if direction == VERTICAL_END_HORIZONTAL: direction = HORIZONTAL
    
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace * numChars     
    
    return (xD  , yD)
        
def drawNumIter(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    
    for key, value in kwargs.items():
        if key == "beginNum"          : beginNum      = value 
        elif key == "endNum"         : endNum       = value 
    x = xD + 3*scale
    y = yD
    
    
    for i in range(beginNum,endNum+1):
        text = str(i)
        (x, y) = drawChar(canvas, x,y,scale,width, direction=direction , text=text, scaleChar=0.7, **kwargs )

  
    
    if direction == HORIZONTAL:
        xD += interSpace * (endNum - beginNum)  
    elif direction == VERTICAL: yD += interSpace    
    
    return (xD  , yD)    
         

def drawSquareHole(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space       = 9*scale
    interSpace  = 15*scale
    
    darkColor, lightColor, holeColor = '#c0c0c0', '#f6f6f6', "#484848"
    for key, value in kwargs.items():
        if key == "colors"     : darkColor, lightColor, holeColor           = value
 
    canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill=darkColor, outline=darkColor)
    canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill=lightColor, outline=lightColor)
    canvas.create_rectangle(xD+space//3, yD+space//3, xD+2*space//3,yD+2*space//3,fill=holeColor,outline=holeColor)
    
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def drawRoundHole(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space       = 9*scale
    interSpace  = 15*scale
    
    darkColor, lightColor, holeColor = '#c0c0c0', '#f6f6f6', "#484848"
    for key, value in kwargs.items():
        if key == "colors"     : darkColor, lightColor, holeColor           = value
 
    canvas.create_arc(xD, yD, xD + space, yD + space, start=45, extent= 225, style= tk.PIESLICE ,fill=darkColor,  outline=darkColor) #x, y2 - 2*radius, x + 2*radius, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs
    canvas.create_arc(xD, yD, xD + space, yD + space, start=225, extent= 45, style= tk.PIESLICE , fill=lightColor, outline=lightColor)
    canvas.create_oval(xD+space//3, yD+space//3, xD+2*space//3,yD+2*space//3,fill=holeColor,outline=holeColor)
    
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

funcHole = {"function":drawSquareHole}

def drawHole(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs):
    global funcHole

    return funcHole["function"](canvas, xD,yD,scale,width, direction , **kwargs)
    

def setfuncHole(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    global funcHole
    
    function = drawSquareHole
    for key, value in kwargs.items():
        if key == "function"     : function   = value
        
    funcHole = {"function" : function }
    
    return xD, yD

def drawBlank(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    interSpace = 15*scale  
    
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace  
    
    return (xD ,yD)

def drawHalfBlank(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    interSpace = 15*scale  
    
    if direction == HORIZONTAL:
        xD += interSpace/2
    elif direction == VERTICAL: yD += interSpace /2 
    
    return (xD ,yD)

def drawRail(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs):
    if (width !=-1):
        scale = width / 9.0

    color = "black"
    for key, value in kwargs.items():
        if key == "color": color = value 
    interSpace = 15*scale  
    thickness = 2*scale
    canvas.create_line(xD + interSpace//3, yD+interSpace//2, xD + interSpace*1.5, yD + interSpace//2, fill=color, width=thickness)
    
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace  
    
    return (xD ,yD)

def drawredRail(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs):
    if (width !=-1):
        scale = width / 9.0

    interSpace = 15*scale  
    #thickness = 2*scale
    
    (x,y) = drawRail(canvas, xD,yD-interSpace//2,scale,width,direction,color="red")
    
    return (x, yD)


def drawBoard(canvas,xD=0,yD=0,scale=1,width=-1, direction = VERTICAL, **kwargs ):
    from dataComponent import board830pts
    
    if (width !=-1):
        scale = width / 9.0
    interSpace = 15*scale 
    thickness = 1*scale
    
    dim=board830pts
    color ="#F5F5DC"
    sepAlim = dim["sepAlim"]
    sepDist = dim["sepDistribution"]
    radius = 20
    for key, value in kwargs.items():
        if key == "dimLine"             : dim["dimLine"]        = value
        if key == "dimColumn"           : dim["dimColumn"]      = value
        if key == "color"             : color               = value
        if key == "sepAlim"             : sepAlim               = value
        if key == "sepDistribution"     : sepDist               = value
        if key == "radius"               : radius               = value
        
    thickness = 1*scale   
    dimLine = dim["dimLine"]*interSpace
    dimColumn = dim["dimColumn"]*interSpace   
    #sepAlim =  [] if not dim.get("sepAlim") else dim.get("sepAlim")
    #sepDistribution =  [] if not dim.get("sepDistribution") else dim.get("sepDistribution")
    roundedRect(canvas, xD, yD, dimLine,  dimColumn, radius, outline=color, fill=color, thickness=thickness)
    for sepA in sepAlim:
        canvas.create_line(xD + interSpace*sepA[0], yD+interSpace*sepA[1], xD - interSpace*sepA[0] + dimLine, yD + interSpace*sepA[1], fill="#707070", width=thickness) 
    darknessFactor = 0.9
    r = int(color[1:3],16) * (darknessFactor + 0.06)
    r = int(max(0, min(255, r)))
    g = int(color[3:5],16) * (darknessFactor + 0.06)
    g = int(max(0, min(255, g)))
    b = int(color[5:7],16) * (darknessFactor + 0.06)
    b = int(max(0, min(255, b)))
    c = ["#{:02x}{:02x}{:02x}".format(r, g, b)]
    r = int(color[1:3],16) * (darknessFactor )
    r = int(max(0, min(255, r)))
    g = int(color[3:5],16) * (darknessFactor )
    g = int(max(0, min(255, g)))
    b = int(color[5:7],16) * (darknessFactor )
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= darknessFactor; g *= darknessFactor; b *= darknessFactor; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= darknessFactor; g *= darknessFactor; b *= darknessFactor; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= darknessFactor; g *= darknessFactor; b *= darknessFactor; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    for sepD in sepDist:      
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1], xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1], fill=c[1], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1] + thickness, fill=c[2], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + 2*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1]  + 2*thickness, fill=c[3], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + 3*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1]  + 3*thickness, fill=c[4], width=thickness)    
        for dy in range(4,11):
            canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + dy*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1] + dy*thickness, fill=c[0], width=thickness)   
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - 4*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1]+interSpace - 4*thickness, fill=c[1], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - 3*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1] + interSpace - 3*thickness, fill=c[2], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1]+ interSpace - 2*thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1]  + interSpace - 2*thickness, fill=c[3], width=thickness)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - thickness, xD + dimLine - interSpace*sepD[0], yD + interSpace*sepD[1] + interSpace - thickness, fill=c[4], width=thickness)    
    #canvas.create_line(xD , yD+interSpace*11+interSpace//3, xD + dimLine, yD + interSpace*11+interSpace//3, fill="#c0c0c0", width=(3*interSpace)//5)    
    # if direction == HORIZONTAL:
    #     xD += dimLine
    # else: yD += dimColumn  
    
    return (xD ,yD)

################ BOITIERS DIP ####################################

def drawPin(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value
        
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*interSpace, fill="#ffffff", width=1, tags=tag)
    
    canvas.create_line(xD - 18*interSpace//15, yD + orientation*2*interSpace//15, xD + 3*interSpace//15, yD + orientation*2*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD - 18*interSpace//15, yD +orientation* 2*interSpace//15, xD - 18*interSpace//15, yD + orientation*interSpace, fill="#ffffff", width=1, tags=tag)
    
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD + 3*interSpace//15, yD + orientation*5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    #canvas.create_line(xD - interSpace//2, yD + 8*interSpace//15, xD - interSpace//2, yD + 13*interSpace//15, fill="#ffffff", width=1)
    #canvas.create_line(xD - interSpace//2, yD + 13*interSpace//15, xD , yD + 13*interSpace//15, fill="#ffffff", width=1)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD - 3*interSpace//15, yD + orientation*interSpace, fill="#ffffff", width=1, tags=tag)
    
def drawLabelPin(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale   
    color="#ffffff" 
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "color"     : color       = value
        
    canvas.create_rectangle(xD, yD, xD + 4*interSpace//15,yD + orientation*4*interSpace//15,fill=color,outline=color, tags=tag)
    canvas.create_polygon(xD, yD + orientation*4*interSpace//15, xD + 4*interSpace//15 , yD + orientation*4*interSpace//15, xD + 2*interSpace//15 , yD + orientation*7*interSpace//15, fill=color, outline=color, tags=tag)

def drawInv(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale   
    color="#ffffff" 
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "color"     : color       = value
    
    canvas.create_oval(xD + 9*interSpace//15, yD + orientation*2.5*interSpace//15, xD + 11*interSpace//15, yD + orientation*4.5*interSpace//15, fill=color, outline=color, tags=tag)    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')

def drawOR(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value
        
    canvas.create_rectangle(xD, yD, xD + 3*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill="#ffffff", width=1, tags=tag)

    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 3*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=270, extent=180,  fill="#000000", outline="#000000", tags=tag) 
    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=-90, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 

def symbOR(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value
     
    drawOR(canvas, xD,yD,scale=scale,width=width, direction = direction,  orientation = orientation, **kwargs )
    drawPin(canvas, xD, yD,scale=scale,width=width,direction=direction, orientation=orientation, **kwargs)
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def symbNOR(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    drawOR(canvas, xD,yD,scale=scale,width=width, direction = direction,  orientation = orientation, **kwargs )
    drawInv(canvas,xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
    drawPin(canvas, xD, yD,scale=scale,width=width,direction=direction, orientation=orientation, **kwargs)
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def drawAOP(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    color="#ffffff"
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "color"     : color       = value

    canvas.create_polygon(xD, yD, xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD  , yD + orientation*7*interSpace//15, fill=color, outline=color, tags=tag)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill=color, width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD + 3*interSpace//15, yD + orientation*5*interSpace//15, fill=color, width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*2*interSpace//15, xD + 3*interSpace//15, yD + orientation*2*interSpace//15, fill=color, width=1, tags=tag)
   

def symbNOT(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    drawAOP(canvas,xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
    drawInv(canvas,xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)

    drawPin(canvas, xD, yD,scale=scale,width=width,direction=direction, orientation=orientation, **kwargs)
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def drawAND(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    canvas.create_rectangle(xD, yD, xD + 6*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD + 3*interSpace//15, yD + orientation*5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*2*interSpace//15, xD + 3*interSpace//15, yD + orientation*2*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_arc(xD + 6*interSpace//15 - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=270, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 


def symbAND(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    drawAND(canvas, xD,yD,scale=scale,width=width, direction = direction,  orientation = orientation, **kwargs )
    drawPin(canvas, xD, yD,scale=scale,width=width,direction=direction, orientation=orientation,**kwargs)
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def symbNAND(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL,  orientation = 1, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    drawAND(canvas, xD,yD,scale=scale,width=width, direction = direction,  orientation = orientation, **kwargs )
    drawInv(canvas,xD, yD, scale=scale, width=width, direction=direction, orientation=orientation, **kwargs)
    drawPin(canvas, xD, yD,scale=scale,width=width,direction=direction, orientation=orientation, **kwargs)
    if direction == HORIZONTAL:
        xD += interSpace
    elif direction == VERTICAL: yD += interSpace      
    
    return (xD  , yD)


def internalFunc(canvas, xD,yD,scale=1,width=-1, direction = HORIZONTAL, **kwargs ):
    if (width !=-1):
        scale = width / 9.0

    space = 9*scale
    interSpace = 15*scale    
    io = []
    for key, value in kwargs.items():
        if key == "logicFunction"     : logicFunction       = value
        if key == "io"                  : io                    = value
        if key == "pinCount"           : pinCount             = value
        if key == "chipWidth"      : chipWidth        = value
    dimColumn = chipWidth*interSpace  
    for pin in io:
        p = pin[1][0]
        orientation = 1 - 2*((p -1)*2 // pinCount)
        if p > pinCount//2: p = 15 - p 
        x = xD + 2*scale + space//2 + (p - 2)*interSpace + 3*interSpace//15
        y = yD  + dimColumn//2 + orientation*0.2*interSpace
        logicFunction(canvas,x,y,scale=scale, width=width, direction=direction,orientation=orientation, **kwargs)
        

def onSwitch( event, canvas, tag, id, numBtn):
    params = curDictCircuit.get(id)
    if params:
        btn = params["btnMenu"][numBtn - 1]
        if btn > 0 :
            btn = abs(btn - 2) + 1
            params["btnMenu"][numBtn - 1] = btn
            if btn == 1:
                color="#ff0000"; pos = LEFT
                if numBtn == 1:
                    canvas.itemconfig("chipCover" + id, state="normal")
            else : 
                color="#00ff00"; pos = RIGHT
                if numBtn == 1:
                    canvas.itemconfig("chipCover" + id, state="hidden")
            canvas.move(tag, pos*40 - 20,0)
            canvas.itemconfig(tag, fill=color)
       
    
def drawSwitch(canvas, x1,y1,fillSupport="#fffffe", fillSwitch="#ff0000", outSwitch="#000000", posSwitch=LEFT,tag=None, numBtn=1):
    canvas.create_arc(x1,y1, x1 + 20, y1 + 20, \
                        start=90, extent=180,  fill=fillSupport, outline=fillSupport,tags=tag) 
    canvas.create_arc(x1+20,y1 , x1 + 40, y1 + 20, \
                        start=270, extent=180,  fill=fillSupport, outline=fillSupport,tags=tag) 
    canvas.create_rectangle(x1+10,y1,x1+30,y1+20,fill=fillSupport, outline=fillSupport,tags=tag)
    canvas.create_oval(x1 +3+posSwitch*20,y1 + 3, x1 + 17 + posSwitch*20, y1 + 17,fill=fillSwitch, outline=outSwitch,tags="btn" + str(numBtn) + "_" + tag)
    canvas.addtag_withtag(tag, "btn" + str(numBtn) + "_" + tag)
    

def onDragMenu( event, canvas, tag):
    global xSouris, ySouris, dragMouseX, dragMouseY
    
    canvas.move(tag, event.x - dragMouseX, event.y - dragMouseY)
    dragMouseX, dragMouseY = event.x, event.y
        
def onStartDragMenu( event,canvas,tag):
    global dragMouseX, dragMouseY 
    
    dragMouseX, dragMouseY = event.x, event.y
    canvas.itemconfig(tag, fill="red")

def onStopDragMenu( event,canvas,tag):
    canvas.itemconfig(tag, fill="#ffffff")
    
def onCrossOver(event,canvas,tag):
    canvas.itemconfig("crossBg_" + tag, fill="#008000")

def onCrossLeave(event,canvas,tag):
    canvas.itemconfig("crossBg_" + tag, fill="")

def onCrossClick(event,canvas,tagMenu, tagRef):
    canvas.itemconfig( tagMenu, state="hidden")
    canvas.itemconfig( tagRef, outline="")

def drawMenu(canvas, xMenu, yMenu, thickness,label, tag, id):
    global imageIcoPdf
    
    rgba_color = (0, 0, 0, 255) 
    fillMenu= "#48484c"
    outMenu = "#909098"
    colorCross = "#e0e0e0"
    params = curDictCircuit.get(id)
    if params :
        [btn1, btn2, btn3] = params["btnMenu"]
        if btn1 == 0:
            color1="#808080"; pos1 = LEFT
        elif btn1 == 1:
            color1="#ff0000"; pos1 = LEFT
        else : color1="#00ff00"; pos1 = RIGHT
        if btn2 == 0:
            color2="#808080"; pos2 = LEFT
        elif btn2 == 1:
            color2="#ff0000"; pos2 = LEFT
        else : color2="#00ff00"; pos2 = RIGHT
        if btn3 == 0:
            color3="#808080"; pos3 = LEFT
        elif btn3 == 1:
            color3="#ff0000"; pos3 = LEFT
        else : color3="#00ff00"; pos3 = RIGHT

        roundedRect(canvas, xMenu, yMenu, 128,  128, 10, outline=outMenu, fill=fillMenu, thickness=thickness, tags = tag)
        canvas.create_rectangle(xMenu,      yMenu, xMenu + 114, yMenu + 17, fill="",outline="", tags="drag_" + tag)
        canvas.create_line(xMenu , yMenu + 17, xMenu + 127,  yMenu + 17, fill=outMenu, width=thickness, tags = tag)
        canvas.create_rectangle(xMenu + 110,      yMenu + 1, xMenu + 125, yMenu + 16, fill="",outline="", tags="crossBg_" + tag)
        canvas.create_line(xMenu + 115, yMenu + 5, xMenu + 120,  yMenu + 12, fill=colorCross, width=thickness*2, tags = "cross_" + tag)
        canvas.create_line(xMenu + 115, yMenu + 12, xMenu + 120,  yMenu + 5, fill=colorCross, width=thickness*2, tags = "cross_" + tag)
        drawChar(canvas, xMenu +63 , yMenu + 8 ,scaleChar=0.8,angle=0, text=label,color="#ffffff", anchor="center", tags = "title_" + tag)
        drawSwitch(canvas, xMenu+10, yMenu + 27,fillSwitch=color1, posSwitch=pos1, tag = "switch_" + tag,numBtn=1)
        canvas.tag_bind("btn1_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn1_switch_" + tag, id,1))
        drawAOP(canvas,xMenu + 82, yMenu + 32, scale=2, color="#000000",tags=tag)
        drawAOP(canvas,xMenu + 80, yMenu + 30, scale=2, tags=tag)
        drawSwitch(canvas, xMenu+10, yMenu + 60,fillSwitch=color2, posSwitch=pos2,tag = "switch_" + tag,numBtn=2)
        canvas.tag_bind("btn2_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn2_switch_" + tag, id,2))
        drawLabelPin(canvas,xMenu + 68, yMenu + 65, scale=2,color = "#000000", tags=tag)
        drawLabelPin(canvas,xMenu + 65, yMenu + 62, scale=2,color = "#faa000", tags=tag)
        drawLabelPin(canvas,xMenu + 88, yMenu + 65, scale=2,color = "#000000", tags=tag)
        drawLabelPin(canvas,xMenu + 85, yMenu + 62, scale=2,color = "#faa000", tags=tag)
        drawLabelPin(canvas,xMenu + 108, yMenu + 65, scale=2,color = "#000000", tags=tag)
        drawLabelPin(canvas,xMenu + 105, yMenu + 62, scale=2,color = "#faa000", tags=tag)
        drawSwitch(canvas, xMenu+10, yMenu + 93,fillSwitch=color3, posSwitch=pos3,tag = "switch_" + tag,numBtn=3)
        imgSave.append( canvas.create_image(xMenu+85, yMenu + 105, image=imageIcoPdf, tags=tag, anchor="center"))
        canvas.tag_bind("btn3_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn3_switch_" + tag, id,3))
        canvas.tag_raise("drag_" + tag)
        canvas.addtag_withtag(tag, "title_" + tag)
        canvas.addtag_withtag(tag, "crossBg_" + tag)
        canvas.addtag_withtag(tag, "cross_" + tag)
        canvas.addtag_withtag(tag,  "btn_" + tag)
        canvas.addtag_withtag(tag,  "drag_" + tag)
        canvas.addtag_withtag(tag,  "switch_" + tag)
        canvas.addtag_withtag("componentMenu",  tag)
        canvas.tag_bind("drag_" + tag,"<B1-Motion>", lambda event : onDragMenu(event,canvas, tag))
        canvas.tag_bind("drag_" + tag,"<Button-1>", lambda event : onStartDragMenu(event,canvas, "title_" + tag))
        canvas.tag_bind("cross_" + tag,"<Enter>", lambda event : onCrossOver(event, canvas, tag))
        canvas.tag_bind("cross_" + tag,"<Leave>", lambda event : onCrossLeave(event, canvas, tag))
        canvas.tag_bind("cross_" + tag,"<Button-1>", lambda event : onCrossClick(event, canvas, tag,  "activeArea" + id))
        canvas.tag_bind("drag_" + tag,"<ButtonRelease-1>", lambda event : onStopDragMenu(event,canvas, "title_" + tag))
        canvas.itemconfig(tag, state="hidden")
    

def onEnter( canvas, tag):
    global xSouris, ySouris 
    
    space=9
    tagCoords = canvas.coords(tag)
    canvas.move(tag, xSouris - tagCoords[0] - space,0)
    canvas.tag_raise(tag)
    canvas.itemconfig(tag, state="normal")
    
def onMenu( event,canvas, tagMenu, tagAll, tagRef, colorOut="#60d0ff"):
    canvas.tag_raise( tagMenu)
    canvas.itemconfig(tagAll , state="hidden")
    canvas.itemconfig(tagMenu, state="normal")
    canvas.itemconfig("componentActiveArea", outline="")
    canvas.itemconfig(tagRef, outline=colorOut)

# Fonction pour réinitialiser le curseur lorsqu'il sort de la zone
def onLeave( canvas, tag):
    canvas.itemconfig("bg_" + tag, state="hidden")
    canvas.itemconfig("symb_" + tag, state="hidden")
    canvas.itemconfig("pin_" + tag, state="hidden")
    canvas.itemconfig(tag, state="hidden")



def drawChip(canvas, xD, yD, scale=1, width = -1,  direction = HORIZONTAL, **kwargs):
    from dataComponent import dip14
    
    global numID
    
    if (width !=-1):
        scale = width / 9.0
    interSpace = 15*scale  
    space = 9*scale
    thickness = 1*scale
        
    dim = dip14
    open=NO
    internalFunc=None
    cursorOver = ""
    id = None
    tags = []
    for key, value in kwargs.items():
        if key == "pinCount"            : dim["pinCount"]       = value
        if key == "chipWidth"           : dim["chipWidth"]      = value
        if key == "label"               : dim["label"]          = value
        if key == "internalFunc"        : dim["internalFunc"]   = value
        if key == "open"                : open                  = value
        if key == "cursorOver"          : cursorOver            = value
        if key == "id"                  : id                    = value    
        if key == "tags"                : tags                  = value         
        if key == "type"                : type                  = value    
        
    dimLine = (dim["pinCount"] - 0.30)*interSpace/2
    dimColumn = dim["chipWidth"]*interSpace  
                
    params = {}
    if (id):                
        if (curDictCircuit.get(id)):
            params = curDictCircuit[id]
            tags = params["tags"]
    else: 
        idType[type] += 1
        id="_chip_" + str(numID)
        numID += 1
        
    if (not tags):
        params["id"]= id
        params["XY"]=(xD, yD)
        
        dimLine = (dim["pinCount"] - 0.30)*interSpace/2
        dimColumn = dim["chipWidth"]*interSpace  
        label = dim["label"] + "-" + str(idType[type])
        params["label"] = label
        params["type"] = type
        params["btnMenu"] = [1,1,0]
        nbBrocheParCote = dim["pinCount"] // 2
        tagBase = "base" + id
        tagMenu = "menu" + id
        tagCapot = "chipCover" + id
        tagSouris = "activeArea" + id
        for i in range(dim["pinCount"]):
            canvas.create_rectangle(xD + 2*scale+(i%nbBrocheParCote)*interSpace,      yD-(0 - (i//nbBrocheParCote)*(dimColumn + 0)), \
                                    xD + 11*scale+(i%nbBrocheParCote)*interSpace,     yD-(3*scale - (i//nbBrocheParCote)*(dimColumn + 6*scale)), \
                                    fill="#909090",outline="#000000", tags=tagBase)
            canvas.create_polygon(xD + 2*scale + (i%nbBrocheParCote)*interSpace,        yD-space//3 - (0-(i//nbBrocheParCote)*(dimColumn + 2*space//3)), \
                                xD + space//3+ 2*scale +(i%nbBrocheParCote)*interSpace,   yD-(2*space)//3 - (0-(i//nbBrocheParCote)*(dimColumn + (4*space)//3)), \
                                xD + (2*space)//3+ 2*scale +(i%nbBrocheParCote)*interSpace, yD-(2*space)//3 - (0-(i//nbBrocheParCote)*(dimColumn + (4*space)//3)), \
                                xD+(11+(i%nbBrocheParCote)*15)*scale,         yD-space//3 - (0-(i//nbBrocheParCote)*(dimColumn + 2*space//3)), \
                                fill="#b0b0b0",outline="#000000", smooth=False, tags=tagBase)
        
        zone = roundedRect(canvas, xD, yD, dimLine,  dimColumn, 5, outline="#343434", fill="#343434",thickness=thickness, tags=tagBase)
        
        params["tags"] = [tagBase]
        canvas.create_rectangle(xD + 2*scale,      yD + 2*scale, \
                                xD - 2*scale+ dimLine,     yD-2*scale + dimColumn, \
                                fill="#000000",outline="#000000", tags=tagBase)
        if dim["internalFunc"] != None:
            dim["internalFunc"](canvas,xD , yD ,scale=scale, tags=tagBase, \
                                **kwargs )

        roundedRect(canvas, xD, yD, dimLine,  dimColumn, 5, outline="#343434", fill="#343434",thickness=thickness, tags=tagCapot)
        canvas.create_line(xD , yD+1*space//3, xD + dimLine, yD + 1*space//3, fill="#b0b0b0", width=thickness, tags=tagCapot)
        canvas.create_line(xD , yD + dimColumn - 1*space//3, xD + dimLine, yD + dimColumn - 1*space//3, fill="#b0b0b0", width=thickness, tags=tagCapot)
        canvas.create_oval(xD + 4*scale, yD + dimColumn - 1*space//3 - 6*scale, xD + 8*scale, yD + dimColumn - 1*space//3 - 2*scale, fill='#ffffff', outline='#ffffff', tags=tagCapot)
        canvas.create_arc(xD - 5*scale, yD + dimColumn//2 - 5*scale, xD + 5*scale, yD + dimColumn//2 + 5*scale, start=270, extent=180, fill='#000000', outline='#505050', style=tk.PIESLICE, tags=tagCapot)
        drawChar(canvas, xD + dimLine//2, yD + dimColumn//2 ,scale=scale,angle=0, text=label,color="#ffffff", anchor="center", tags=tagCapot)  # xD + 30*scale,yD - 10*scale
        canvas.create_rectangle(xD + 2*scale,      yD + 2*scale, \
                                xD - 2*scale+ dimLine,     yD-2*scale + dimColumn, \
                                fill="",outline="", tags=tagSouris)
        canvas.tag_raise(tagCapot)
        canvas.tag_raise(tagSouris)
        canvas.addtag_withtag("componentActiveArea",  tagSouris)
        if open:
            canvas.itemconfig(tagCapot, state="hidden")
        else:
            params["tags"].append(tagCapot)
        curDictCircuit[id]=params
        drawMenu(canvas,xD + dimLine + 2.3*scale + space*0, yD - space,thickness,label, tagMenu, id)
        canvas.tag_bind(tagSouris, "<Button-2>", lambda event: onMenu( event,canvas, tagMenu,"componentMenu",tagSouris))
    else :
        X, Y= params["XY"]
        dX = xD - X
        dY = yD - Y
        for tg in tags:
            canvas.move(tg,dX ,dY)
        
    return  xD + dimLine + 2.3*scale, yD


def getXY(column, line, scale=1, **kwargs):
    interSpace = 15*scale  
    space = 9*scale
    thickness = 1*scale
    matrix = matrix830pts
    for key, value in kwargs.items():
        if key == "matrix"   : matrix      = value     
        
    id = str(column) +"," + str(line)
    x,y = matrix[id]["xy"]
    
    return x*scale, y*scale

def drawWire(canvas, xD, yD, scale=1, width = -1,  direction = HORIZONTAL, **kwargs) :
    global numID
    
    if (width !=-1):
        scale = width / 9.0
    interSpace = 15*scale  
    space = 9*scale
    thickness = 1*scale
    matrix = matrix830pts
    id = None
    for key, value in kwargs.items():
        if key == "color"   : color     = value
        if key == "mode"      : mode        = value    
        if key == "coords"    : coords      = value  
        if key == "matrix"   : matrix     = value    
        if key == "id"        : id          = value    
        if key == "tags"      : tags        = value    
    
    params = {}
    if (id):                # supprime l'ancien câble si existant id != None
        if (curDictCircuit.get(id)):
            params = curDictCircuit[id]
            tags = params["tags"]
            for tg in tags:
                canvas.delete(tg)
    else: 
        id="_wire_" + str(numID)
        numID += 1
    
    params["id"]= id
    params["mode"]=mode
    #params["matrix"] = matrix
    params["coord"] = coords
    xO, yO, xF, yF = coords[0] 
    xO, yO = getXY(xO,yO,scale=scale,matrix=matrix)
    xF, yF = getXY(xF,yF,scale=scale,matrix=matrix)
    params["XY"]=(xO,yO, xF, yF)
    params["color"]=color
    encre = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
    contour = f"#{color[0]//2:02x}{color[1]//2:02x}{color[2]//2:02x}"
    canvas.create_oval(xD + xO + 2*space/9, yD + yO + 2*space/9, xD + xO + 7*space/9, yD + yO + 7*space/9, fill='#dfdfdf', outline='#404040', width=1*thickness, tags=id)
    canvas.create_oval(xD + xF + 2*space/9, yD + yF + 2*space/9, xD + xF + 7*space/9, yD + yF + 7*space/9, fill='#dfdfdf', outline='#404040', width=1*thickness, tags=id)

    divY  = yF - yO if yF != yO else 0.000001
    xDiff = (space/2)*(1 - math.cos(math.atan((xF-xO)/divY)))
    yDiff = (space/2)*(1 - math.sin(math.atan((xF-xO)/divY)))
    p1    = ( (xO + xDiff), (yO + space - yDiff))
    p2    = ( (xF + xDiff), (yF + space - yDiff))
    p3    = ( (xF + space - xDiff), (yF + yDiff))
    p4    = ( (xO+ space - xDiff), (yO + yDiff))
    canvas.create_polygon(xD + p1[0], yD + p1[1], xD + p2[0], yD + p2[1], \
                         xD + p3[0], yD + p3[1], xD + p4[0], yD + p4[1], \
                         fill=encre, outline=contour, width=1*thickness, tags=id )  

    params["tags"] = [id]
    curDictCircuit[id] = params

    return xD, yD
