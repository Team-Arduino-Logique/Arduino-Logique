import tkinter as tk
import breadboard as pe
from tkinter import font

def zoom(echelle):
    canvas.delete("all")
    pe.init(canvas)
    pe.fillMatrix830pts()
    pe.circuit(canvas,xPlaque ,yPlaque, scale=int(echelle) /10.0, model = circuitLab2)    # xPlaque ,yPlaque ,
 

win = tk.Tk()
win.title("Laboratoire virtuel de circuit logique - GIF-1002")

# Créer un canvas (surface sur laquelle on dessine)
canvas = tk.Canvas(win, width=1500, height=900)
canvas.pack()

#text_widget = tk.Text(win, height=15, width=160)
#canvas.create_window(570, 800, window=text_widget)
#canvas.create_rectangle()
xPlaque, yPlaque = 50,10
pe.init(canvas)
pe.fillMatrix830pts()
ligneDistribution = [ (pe.drawHole, 17)] 
bandeDistribution = [(pe.drawHalfBlank,1,{"direction":pe.HORIZONTAL}),(pe.drawHalfBlank,1,{"direction":pe.VERTICAL}),(ligneDistribution,5, {"direction":pe.VERTICAL})]
plaqueMini170 = [(pe.drawBoard,1,{"radius":3,"dimLine":17.5, "dimColumn":12, "sepAlim":[], "sepDistribution":[(3,5.5)]}), (bandeDistribution,1,{"direction":pe.VERTICAL}), \
                   (bandeDistribution,1)]
#pe.circuit(canvas,xPlaque ,yPlaque, model = plaqueMini170)
wireLab2   = [(pe.drawWire,1,{"color":(255,0,0,255), "mode":pe.AUTO, "coords":[(3,3,3,2)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(0,0,0,255), "mode":pe.AUTO, "coords":[(9,12,9,13)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(255,0,0,255), "mode":pe.AUTO, "coords":[(10,3,10,2)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(0,0,0,255), "mode":pe.AUTO, "coords":[(16,12,16,13)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(255,170,37,255), "mode":pe.AUTO, "coords":[(1,7,1,8)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(170,77,74,255), "mode":pe.AUTO, "coords":[(2,7,2,8)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(255,170,37,255), "mode":pe.AUTO, "coords":[(1,6,7,6)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(170,77,74,255), "mode":pe.AUTO, "coords":[(2,5,8,5)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(0,255,0,255), "mode":pe.AUTO, "coords":[(9,5,20,5)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(255,170,37,255), "mode":pe.AUTO, "coords":[(1,9,13,9)], "matrix": pe.matrix830pts}), \
              (pe.drawWire,1,{"color":(170,77,74,255), "mode":pe.AUTO, "coords":[(2,10,14,10)], "matrix": pe.matrix830pts}) , \
              (pe.drawWire,1,{"color":(0,128,0,255), "mode":pe.AUTO, "coords":[(15,10,20,10)], "matrix": pe.matrix830pts}) ] #, \


circuitLab2 = [(pe.setXYOrigin,1,{"idOrigin":"circLab2"}),(pe.board830pts,1), (pe.goXY,1,{"line":10.1, "column":1.4+2, "idOrigin":"circLab2"}), \
               (pe.chip7408,1,{"direction":pe.HORIZONTAL}), \
               (pe.chip7432,1,{"direction":pe.HORIZONTAL}),  \
               (pe.goXY,1,{"line":0, "column":0, "idOrigin":"circLab2"}), (wireLab2,1)]   #  ,(wireTest,1)

pe.circuit(canvas,xPlaque ,yPlaque, model = circuitLab2)

h_slider = tk.Scale(win, from_=10, to=30, orient='horizontal', command=zoom)
h_slider.pack(fill='x', padx=10, pady=10)

win.mainloop()

#(pe.demiPlat,1,{"direction":pe.HORIZONTAL}),(pe.demiPlat,1,{"direction":pe.VERTICAL}),