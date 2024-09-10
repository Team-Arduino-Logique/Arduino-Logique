import tkinter as tk
import platineEssai as pe
from tkinter import font

def zoom(echelle):
    canvas.delete("all")
    pe.init(canvas)
    pe.remplirMatrice1260pts()
    pe.circuit(canvas,xPlaque ,yPlaque, echelle=int(echelle) /10.0, modele = pe.circuitTest)    # xPlaque ,yPlaque ,
    #pe.circuit(canvas,xPlaque ,yPlaque, echelle=int(echelle) /10.0, modele = nouveauCable) 
    #pe.circuit(canvas,xNouvBoitier ,yNouvBoitier, echelle=int(echelle) /10.0, modele = moveBoitier) 
    #print(nouveauCable[0][2]["id"])
   # nouveauCable[0][2]["coords"]=[(1,6,13,2)]
    #nouveauCable[0][2]["couleur"]=(128,255,128,255)
    #pe.circuit(canvas,xPlaque ,yPlaque, echelle=int(echelle) /10.0, modele = nouveauCable) 
    
    #print(pe.curDictCircuit)
    #pe.circuit(canvas,xPlaque + (1.4*15)*int(echelle) /10.0, yPlaque + (10.1*15)*int(echelle) /10.0,echelle=int(echelle) /10.0,modele=pe.boitierDIP14)
    #pe.boitier(canvas,xPlaque + (1.4*15 + 30*15)*int(echelle) /10.0, yPlaque + (10.1*15)*int(echelle) /10.0,echelle=int(echelle) /10.0, modele=pe.dip60)


# Créer la fenêtre principale
fen = tk.Tk()
fen.title("Laboratoire virtuel de circuit logique - GIF-1002")

# Créer un canvas (surface sur laquelle on dessine)
canvas = tk.Canvas(fen, width=1500, height=900)
canvas.pack()
#canvas.config(cursor=pe.curseur_cleA)
xPlaque, yPlaque = 50,10
xNouvBoitier, yNouvBoitier = 500,161.5
#pe.rectangleArrondi(canvas, xPlaque, yPlaque, xPlaque + 1000, yPlaque + 300, 20, outline="#F5F5DC", fill="#F5F5DC")
#pe.planche(canvas,xPlaque,yPlaque)

#imgText = pe.imageDuTexte("a" )
pe.init(canvas)
pe.remplirMatrice1260pts()
#pe.trou(canvas,100,100)
nouveauCable = [(pe.cabler,1,{"id": "pcable_1", "couleur":(255,0,0,255), "mode":pe.AUTO, "coords":[(1,5,3,2)], "matrice": pe.matrice1260pts})]
moveBoitier = [(pe.boitier,1,{"id": "_boitier_5", "XY":(500, 161.5)})]
ech=10.0
zoom(ech)
#pe.symbNOR(canvas, 350,500,echelle=8)
#pe.plaqueEssai(canvas,xPlaque ,yPlaque , echelle=ech, modele=pe.plaquette830pts)
#pe.boitier(canvas,xPlaque + (1.4*15)*ech, yPlaque + (10.09*15)*ech,echelle=ech)
#pe.boitier(canvas,xPlaque + (1.4*15 + 7*15)*ech, yPlaque + (10.09*15)*ech,echelle=ech)

h_slider = tk.Scale(fen, from_=10, to=30, orient='horizontal', command=zoom)
h_slider.pack(fill='x', padx=10, pady=10)

#pe.plaqueEssai(canvas,xPlaque + 15,yPlaque + 75)
#pe.plaqueEssai(canvas,xPlaque + 41,yPlaque+7, modele=pe.railAlim)

firaCodeFont = font.Font(family="FiraCode-Bold.ttf", size=15)
#canvas.create_text(300, 100, text="74LS001", font=firaCodeFont, fill="black")

#canvas.create_image(76, 357, image=imgText, anchor=tk.CENTER)
#pe.car(canvas, 76,57,texte="-")
#pe.car(canvas, 76,327,texte="+")

# interSpace = 15
# space= 9
# xD, yD=100, 100
# for y in range(10):
#     if y == 5: yD+=2*interSpace+2*space//3
#     for x in range(63):
#         canvas.create_polygon(xD+x*interSpace, yD+space+y*interSpace, xD+x*interSpace, yD+y*interSpace, xD+space+x*interSpace, yD+y*interSpace, fill='#c0c0c0', outline='#c0c0c0')
#         canvas.create_polygon(xD+x*interSpace, yD+space+y*interSpace, xD+space+x*interSpace, yD+space+y*interSpace, xD+space+x*interSpace, yD+y*interSpace, fill='#f6f6f6', outline='#f6f6f6')
#         canvas.create_rectangle(xD+space//3+x*interSpace, yD+space//3+y*interSpace, xD+2*space//3+x*interSpace,yD+2*space//3+y*interSpace,fill="#484848",outline="#484848")



fen.mainloop()