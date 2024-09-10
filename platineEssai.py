import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageGrab
from tkinter import font
import math


#    ligneDistribution  = [(trou, 63)]  
#    blocAlim           = [(trou,5), (plat,1)]

PERSO                       = 0
HORIZONTAL                  = 1 
VERTICAL                    = 2 
VERTICAL_FIN_HORIZONTAL     = 3
AUTO                        = 0
DIRECT                      = 1
LIBRE                       = 0
OCCUPE                      = 1
NON                         = 0
OUI                         = 1
GAUCHE                      = 0
DROITE                      = 1
RIEN                        = (0, 0)
CUR_CLE_ANGLAISE            = {"path":"Icones/CleAnglaise_32.png", "imageId": None}
CUR_TOURNEVIS               = {"path":"Icones/TourneVis_48.png", "imageId": None}
CUR_CADENAS                 = {"path":"Icones/Cadenas_48.png", "imageId": None}
ICO_PDF                     = {"path":"Icones/pdf-icon-png-2079.png", "imageId": None}

curseur_cleA = "@CleAnglaise_16.xbm white black"

imgSave = []
idOrigines = {"xyOrigine":(0,0)}
curseurCourant = None
curseurSauve = None
baseDictCircuit = {}
idType = {}
curDictCircuit = baseDictCircuit
numID = 1
xSouris, ySouris = 0,0
xDragSouris, yDragSouris = 0,0

def setDictCircuit(dico = baseDictCircuit, **kwargs):
    curDictCircuit = dico    

def suivreSouris(event, canvas):
    global xSouris, ySouris 
    
    #canvas.tag_raise(curseurCourant)
    #canvas.coords(curseurCourant, event.x-32, event.y-32)
    #canvas.update_idletasks()
    xSouris, ySouris = event.x, event.y
    
def initImgIdCurseur(canvas):
    global CUR_CLE_ANGLAISE, CUR_TOURNEVIS, CUR_CADENAS
    
    image       = Image.open(CUR_TOURNEVIS["path"])
    imagePhoto  = ImageTk.PhotoImage(image)
    CUR_TOURNEVIS["imageId"] = canvas.create_image(1000, 150, image=imagePhoto)
    canvas.itemconfig(CUR_TOURNEVIS["imageId"] , state='hidden')
    imgSave.append(imagePhoto)
    image       = Image.open(CUR_CADENAS["path"])
    imagePhoto  = ImageTk.PhotoImage(image)
    CUR_CADENAS["imageId"] = canvas.create_image(1000, 150, image=imagePhoto)
    canvas.itemconfig(CUR_CADENAS["imageId"] , state='hidden')
    imgSave.append(imagePhoto)
    image       = Image.open(CUR_CLE_ANGLAISE["path"])
    imagePhoto  = ImageTk.PhotoImage(image)
    CUR_CLE_ANGLAISE["imageId"] = canvas.create_image(1000, 150, image=imagePhoto)
    canvas.itemconfig(CUR_CLE_ANGLAISE["imageId"] , state='hidden')
    imgSave.append(imagePhoto)
    
    return CUR_CLE_ANGLAISE
        
def init(canvas):
    global curseurCourant, imageIcoPdf, idOrigines, curseurSauve, idType, curDictCircuit, numID, xSouris, ySouris, xDragSouris, yDragSouris
    
    imgSave = []
    idOrigines = {"xyOrigine":(0,0)}
    curseurCourant = None
    curseurSauve = None
    baseDictCircuit = {}
    #idType = {}
    curDictCircuit = baseDictCircuit
    numID = 1
    xSouris, ySouris = 0,0
    xDragSouris, yDragSouris = 0,0
    idType.update({"dip14":0,"74HC00":0,"74HC02":0,"74HC08":0,"74HC04":0,"74HC32":0})

    
    canvas.config(cursor="")
    curseur = initImgIdCurseur(canvas)
    if curseur["imageId"] == None:
        image       = Image.open(curseur["path"])
        imagePhoto  = ImageTk.PhotoImage(image)
        curseur["imageId"] = canvas.create_image(1000, 150, image=imagePhoto)
        imgSave.append(imagePhoto)
    image       = Image.open(ICO_PDF["path"])
    
    imageIcoPdf  = ImageTk.PhotoImage(image.resize((32,32)))    
    #canvas.itemconfig(curseur["imageId"] , state='normal')   
    #curseurCourant = curseur["imageId"]
    canvas.bind("<Motion>", lambda event:  suivreSouris(event, canvas))
    
def captureZoneCanvas(canvas, x1, y1, x2, y2):
    # Convertir les coordonnées canvas en coordonnées de l'écran
    x1 = canvas.winfo_rootx() + x1
    y1 = canvas.winfo_rooty() + y1
    x2 = canvas.winfo_rootx() + x2
    y2 = canvas.winfo_rooty() + y2
    
    # Capturer la zone spécifiée directement à partir de l'écran
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    return image

def imageDuTexte(texte, angle=90, fontPath="FiraCode-Light", fontTaille=15, couleur=(0, 0, 0, 255), size=(15,15) ):

    police = ImageFont.truetype(fontPath, fontTaille)

    #imgTemp = Image.new('RGBA', (1, 1))
    #draw = ImageDraw.Draw(imgTemp)

    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    draw.text((0, 0), texte, font=police, fill=couleur)
    
    imageRot = image.rotate(angle, expand=1)
    
    return ImageTk.PhotoImage(imageRot)
    

def rectangleArrondi(canvas, x, y, largeur, hauteur, rayon, **kwargs):
    x2 = x + largeur
    y2 = y + hauteur
    points = [
        x + rayon, y,
        x2 - rayon, y,
      #  x2, y,
        x2, y + rayon,
        x2, y2 - rayon,
    #    x2, y2,
        x2 - rayon, y2,
        x + rayon, y2,
    #    x, y2,
        x, y2 - rayon,
        x, y + rayon,
    #    x, y
    ]
    tag=""
    for key, value in kwargs.items():
        if key == "tags"           : tag            = value
        if key == "fill"           : fill           = value
        if key == "width"          : epaisseur      = value
        
   
    # Draw four arcs for corners
    canvas.create_arc(x, y, x + 2*rayon, y + 2*rayon, start=90, extent=90, style=tk.PIESLICE, **kwargs)
    canvas.create_arc(x2 - 2*rayon, y, x2, y + 2*rayon, start=0, extent=90, style=tk.PIESLICE, **kwargs)
    canvas.create_arc(x2 - 2*rayon, y2 - 2*rayon, x2, y2, start=270, extent=90, style=tk.PIESLICE,  **kwargs)
    canvas.create_arc(x, y2 - 2*rayon, x + 2*rayon, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs)
    #kwargs["outline"] = fill
    canvas.create_polygon(points, smooth=False, **kwargs)
    canvas.create_line(x + rayon, y,x, y + rayon,fill=fill, width=epaisseur, tags=tag)
    canvas.create_line(x2 - rayon, y, x2, y + rayon, fill=fill, width=epaisseur, tags=tag)
    canvas.create_line(x2 - rayon, y2, x2 , y2 - rayon, fill=fill, width=epaisseur, tags=tag)
    canvas.create_line(x, y2 - rayon, x + rayon, y2, fill=fill, width=epaisseur, tags=tag)

    
def setXYOrigine(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    xO, yO = xD, yD
    idOrigine = "xyOrigine"
    for key, value in kwargs.items():
        if key == "idOrigine": idOrigine    = value
        #if key == "xyOrigine": xO, yO       = value
        
    idOrigines[idOrigine]=(xD,yD)
    return (xO , yO )

def goXY(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    idOrigine = "xyOrigine"
    for key, value in kwargs.items():
        if key == "ligne":  ligne    = value
        if key == "colonne": colonne = value
        if key == "idOrigine": idOrigine    = value
        
    xO, yO = idOrigines[idOrigine]
       
    return (xO + colonne*15*echelle, yO + ligne*15*echelle)
    
def car(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    global imgText
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    angle = 90
    for key, value in kwargs.items():
        if key == "angle": angle = value 
    couleur = "#000000"
    texte = "-"
    deltaY = 0
    echelleCar=1
    taille = (int(interSpace*1),int( interSpace*1))
    anchor = "center"
    tags=""
    for key, value in kwargs.items():
        if   key == "couleur"       : couleur       = value 
        elif key == "texte"         : texte         = value 
        elif key == "deltaY"        : deltaY        = value 
        elif key == "echelleCar"    : echelleCar    = value
        elif key == "anchor"        : anchor        = value
        elif key == "tags"          : tags          = value
        
    taille = (int(echelleCar*interSpace*len(texte)),int(echelleCar*interSpace)) 
    firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=int(15*echelle*echelleCar))
    if angle !=0:
        #imgText = imageDuTexte(texte=texte, angle=angle, couleur=couleur,fontTaille = taille[1], size=taille )
        #canvas.create_image(xD, yD + deltaY*space , image=imgText, anchor=tk.CENTER)   fontPath="FiraCode-Light"
        firaCodeFont = font.Font(family="FiraCode-Light", size=int(15*echelleCar*echelle))
        canvas.create_text(xD , yD + deltaY*space , text=texte, font=firaCodeFont, fill=couleur, anchor=anchor,angle=angle, tags=tags)
    else: canvas.create_text(xD , yD , text=texte, font=firaCodeFont, fill=couleur, anchor=anchor, tags=tags)
    #imgSave.append(imgText)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)


def carIter(canvas, xD,yD,echelle=1,largeur=-1, sens = VERTICAL_FIN_HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    
    for key, value in kwargs.items():
        if key == "carDeb"          : carDeb      = value 
        elif key == "nbCar"         : nbCar       = value 
        
    x = xD
    y = yD
    s = sens
    if sens == VERTICAL_FIN_HORIZONTAL: s = VERTICAL
    for i in range(nbCar):
        texte = chr(ord(carDeb) + nbCar - i-1)
        (x, y) = car (canvas, x,y,echelle,largeur, s , texte=texte, **kwargs )

    if sens == VERTICAL_FIN_HORIZONTAL: sens = HORIZONTAL
    
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace * nbCar     
    
    return (xD  , yD)
        
def numIter(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    
    for key, value in kwargs.items():
        if key == "numDeb"          : numDeb      = value 
        elif key == "numFin"         : numFin       = value 
    x = xD + 3*echelle
    y = yD
    
    
    for i in range(numDeb,numFin+1):
        texte = str(i)
        (x, y) = car(canvas, x,y,echelle,largeur, sens=sens , texte=texte, echelleCar=0.7, **kwargs )

  
    
    if sens == HORIZONTAL:
        xD += interSpace * (numFin - numDeb)  
    elif sens == VERTICAL: yD += interSpace    
    
    return (xD  , yD)    
         

def trouCarre(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space       = 9*echelle
    interSpace  = 15*echelle
    
    couleurSombre, couleurClaire, couleurTrou = '#c0c0c0', '#f6f6f6', "#484848"
    for key, value in kwargs.items():
        if key == "couleurs"     : couleurSombre, couleurClaire, couleurTrou           = value
 
    canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill=couleurSombre, outline=couleurSombre)
    canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill=couleurClaire, outline=couleurClaire)
    canvas.create_rectangle(xD+space//3, yD+space//3, xD+2*space//3,yD+2*space//3,fill=couleurTrou,outline=couleurTrou)
    
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def trouRond(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space       = 9*echelle
    interSpace  = 15*echelle
    
    couleurSombre, couleurClaire, couleurTrou = '#c0c0c0', '#f6f6f6', "#484848"
    for key, value in kwargs.items():
        if key == "couleurs"     : couleurSombre, couleurClaire, couleurTrou           = value
 
    canvas.create_arc(xD, yD, xD + space, yD + space, start=45, extent= 225, style= tk.PIESLICE ,fill=couleurSombre,  outline=couleurSombre) #x, y2 - 2*rayon, x + 2*rayon, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs
    canvas.create_arc(xD, yD, xD + space, yD + space, start=225, extent= 45, style= tk.PIESLICE , fill=couleurClaire, outline=couleurClaire)
    canvas.create_oval(xD+space//3, yD+space//3, xD+2*space//3,yD+2*space//3,fill=couleurTrou,outline=couleurTrou)
    
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

foncTrou = {"fonction":trouCarre}

def trou(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs):
    global foncTrou

    return foncTrou["fonction"](canvas, xD,yD,echelle,largeur, sens , **kwargs)
    

def setFoncTrou(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    global foncTrou
    
    fonction = trouCarre
    for key, value in kwargs.items():
        if key == "fonction"     : fonction   = value
        
    foncTrou = {"fonction" : fonction }
    
    return xD, yD

def plat(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    interSpace = 15*echelle  
    
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace  
    
    return (xD ,yD)

def demiPlat(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    interSpace = 15*echelle  
    
    if sens == HORIZONTAL:
        xD += interSpace/2
    elif sens == VERTICAL: yD += interSpace /2 
    
    return (xD ,yD)

def rail(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs):
    if (largeur !=-1):
        echelle = largeur / 9.0

    couleur = "black"
    for key, value in kwargs.items():
        if key == "couleur": couleur = value 
    interSpace = 15*echelle  
    epaisseur = 2*echelle
    canvas.create_line(xD + interSpace//3, yD+interSpace//2, xD + interSpace*1.5, yD + interSpace//2, fill=couleur, width=epaisseur)
    
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace  
    
    return (xD ,yD)

def railRouge(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs):
    if (largeur !=-1):
        echelle = largeur / 9.0

    interSpace = 15*echelle  
    #epaisseur = 2*echelle
    
    (x,y) = rail(canvas, xD,yD-interSpace//2,echelle,largeur,sens,couleur="red")
    
    return (x, yD)

pe830pts = {"lgLigne":66, "lgColonne":22, "sepAlim":[(0,4),(0,18.5)], "sepDistribution":[(0,10.7)]}

def planche(canvas,xD=0,yD=0,echelle=1,largeur=-1, sens = VERTICAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0
    interSpace = 15*echelle 
    epaisseur = 1*echelle
    
    dim=pe830pts
    couleur ="#F5F5DC"
    sepAlim = dim["sepAlim"]
    sepDist = dim["sepDistribution"]
    for key, value in kwargs.items():
        if key == "lgLigne"             : dim["lgLigne"]        = value
        if key == "lgColonne"           : dim["lgColonne"]      = value
        if key == "couleur"             : couleur               = value
        if key == "sepAlim"             : sepAlim               = value
        if key == "sepDistribution"     : sepDist               = value
        
    epaisseur = 1*echelle   
    dimLigne = dim["lgLigne"]*interSpace
    dimColone = dim["lgColonne"]*interSpace   
    #sepAlim =  [] if not dim.get("sepAlim") else dim.get("sepAlim")
    #sepDistribution =  [] if not dim.get("sepDistribution") else dim.get("sepDistribution")
    rectangleArrondi(canvas, xD, yD, dimLigne,  dimColone, 20, outline=couleur, fill=couleur, width=epaisseur)
    for sepA in sepAlim:
        canvas.create_line(xD + interSpace*sepA[0], yD+interSpace*sepA[1], xD - interSpace*sepA[0] + dimLigne, yD + interSpace*sepA[1], fill="#707070", width=epaisseur) 
    facteurNoirceur = 0.9
    r = int(couleur[1:3],16) * (facteurNoirceur + 0.06)
    r = int(max(0, min(255, r)))
    g = int(couleur[3:5],16) * (facteurNoirceur + 0.06)
    g = int(max(0, min(255, g)))
    b = int(couleur[5:7],16) * (facteurNoirceur + 0.06)
    b = int(max(0, min(255, b)))
    c = ["#{:02x}{:02x}{:02x}".format(r, g, b)]
    r = int(couleur[1:3],16) * (facteurNoirceur )
    r = int(max(0, min(255, r)))
    g = int(couleur[3:5],16) * (facteurNoirceur )
    g = int(max(0, min(255, g)))
    b = int(couleur[5:7],16) * (facteurNoirceur )
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= facteurNoirceur; g *= facteurNoirceur; b *= facteurNoirceur; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= facteurNoirceur; g *= facteurNoirceur; b *= facteurNoirceur; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    r *= facteurNoirceur; g *= facteurNoirceur; b *= facteurNoirceur; 
    r = int(max(0, min(255, r)))
    g = int(max(0, min(255, g)))
    b = int(max(0, min(255, b)))
    c.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    for sepD in sepDist:      
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1], xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1], fill=c[1], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1] + epaisseur, fill=c[2], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + 2*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1]  + 2*epaisseur, fill=c[3], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + 3*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1]  + 3*epaisseur, fill=c[4], width=epaisseur)    
        for dy in range(4,11):
            canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + dy*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1] + dy*epaisseur, fill=c[0], width=epaisseur)   
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - 4*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1]+interSpace - 4*epaisseur, fill=c[1], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - 3*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1] + interSpace - 3*epaisseur, fill=c[2], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1]+ interSpace - 2*epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1]  + interSpace - 2*epaisseur, fill=c[3], width=epaisseur)    
        canvas.create_line(xD +interSpace*sepD[0], yD+interSpace*sepD[1] + interSpace - epaisseur, xD + dimLigne - interSpace*sepD[0], yD + interSpace*sepD[1] + interSpace - epaisseur, fill=c[4], width=epaisseur)    
    #canvas.create_line(xD , yD+interSpace*11+interSpace//3, xD + dimLigne, yD + interSpace*11+interSpace//3, fill="#c0c0c0", width=(3*interSpace)//5)    
    # if sens == HORIZONTAL:
    #     xD += dimLigne
    # else: yD += dimColone  
    
    return (xD ,yD)

################ BOITIERS DIP ####################################

def connexionBroche(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
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
    
def dessinerLabelBroche(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle   
    couleur="#ffffff" 
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "couleur"     : couleur       = value
        
    canvas.create_rectangle(xD, yD, xD + 4*interSpace//15,yD + orientation*4*interSpace//15,fill=couleur,outline=couleur, tags=tag)
    canvas.create_polygon(xD, yD + orientation*4*interSpace//15, xD + 4*interSpace//15 , yD + orientation*4*interSpace//15, xD + 2*interSpace//15 , yD + orientation*7*interSpace//15, fill=couleur, outline=couleur, tags=tag)

def inv(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle   
    couleur="#ffffff" 
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "couleur"     : couleur       = value
    
    canvas.create_oval(xD + 9*interSpace//15, yD + orientation*2.5*interSpace//15, xD + 11*interSpace//15, yD + orientation*4.5*interSpace//15, fill=couleur, outline=couleur, tags=tag)    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')

def dessinerOR(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value
        
    canvas.create_rectangle(xD, yD, xD + 3*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill="#ffffff", width=1, tags=tag)

    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 3*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=270, extent=180,  fill="#000000", outline="#000000", tags=tag) 
    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=-90, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 

def symbOR(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    #canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill='#c0c0c0', outline='#c0c0c0')
    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')
   # canvas.create_rectangle(xD, yD, xD + 3*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    #  canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 3*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=270, extent=180,  fill="#000000", outline="#000000", tags=tag) 
    # canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=-90, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 
    # canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=-90, extent=90,  fill="#ffffff", outline="#ffffff") 
     
    dessinerOR(canvas, xD,yD,echelle=echelle,largeur=largeur, sens = sens,  orientation = orientation, **kwargs )
    connexionBroche(canvas, xD, yD,echelle=echelle,largeur=largeur,sens=sens, orientation=orientation, **kwargs)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def symbNOR(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    #canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill='#c0c0c0', outline='#c0c0c0')
    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')
    # canvas.create_rectangle(xD, yD, xD + 3*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    # #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    # canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 3*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=270, extent=180,  fill="#000000", outline="#000000", tags=tag) 
    # canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=-90, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 
#    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
#                      start=-90, extent=90,  fill="#ffffff", outline="#ffffff") 
    dessinerOR(canvas, xD,yD,echelle=echelle,largeur=largeur, sens = sens,  orientation = orientation, **kwargs )
    inv(canvas,xD, yD, echelle=echelle, largeur=largeur, sens=sens, orientation=orientation, **kwargs)
    connexionBroche(canvas, xD, yD,echelle=echelle,largeur=largeur,sens=sens, orientation=orientation, **kwargs)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def dessinerAOP(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    couleur="#ffffff"
    for key, value in kwargs.items():
        if key == "tags"        : tag           = value
        if key == "couleur"     : couleur       = value

    canvas.create_polygon(xD, yD, xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD  , yD + orientation*7*interSpace//15, fill=couleur, outline=couleur, tags=tag)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill=couleur, width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD + 3*interSpace//15, yD + orientation*5*interSpace//15, fill=couleur, width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*2*interSpace//15, xD + 3*interSpace//15, yD + orientation*2*interSpace//15, fill=couleur, width=1, tags=tag)
   

def symbNOT(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    #canvas.create_polygon(xD, yD, xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD  , yD + orientation*7*interSpace//15, fill='#ffffff', outline='#ffffff', tags=tag)
    dessinerAOP(canvas,xD, yD, echelle=echelle, largeur=largeur, sens=sens, orientation=orientation, **kwargs)
    inv(canvas,xD, yD, echelle=echelle, largeur=largeur, sens=sens, orientation=orientation, **kwargs)
    #canvas.create_rectangle(xD, yD, xD + 3*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff")
    #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    #canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 3*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                  start=270, extent=180,  fill="#000000", outline="#000000") 
    #canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                  start=-90, extent=180,  fill="#ffffff", outline="#ffffff") 
#    canvas.create_arc(xD  - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
#                      start=-90, extent=90,  fill="#ffffff", outline="#ffffff") 
    connexionBroche(canvas, xD, yD,echelle=echelle,largeur=largeur,sens=sens, orientation=orientation, **kwargs)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def dessinerAND(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    canvas.create_rectangle(xD, yD, xD + 6*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    canvas.create_line(xD + 9*interSpace//15 , yD + orientation*3.5*interSpace//15, xD + 12*interSpace//15, yD + orientation*3.5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*5*interSpace//15, xD + 3*interSpace//15, yD + orientation*5*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_line(xD - 3*interSpace//15, yD + orientation*2*interSpace//15, xD + 3*interSpace//15, yD + orientation*2*interSpace//15, fill="#ffffff", width=1, tags=tag)
    canvas.create_arc(xD + 6*interSpace//15 - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
                      start=270, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 


def symbAND(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    #canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill='#c0c0c0', outline='#c0c0c0')
    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')
    # canvas.create_rectangle(xD, yD, xD + 6*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    # #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    # canvas.create_arc(xD + 6*interSpace//15 - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=270, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 
    dessinerAND(canvas, xD,yD,echelle=echelle,largeur=largeur, sens = sens,  orientation = orientation, **kwargs )
    connexionBroche(canvas, xD, yD,echelle=echelle,largeur=largeur,sens=sens, orientation=orientation,**kwargs)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)

def symbNAND(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL,  orientation = 1, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle
    for key, value in kwargs.items():
        if key == "tags"     : tag       = value

    #canvas.create_polygon(xD, yD+space, xD, yD, xD+space, yD, fill='#c0c0c0', outline='#c0c0c0')
    #canvas.create_polygon(xD, yD+space, xD+space, yD+space, xD+space, yD, fill='#f6f6f6', outline='#f6f6f6')
    # canvas.create_rectangle(xD, yD, xD + 6*interSpace//15,yD + orientation*7*interSpace//15,fill="#ffffff",outline="#ffffff", tags=tag)
    # #canvas.create_line(xD + 1*interSpace//2, yD, xD + 1*interSpace//2, yD + 2*interSpace//3, fill="#ffffff", width=1)
    # canvas.create_arc(xD + 6*interSpace//15 - 3*interSpace//15, yD, xD + 9*interSpace//15 , yD + orientation*7*interSpace//15, \
    #                   start=270, extent=180,  fill="#ffffff", outline="#ffffff", tags=tag) 
    dessinerAND(canvas, xD,yD,echelle=echelle,largeur=largeur, sens = sens,  orientation = orientation, **kwargs )
    inv(canvas,xD, yD, echelle=echelle, largeur=largeur, sens=sens, orientation=orientation, **kwargs)
    connexionBroche(canvas, xD, yD,echelle=echelle,largeur=largeur,sens=sens, orientation=orientation, **kwargs)
    if sens == HORIZONTAL:
        xD += interSpace
    elif sens == VERTICAL: yD += interSpace      
    
    return (xD  , yD)




def foncInterne(canvas, xD,yD,echelle=1,largeur=-1, sens = HORIZONTAL, **kwargs ):
    if (largeur !=-1):
        echelle = largeur / 9.0

    space = 9*echelle
    interSpace = 15*echelle    
    io = []
    for key, value in kwargs.items():
        if key == "fonctionLogique"     : fonctionLogique       = value
        if key == "io"                  : io                    = value
        if key == "nbBroches"           : nbBroches             = value
        if key == "largeurBoitier"      : largeurBoitier        = value
    dimColone = largeurBoitier*interSpace  
    for pin in io:
        p = pin[1][0]
        orientation = 1 - 2*((p -1)*2 // nbBroches)
        if p > nbBroches//2: p = 15 - p 
        x = xD + 2*echelle + space//2 + (p - 2)*interSpace + 3*interSpace//15
        y = yD  + dimColone//2 + orientation*0.2*interSpace
        fonctionLogique(canvas,x,y,echelle=echelle, largeur=largeur, sens=sens,orientation=orientation, **kwargs)
        
# def initBoitiers():
#     global dip14, dip7400, dip7402, dip7404, dip7408, dip7432, capotOuvert, capotFerme, dip20, dip60, dip120, idType, pins7400, pins7402, pins7404, pins7408, pins7432
    
dip14 = {"nbBroches":14, "largeurBoitier":2.4, "label":"DIP 14", "cursorOver":CUR_CADENAS, "type":"dip14"}
dip7400 = dip14.copy()
dip7400["label"] = "74HC00"  # 74HC00
dip7400["type"] = "74HC00"  # 74HC00
dip7402 = dip14.copy()
dip7402["label"] = "74HC02"  # 74HC02
dip7402["type"] = "74HC02"  # 74HC02
dip7408 = dip14.copy()
dip7408["label"] = "74HC08"  # 74HC08
dip7408["type"] = "74HC08"  # 74HC08
dip7404 = dip14.copy()
dip7404["label"] = "74HC04"  # 74HC04
dip7404["type"] = "74HC04"  # 74HC04
dip7432 = dip14.copy()
dip7432["label"] = "74HC32"  # 74HC32
dip7432["type"] = "74HC32"  # 74HC32
capotOuvert = {"ouvert": OUI}
capotFerme  = {"ouvert": NON}
dip20 = {"nbBroches":20, "largeurBoitier":2.4, "label":"DIP 20", "type": "dip20"}
dip60 = {"nbBroches":60, "largeurBoitier":2.4, "label":"DIP 60", "type": "dip60"}
dip120 = {"nbBroches":120, "largeurBoitier":2.4, "label":"DIP 120", "type": "dip120"}
idType.update({"dip14":0,"74HC00":0,"74HC02":0,"74HC08":0,"74HC04":0,"74HC32":0})

pins7400 = {"fonctionLogique":symbNAND, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7402 = {"fonctionLogique":symbNOR, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7404 = {"fonctionLogique":symbNOT, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7408 = {"fonctionLogique":symbAND, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7432 = {"fonctionLogique":symbOR, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
    

# Fonction pour changer le curseur lorsqu'il entre dans la zone
# def on_enter( canvas, cursorOver):
#     global curseurCourant,curseurSauve
    
#     #canvas.config(cursor=cursorOver)
#     if cursorOver["imageId"] == None:
#         image       = Image.open(cursorOver["path"])
#         imagePhoto  = ImageTk.PhotoImage(image)
#         cursorOver["imageId"] = canvas.create_image(1000, 150, image=imagePhoto)
#         imgSave.append(imagePhoto)
#     canvas.itemconfig(cursorOver["imageId"] , state='normal')   
#     curseurSauve = curseurCourant
#     curseurCourant = cursorOver["imageId"]

#     image = Image.new('RGBA', (64,128), (128, 128, 128, 1))
#     draw = ImageDraw.Draw(image)
#     draw.rounded_rectangle([(0,0), (63,127)],radius=20,outline="black")
#     imgMenu = ImageTk.PhotoImage(image)
#     canvas.create_image(640, 60, image=imgMenu, anchor=tk.NW)
#     imgSave.append(imgMenu)
def onSwitch( event, canvas, tag, id, numBtn):
    params = curDictCircuit.get(id)
    if params:
        btn = params["btnMenu"][numBtn - 1]
        if btn > 0 :
            btn = abs(btn - 2) + 1
            params["btnMenu"][numBtn - 1] = btn
            if btn == 1:
                coul="#ff0000"; pos = GAUCHE
                if numBtn == 1:
                    canvas.itemconfig("capot" + id, state="normal")
            else : 
                coul="#00ff00"; pos = DROITE
                if numBtn == 1:
                    canvas.itemconfig("capot" + id, state="hidden")
            canvas.move(tag, pos*40 - 20,0)
            canvas.itemconfig(tag, fill=coul)
       
    
def dessinerInter(canvas, x1,y1,fillSupport="#fffffe", fillBouton="#ff0000", outBouton="#000000", posBouton=GAUCHE,tag=None, numBtn=1):
    #pass
    canvas.create_arc(x1,y1, x1 + 20, y1 + 20, \
                        start=90, extent=180,  fill=fillSupport, outline=fillSupport,tags=tag) 
    canvas.create_arc(x1+20,y1 , x1 + 40, y1 + 20, \
                        start=270, extent=180,  fill=fillSupport, outline=fillSupport,tags=tag) 
    canvas.create_rectangle(x1+10,y1,x1+30,y1+20,fill=fillSupport, outline=fillSupport,tags=tag)
    canvas.create_oval(x1 +3+posBouton*20,y1 + 3, x1 + 17 + posBouton*20, y1 + 17,fill=fillBouton, outline=outBouton,tags="btn" + str(numBtn) + "_" + tag)
    canvas.addtag_withtag(tag, "btn" + str(numBtn) + "_" + tag)
    

def onDragMenu( event, canvas, tag):
    global xSouris, ySouris, xDragSouris, yDragSouris
    
    #tagCoords = canvas.coords(tag)
    canvas.move(tag, event.x - xDragSouris, event.y - yDragSouris)
    xDragSouris, yDragSouris = event.x, event.y
        
def onStartDragMenu( event,canvas,tag):
    global xDragSouris, yDragSouris 
    
    xDragSouris, yDragSouris = event.x, event.y
    canvas.itemconfig(tag, fill="red")

def onStopDragMenu( event,canvas,tag):
    canvas.itemconfig(tag, fill="#ffffff")
    
def onOverCroix(event,canvas,tag):
    canvas.itemconfig("fdCroix_" + tag, fill="#008000")

def onLeaveCroix(event,canvas,tag):
    canvas.itemconfig("fdCroix_" + tag, fill="")

def onClickCroix(event,canvas,tagMenu, tagRef):
    canvas.itemconfig( tagMenu, state="hidden")
    canvas.itemconfig( tagRef, outline="")

def dessinerMenu(canvas, xMenu, yMenu, epaisseur,label, tag, id):
    global imageIcoPdf
    
    rgba_color = (0, 0, 0, 255) 
    fillMenu= "#48484c"
    outMenu = "#909098"
    croixCoul = "#e0e0e0"
    params = curDictCircuit.get(id)
    if params :
        [btn1, btn2, btn3] = params["btnMenu"]
        if btn1 == 0:
            coul1="#808080"; pos1 = GAUCHE
        elif btn1 == 1:
            coul1="#ff0000"; pos1 = GAUCHE
        else : coul1="#00ff00"; pos1 = DROITE
        if btn2 == 0:
            coul2="#808080"; pos2 = GAUCHE
        elif btn2 == 1:
            coul2="#ff0000"; pos2 = GAUCHE
        else : coul2="#00ff00"; pos2 = DROITE
        if btn3 == 0:
            coul3="#808080"; pos3 = GAUCHE
        elif btn3 == 1:
            coul3="#ff0000"; pos3 = GAUCHE
        else : coul3="#00ff00"; pos3 = DROITE
        #imageFond = captureZoneCanvas(canvas,xMenu, yMenu, xMenu + 128,  yMenu + 128)
        #canvas.create_image(xMenu, yMenu, image=imgMenu, anchor=tk.NW)
        rectangleArrondi(canvas, xMenu, yMenu, 128,  128, 10, outline=outMenu, fill=fillMenu, width=epaisseur, tags = tag)
        canvas.create_rectangle(xMenu,      yMenu, xMenu + 114, yMenu + 17, fill="",outline="", tags="drag_" + tag)
        canvas.create_line(xMenu , yMenu + 17, xMenu + 127,  yMenu + 17, fill=outMenu, width=epaisseur, tags = tag)
        canvas.create_rectangle(xMenu + 110,      yMenu + 1, xMenu + 125, yMenu + 16, fill="",outline="", tags="fdCroix_" + tag)
        canvas.create_line(xMenu + 115, yMenu + 5, xMenu + 120,  yMenu + 12, fill=croixCoul, width=epaisseur*2, tags = "croix_" + tag)
        canvas.create_line(xMenu + 115, yMenu + 12, xMenu + 120,  yMenu + 5, fill=croixCoul, width=epaisseur*2, tags = "croix_" + tag)
        car(canvas, xMenu +63 , yMenu + 8 ,echelleCar=0.8,angle=0, texte=label,couleur="#ffffff", anchor="center", tags = "titre_" + tag)
        dessinerInter(canvas, xMenu+10, yMenu + 27,fillBouton=coul1, posBouton=pos1, tag = "switch_" + tag,numBtn=1)
        canvas.tag_bind("btn1_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn1_switch_" + tag, id,1))
        dessinerAOP(canvas,xMenu + 82, yMenu + 32, echelle=2, couleur="#000000",tags=tag)
        dessinerAOP(canvas,xMenu + 80, yMenu + 30, echelle=2, tags=tag)
        dessinerInter(canvas, xMenu+10, yMenu + 60,fillBouton=coul2, posBouton=pos2,tag = "switch_" + tag,numBtn=2)
        canvas.tag_bind("btn2_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn2_switch_" + tag, id,2))
        dessinerLabelBroche(canvas,xMenu + 68, yMenu + 65, echelle=2,couleur = "#000000", tags=tag)
        dessinerLabelBroche(canvas,xMenu + 65, yMenu + 62, echelle=2,couleur = "#faa000", tags=tag)
        dessinerLabelBroche(canvas,xMenu + 88, yMenu + 65, echelle=2,couleur = "#000000", tags=tag)
        dessinerLabelBroche(canvas,xMenu + 85, yMenu + 62, echelle=2,couleur = "#faa000", tags=tag)
        dessinerLabelBroche(canvas,xMenu + 108, yMenu + 65, echelle=2,couleur = "#000000", tags=tag)
        dessinerLabelBroche(canvas,xMenu + 105, yMenu + 62, echelle=2,couleur = "#faa000", tags=tag)
        dessinerInter(canvas, xMenu+10, yMenu + 93,fillBouton=coul3, posBouton=pos3,tag = "switch_" + tag,numBtn=3)
        imgSave.append( canvas.create_image(xMenu+85, yMenu + 105, image=imageIcoPdf, tags=tag, anchor="center"))
        canvas.tag_bind("btn3_switch_" + tag, "<Button-1>",lambda event : onSwitch(event,canvas,"btn3_switch_" + tag, id,3))
        canvas.tag_raise("drag_" + tag)
        canvas.addtag_withtag(tag, "titre_" + tag)
        canvas.addtag_withtag(tag, "fdCroix_" + tag)
        canvas.addtag_withtag(tag, "croix_" + tag)
        canvas.addtag_withtag(tag,  "btn_" + tag)
        canvas.addtag_withtag(tag,  "drag_" + tag)
        canvas.addtag_withtag(tag,  "switch_" + tag)
        canvas.addtag_withtag("menuComposant",  tag)
        canvas.tag_bind("drag_" + tag,"<B1-Motion>", lambda event : onDragMenu(event,canvas, tag))
        canvas.tag_bind("drag_" + tag,"<Button-1>", lambda event : onStartDragMenu(event,canvas, "titre_" + tag))
        canvas.tag_bind("croix_" + tag,"<Enter>", lambda event : onOverCroix(event, canvas, tag))
        canvas.tag_bind("croix_" + tag,"<Leave>", lambda event : onLeaveCroix(event, canvas, tag))
        canvas.tag_bind("croix_" + tag,"<Button-1>", lambda event : onClickCroix(event, canvas, tag,  "zoneActive" + id))
        canvas.tag_bind("drag_" + tag,"<ButtonRelease-1>", lambda event : onStopDragMenu(event,canvas, "titre_" + tag))
        #canvas.itemconfig("fdCroix_" + tag, state="hidden")
        #
        #rectangleArrondi(canvas, xMenu, yMenu, 128,  128, 10, outline="", fill="", tags=tag)
        #canvas.itemconfig("fond_" + tag, state="hidden")
        #canvas.itemconfig("symb_" + tag, state="hidden")
        #canvas.itemconfig("pin_" + tag, state="hidden")
        canvas.itemconfig(tag, state="hidden")
    

def on_enter( canvas, tag):
    global xSouris, ySouris 
    
    space=9
    tagCoords = canvas.coords(tag)
    canvas.move(tag, xSouris - tagCoords[0] - space,0)
    canvas.tag_raise(tag)
    #canvas.itemconfig("fond_" + tag, state="normal")
    #canvas.itemconfig("symb_" + tag, state="normal")
    #canvas.itemconfig("pin_" + tag, state="normal")
    canvas.itemconfig(tag, state="normal")
    
def onMenu( event,canvas, tagMenu, tagAll, tagRef, coulOut="#60d0ff"):
    #xSouris = event.x
    #space=9
    #tagCoords = canvas.coords(tag)
    #canvas.move(tag,  tagCoords[3] + space,0)
    canvas.tag_raise( tagMenu)
    #canvas.itemconfig("fond_" + tag, state="normal")
    #canvas.itemconfig("symb_" + tag, state="normal")
    canvas.itemconfig(tagAll , state="hidden")
    canvas.itemconfig(tagMenu, state="normal")
    canvas.itemconfig("zaComposant", outline="")
    canvas.itemconfig(tagRef, outline=coulOut)

# Fonction pour réinitialiser le curseur lorsqu'il sort de la zone
def on_leave( canvas, tag):
    #global curseurCourant,curseurSauve
    #canvas.config(cursor="")
    #curseurCourant = curseurSauve
    canvas.itemconfig("fond_" + tag, state="hidden")
    canvas.itemconfig("symb_" + tag, state="hidden")
    canvas.itemconfig("pin_" + tag, state="hidden")
    canvas.itemconfig(tag, state="hidden")
    
def boitier(canvas, xD, yD, echelle=1, largeur = -1,  sens = HORIZONTAL, **kwargs):
    global numID
    
    if (largeur !=-1):
        echelle = largeur / 9.0
    interSpace = 15*echelle  
    space = 9*echelle
    epaisseur = 1*echelle
        
    dim = dip14
    ouvert=NON
    foncInterne=None
    cursorOver = ""
    id = None
    tags = []
    for key, value in kwargs.items():
        if key == "nbBroches"           : dim["nbBroches"]       = value
        if key == "largeurBoitier"      : dim["largeurBoitier"]  = value
        if key == "label"               : dim["label"]           = value
        if key == "foncInterne"         : dim["foncInterne"]     = value
        if key == "ouvert"              : ouvert                 = value
        if key == "cursorOver"          : cursorOver             = value
        if key == "id"                  : id                     = value    
        if key == "tags"                : tags                   = value         
        if key == "type"                : type                   = value    
        
    dimLigne = (dim["nbBroches"] - 0.30)*interSpace/2
    dimColone = dim["largeurBoitier"]*interSpace  
                
    params = {}
    if (id):                
        if (curDictCircuit.get(id)):
            params = curDictCircuit[id]
            tags = params["tags"]
    else: 
        idType[type] += 1
        id="_boitier_" + str(numID)
        numID += 1
        
    if (not tags):
        params["id"]= id
        params["XY"]=(xD, yD)
        
        dimLigne = (dim["nbBroches"] - 0.30)*interSpace/2
        dimColone = dim["largeurBoitier"]*interSpace  
        label = dim["label"] + "-" + str(idType[type])
        params["label"] = label
        params["type"] = type
        params["btnMenu"] = [1,1,0]
        #canvas.create_rectangle(xD+2*echelle,yD-1*echelle,xD+11*echelle,yD-4*echelle, fill="#c0c0c0",outline="#000000")
        #canvas.create_polygon(xD+(3+15)*echelle,yD-1*echelle,xD+(7 + 15)*echelle,yD-6*echelle,xD+ (11 + 15)*echelle, yD -1*echelle, fill="#a0a0a0",outline="#c0c0c0")
        #canvas.create_polygon(xD+(3+15)*echelle,yD-1*echelle,xD+(7 + 15)*echelle,yD-6*echelle,xD+ (11 + 15)*echelle, yD -1*echelle, fill="#a0a0a0",outline="#c0c0c0")
        nbBrocheParCote = dim["nbBroches"] // 2
        tagBase = "base" + id
        tagMenu = "menu" + id
        tagCapot = "capot" + id
        tagSouris = "zoneActive" + id
        for i in range(dim["nbBroches"]):
            canvas.create_rectangle(xD + 2*echelle+(i%nbBrocheParCote)*interSpace,      yD-(0 - (i//nbBrocheParCote)*(dimColone + 0)), \
                                    xD + 11*echelle+(i%nbBrocheParCote)*interSpace,     yD-(3*echelle - (i//nbBrocheParCote)*(dimColone + 6*echelle)), \
                                    fill="#909090",outline="#000000", tags=tagBase)
            canvas.create_polygon(xD + 2*echelle + (i%nbBrocheParCote)*interSpace,        yD-space//3 - (0-(i//nbBrocheParCote)*(dimColone + 2*space//3)), \
                                xD + space//3+ 2*echelle +(i%nbBrocheParCote)*interSpace,   yD-(2*space)//3 - (0-(i//nbBrocheParCote)*(dimColone + (4*space)//3)), \
                                xD + (2*space)//3+ 2*echelle +(i%nbBrocheParCote)*interSpace, yD-(2*space)//3 - (0-(i//nbBrocheParCote)*(dimColone + (4*space)//3)), \
                                xD+(11+(i%nbBrocheParCote)*15)*echelle,         yD-space//3 - (0-(i//nbBrocheParCote)*(dimColone + 2*space//3)), \
                                fill="#b0b0b0",outline="#000000", smooth=False, tags=tagBase)
        
        zone = rectangleArrondi(canvas, xD, yD, dimLigne,  dimColone, 5, outline="#343434", fill="#343434",width=epaisseur, tags=tagBase)
        
        #canvas.tag_bind(zone, "<Enter>", lambda event,canvas=canvas, cursorOver=cursorOver: on_enter(event, canvas, cursorOver))
        #dessinerMenu(canvas,xD + dimLigne + 2.3*echelle + space*0, yD - space,epaisseur,label, tagMenu, id)
        #canvas.tag_bind(tagCapot, "<Enter>", lambda event: on_enter( canvas, tagMenu))
        #canvas.tag_bind(tagSouris, "<Button-2>", lambda event: onMenu( event,canvas, tagMenu))
        #canvas.tag_bind(tagCapot, "<Leave>", lambda event: on_leave( canvas, tagMenu))
        #canvas.tag_bind(tagMenu, "<Leave>", lambda event: on_leave( canvas, tagMenu))
        
        params["tags"] = [tagBase]
        canvas.create_rectangle(xD + 2*echelle,      yD + 2*echelle, \
                                xD - 2*echelle+ dimLigne,     yD-2*echelle + dimColone, \
                                fill="#000000",outline="#000000", tags=tagBase)
        if dim["foncInterne"] != None:
            dim["foncInterne"](canvas,xD , yD ,echelle=echelle, tags=tagBase, \
                                **kwargs )
        #canvas.create_rectangle(xD + 2*echelle,      yD + 2*echelle, \
        #                        xD - 2*echelle+ dimLigne,     yD-2*echelle + dimColone, \
        #                        fill="#343434",outline="#343434", tags=tagCapot)
        rectangleArrondi(canvas, xD, yD, dimLigne,  dimColone, 5, outline="#343434", fill="#343434",width=epaisseur, tags=tagCapot)
        canvas.create_line(xD , yD+1*space//3, xD + dimLigne, yD + 1*space//3, fill="#b0b0b0", width=epaisseur, tags=tagCapot)
        canvas.create_line(xD , yD + dimColone - 1*space//3, xD + dimLigne, yD + dimColone - 1*space//3, fill="#b0b0b0", width=epaisseur, tags=tagCapot)
        canvas.create_oval(xD + 4*echelle, yD + dimColone - 1*space//3 - 6*echelle, xD + 8*echelle, yD + dimColone - 1*space//3 - 2*echelle, fill='#ffffff', outline='#ffffff', tags=tagCapot)
        canvas.create_arc(xD - 5*echelle, yD + dimColone//2 - 5*echelle, xD + 5*echelle, yD + dimColone//2 + 5*echelle, start=270, extent=180, fill='#000000', outline='#505050', style=tk.PIESLICE, tags=tagCapot)
        car(canvas, xD + dimLigne//2, yD + dimColone//2 ,echelle=echelle,angle=0, texte=label,couleur="#ffffff", anchor="center", tags=tagCapot)  # xD + 30*echelle,yD - 10*echelle
        canvas.create_rectangle(xD + 2*echelle,      yD + 2*echelle, \
                                xD - 2*echelle+ dimLigne,     yD-2*echelle + dimColone, \
                                fill="",outline="", tags=tagSouris)
        canvas.tag_raise(tagCapot)
        canvas.tag_raise(tagSouris)
        canvas.addtag_withtag("zaComposant",  tagSouris)
        if ouvert:
            canvas.itemconfig(tagCapot, state="hidden")
        else:
            params["tags"].append(tagCapot)
        curDictCircuit[id]=params
        dessinerMenu(canvas,xD + dimLigne + 2.3*echelle + space*0, yD - space,epaisseur,label, tagMenu, id)
        canvas.tag_bind(tagSouris, "<Button-2>", lambda event: onMenu( event,canvas, tagMenu,"menuComposant",tagSouris))
    else :
        X, Y= params["XY"]
        dX = xD - X
        dY = yD - Y
        for tg in tags:
            canvas.move(tg,dX ,dY)
        
    return  xD + dimLigne + 2.3*echelle, yD

def getXY(colonne, ligne, echelle=1, **kwargs):
    interSpace = 15*echelle  
    space = 9*echelle
    epaisseur = 1*echelle
    matrice = matrice830pts
    for key, value in kwargs.items():
        if key == "matrice"   : matrice      = value     
        
    id = str(colonne) +"," + str(ligne)
    x,y = matrice[id]["xy"]
    
    return x*echelle, y*echelle

def cabler(canvas, xD, yD, echelle=1, largeur = -1,  sens = HORIZONTAL, **kwargs) :
    global numID
    
    if (largeur !=-1):
        echelle = largeur / 9.0
    interSpace = 15*echelle  
    space = 9*echelle
    epaisseur = 1*echelle
    matrice = matrice830pts
    id = None
    for key, value in kwargs.items():
        if key == "couleur"   : couleur     = value
        if key == "mode"      : mode        = value    
        if key == "coords"    : coords      = value  
        if key == "matrice"   : matrice     = value    
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
        id="_cable_" + str(numID)
        numID += 1
    
    params["id"]= id
    params["mode"]=mode
    #params["matrice"] = matrice
    params["coord"] = coords
    xO, yO, xF, yF = coords[0] 
    xO, yO = getXY(xO,yO,echelle=echelle,matrice=matrice)
    xF, yF = getXY(xF,yF,echelle=echelle,matrice=matrice)
    params["XY"]=(xO,yO, xF, yF)
    params["couleur"]=couleur
    encre = f"#{couleur[0]:02x}{couleur[1]:02x}{couleur[2]:02x}"
    contour = f"#{couleur[0]//2:02x}{couleur[1]//2:02x}{couleur[2]//2:02x}"
    canvas.create_oval(xD + xO + 2*space/9, yD + yO + 2*space/9, xD + xO + 7*space/9, yD + yO + 7*space/9, fill='#dfdfdf', outline='#404040', width=1*epaisseur, tags=id)
    canvas.create_oval(xD + xF + 2*space/9, yD + yF + 2*space/9, xD + xF + 7*space/9, yD + yF + 7*space/9, fill='#dfdfdf', outline='#404040', width=1*epaisseur, tags=id)
    # for i in range(4):
    #     coul = "#ff0000"
    #     if i != 2*space//9: coul = "#c00000"
    #     canvas.create_line(xD + xO*echelle + (i+2)*space//9, yD + yO*echelle + (i+2)*space//9, xD + xF*echelle + (i+2)*space//9, yD + yF*echelle + (i+2)*space//9, \
    #                     fill=coul, width=2*epaisseur)
    divY  = yF - yO if yF != yO else 0.000001
    xDiff = (space/2)*(1 - math.cos(math.atan((xF-xO)/divY)))
    yDiff = (space/2)*(1 - math.sin(math.atan((xF-xO)/divY)))
    p1    = ( (xO + xDiff), (yO + space - yDiff))
    p2    = ( (xF + xDiff), (yF + space - yDiff))
    p3    = ( (xF + space - xDiff), (yF + yDiff))
    p4    = ( (xO+ space - xDiff), (yO + yDiff))
    canvas.create_polygon(xD + p1[0], yD + p1[1], xD + p2[0], yD + p2[1], \
                         xD + p3[0], yD + p3[1], xD + p4[0], yD + p4[1], \
                         fill=encre, outline=contour, width=1*epaisseur, tags=id )  
    # canvas.create_polygon(xD + xO*echelle + 2*space//9, yD + yO*echelle + 2*space//9, xD + xF*echelle + 2*space//9, yD + yF*echelle + 2*space//9, \
    #                       xD + xF*echelle + 7*space//9, yD + yF*echelle + 7*space//9, xD + xO*echelle + 7*space//9, yD + yO*echelle + 7*space//9, \
    #                       fill=encre, outline=contour, width=1*epaisseur )  
    params["tags"] = [id]
    curDictCircuit[id] = params

    return xD, yD

matrice830pts = {}
matrice1260pts = {}

boitierDIP14 = [(boitier,1, {**dip14 , **capotFerme, "foncInterne":foncInterne})]    #, **pins7408
boitier7400 = [(boitier,1, {**dip7400 ,**capotFerme,  "foncInterne":foncInterne, **pins7400})]    
boitier7402 = [(boitier,1, {**dip7402 ,**capotFerme,  "foncInterne":foncInterne, **pins7402})]    
boitier7404 = [(boitier,1, {**dip7404 ,**capotFerme,  "foncInterne":foncInterne, **pins7404})]    
boitier7408 = [(boitier,1, {**dip7408 ,**capotFerme,  "foncInterne":foncInterne, **pins7408})]    
boitier7432 = [(boitier,1, {**dip7432 ,**capotFerme,  "foncInterne":foncInterne, **pins7432})]    
cableTest   = [(cabler,1,{"couleur":(255,0,0,255), "mode":AUTO, "coords":[(1,3,3,2)], "matrice": matrice1260pts}), \
               (cabler,1,{"couleur":(10,10,10,255), "mode":AUTO, "coords":[(35,12,35,13)], "matrice": matrice1260pts}), \
               (cabler,1,{"couleur":(0,80,0,255), "mode":AUTO, "coords":[(5,10,15,10)], "matrice": matrice1260pts}), \
               (cabler,1,{"couleur":(0,255,0,255), "mode":AUTO, "coords":[(2,6,40,1)], "matrice": matrice1260pts}),
               (cabler,1,{"couleur":(128,128,0,255), "mode":AUTO, "coords":[(51,1,48,13)], "matrice": matrice1260pts}),
               (cabler,1,{"couleur":(128,128,0,255), "mode":AUTO, "coords":[(51,15,48,27)], "matrice": matrice1260pts}),]


def remplirMatrice830pts(colD=1,  ligneD = 1, **kwargs):
    interSpace = 15

    matrice = matrice830pts
    for key, value in kwargs.items():
        if key == "matrice": matrice =value
        
    for i in range(50):
        idph = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(1 + ligneD) 
        idpb = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(13 + ligneD)
        idmh = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str( ligneD)
        idmb = str(2 + (i % 5) + colD + (i//5)*6)  + "," + str(12 + ligneD)
        matrice[idmh]={"id":["ph", "plus haut", "1"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (1.5 + 22.2*(ligneD//15))*interSpace ), "etat":LIBRE, "lien":None }
        matrice[idph]={"id":["mh", "moins haut", "2"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (2.5+ 22.2*(ligneD//15))*interSpace), "etat":LIBRE, "lien":None }
        matrice[idmb]={"id":["pb", "plus bas", "13"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (19.5 + 22.2*(ligneD//15))*interSpace), "etat":LIBRE, "lien":None }
        matrice[idpb]={"id":["mb", "moins bas", "14"], "xy":(0.5*interSpace + (2 + (i % 5) +colD + (i//5)*6)*interSpace, (20.5+ 22.2*(ligneD//15))*interSpace), "etat":LIBRE, "lien":None }
    for l in range(5):
        for c in range(63):
            id = str(c + colD) + "," + str(l + 2 + ligneD) 
            matrice[id]={"id":[id, str(l + 2 + ligneD)], "xy":(0.5*interSpace + (c + colD)*interSpace, (5.5 + l + 22.2*(ligneD//15))*interSpace), "etat":LIBRE, "lien":None }
            id = str(c + colD)+ "," + str(l + 7 + ligneD) 
            matrice[id]={"id":[id, str(l + 7 + ligneD)], "xy":(0.5*interSpace +  (c + colD)*interSpace, (12.5 + l + 22.2*(ligneD//15))*interSpace), "etat":LIBRE, "lien":None }
            
def remplirMatrice1260pts(colD=1,  ligneD = 1, **kwargs):
    interSpace = 15
    
    matrice = matrice1260pts            
    for key, value in kwargs.items():
        if key == "matrice": matrice =value

    remplirMatrice830pts(matrice=matrice1260pts)
    remplirMatrice830pts(ligneD=15, matrice=matrice1260pts)


ligneDistribution = [ (trou, 63)] #, {"couleurs":("#400010","#c00040","#200008")}
blocAlim = [(trou,5), (plat,1)] #, {"couleurs":("#400010","#c00040","#200008")}
#railAlimMoins = [(plat,1),(car,1),(rail,60)]
railAlimMoins = [(plat,1),(car,1, {"deltaY":1.3,"echelleCar":2}),(rail,60),(demiPlat,1),(plat,1),(car,1, {"deltaY":1.3,"echelleCar":2})]
railAlimPlus = [(plat,1),(car,1,{"couleur":"#ff0000", "texte":"+", "deltaY":-0.6, "echelleCar":2}),(railRouge,60),(plat,1),(demiPlat,1),(car,1,{"couleur":"#ff0000", "texte":"+", "deltaY":-0.6, "echelleCar":2})]
ligneAlim = [(plat,3), (blocAlim,10,{"sens":HORIZONTAL})]
bandeAlim = [(railAlimMoins,1,{"sens":VERTICAL}), (ligneAlim,2,{"sens":VERTICAL}), (railAlimPlus,1,{"sens":VERTICAL})]
bandeDistribution = [(ligneDistribution,5,{"sens":VERTICAL})]  
numerotation = [(plat,1), (numIter,1,{"numDeb":1, "numFin":63, "sens":HORIZONTAL, "deltaY":-1.5})]
#plaquette600pts = [(planche,1),(demiPlat,1,HORIZONTAL),(demiPlat,1,VERTICAL),(bandeAlim,1,VERTICAL), (plat,1,VERTICAL), (bandeDistribution,1,VERTICAL), ([(plat,1)],2,VERTICAL), (bandeDistribution,1,VERTICAL),(plat,1,VERTICAL),(bandeAlim,1,VERTICAL)]
plaquette830pts = [(setXYOrigine,1,{"idOrigine":"plq830"}),(planche,1),(demiPlat,1,{"sens":HORIZONTAL}),(demiPlat,1,{"sens":VERTICAL}),(bandeAlim,1,{"sens":VERTICAL}), \
                   (numerotation,1,{"sens":VERTICAL}), (goXY,1,{"ligne":5.5, "colonne":0.5, "idOrigine":"plq830"}), \
                   (carIter,1,{"carDeb":"f", "nbCar":5, "anchor":"center", "deltaY":0.7}),(bandeDistribution,1,{"sens":VERTICAL}),(goXY,1,{"ligne":5.5, "colonne":64.5, "idOrigine":"plq830"}),(demiPlat,1),(carIter,1,{"carDeb":"f", "nbCar":5, "sens":VERTICAL, "deltaY":0.7}), \
                   (goXY,1,{"ligne":12.5, "colonne":0.5, "idOrigine":"plq830"}), \
                   (carIter,1,{"carDeb":"a", "nbCar":5, "deltaY":0.7}), (bandeDistribution,1,{"sens":VERTICAL}), (goXY,1,{"ligne":12.5, "colonne":64.5, "idOrigine":"plq830"}),(demiPlat,1),(carIter,1,{"carDeb":"a", "nbCar":5, "sens":VERTICAL, "deltaY":0.7}), \
                   (goXY,1,{"ligne":18.8, "colonne":0.5, "idOrigine":"plq830"}), (numerotation,1,{"sens":VERTICAL}),
                   (goXY,1,{"ligne":18.5, "colonne":0.5, "idOrigine":"plq830"}), (bandeAlim,1,{"sens":VERTICAL})]    # ,1,{"sens":VERTICAL})]
#,(setFoncTrou,1,{"fonction":trouRond})
plaqueTest = [(setXYOrigine,1),(bandeAlim,1,{"sens":HORIZONTAL})]
plaqueTestMinimal = [(setXYOrigine,1),(railAlimPlus,4,{"sens":VERTICAL})]
plaquette1260pts =[(plaquette830pts,2,{"sens":PERSO, "dXY": (0, 1.3)})]
circuitTest = [(setXYOrigine,1,{"idOrigine":"circTest"}),(plaquette1260pts,1), (goXY,1,{"ligne":10.1, "colonne":1.4, "idOrigine":"circTest"}), (boitier7408,1,{"sens":HORIZONTAL}), \
               (boitier7402,1,{"sens":HORIZONTAL}), (boitier7404,1,{"sens":HORIZONTAL}), (boitier7400,1,{"sens":HORIZONTAL}), (boitier7432,1,{"sens":HORIZONTAL}), \
               (goXY,1,{"ligne":0, "colonne":0, "idOrigine":"circTest"}),(cableTest,1)]

def circuit(canvas, xD=0, yD=0, echelle=1, largeur = -1,  sens = VERTICAL, **kwargs):
    if (largeur !=-1):
        echelle = largeur / 9.0
    interSpace = 15*echelle  
    
    #xO=yO=-1
    modele = ligneDistribution
    for key, value in kwargs.items():
        if key == "modele": modele =value
        if key == "dXY": dX, dY = value
        
    #if xO == -1: xO, yO = xD,yD
    x, y = xD,yD
    for element in modele:
        if callable(element[0]) and isinstance(element[1],int):
            for _ in range(element[1]):
                if len(element) == 3:
                    (x, y, *retour) = element[0](canvas, x, y, echelle, largeur,**element[2])
                else : (x, y, *retour) = element[0](canvas, x, y, echelle, largeur)
        elif isinstance(element[0],list) and isinstance(element[1],int) :
            for _ in range(element[1]):
                if len(element) == 3:
                    (x,y, *retour) = circuit(canvas,x,y,echelle,largeur, modele=element[0], **element[2] )
                else : (x,y, *retour) = circuit(canvas,x,y,echelle,largeur,modele=element[0])
        else: raise ValueError("L'argument modele de rail doit être un tuple (fonction(), int, [int]) ou (list, int, [int]).")
        

    if sens == HORIZONTAL :  xD = x
    elif sens == VERTICAL :  yD = y + interSpace 
    elif sens == PERSO    :  
        yD = y - interSpace*dY
        #xD = x - interSpace*dX
    
                
    return (xD, yD )


