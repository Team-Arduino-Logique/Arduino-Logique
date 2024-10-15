import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import io

GAUCHE = 0
DROITE = 1

def save_canvas_as_image(canvas):
    # Obtenir les dimensions du canvas
    canvas.update()
    ps = canvas.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    return img

def dessinerInter(x1,y1,fillSupport="#ffffff", fillBouton="#ff0000", outBouton="#000000", posBouton=GAUCHE):
    canvas.create_arc(x1,y1, x1 + 20, y1 + 20, \
                        start=90, extent=180,  fill=fillSupport, outline=fillSupport) 
    canvas.create_arc(x1+20,y1 , x1 + 40, y1 + 20, \
                        start=270, extent=180,  fill=fillSupport, outline=fillSupport) 
    canvas.create_rectangle(x1+10,y1,x1+30,y1+20,fill=fillSupport, outline=fillSupport)
    canvas.create_oval(x1 +3+posBouton*20,y1 + 3, x1 + 17 + posBouton*20, y1 + 17,fill=fillBouton, outline=outBouton)


# Créer une instance de la fenêtre principale
root = tk.Tk()
root.title("Afficher une image sur un canvas")

# Charger l'image avec PIL
image_path = "Icones/Fd_plaquette.png"  # Remplacez par le chemin de votre image
pil_image = Image.open(image_path)

# Convertir l'image PIL en un objet compatible avec Tkinter
tk_image = ImageTk.PhotoImage(pil_image)

# Créer un canvas
canvas = tk.Canvas(root, width=pil_image.width, height=pil_image.height)
canvas.pack()

rgba_color = (0, 0, 0, 192) 
# Ajouter l'image au canvas
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
image = Image.new('RGBA', (128,128), (128, 128, 128, 1))
#image = save_canvas_as_image(canvas)
draw = ImageDraw.Draw(image)
#imgCrop = image.crop((640,60,640+128,60+128))
#draw = ImageDraw.Draw( imgCrop)
draw.rounded_rectangle([(0,0), (127,127)],radius=10,outline="black",fill=rgba_color)
blurred_overlay = image.filter(ImageFilter.GaussianBlur(radius=0))
imgMenu = ImageTk.PhotoImage(blurred_overlay)
xMenu = 1120; yMenu=300
rgba_Menu = (128, 128, 128, 255) 
fillMenu= "#ffffff"
outMenu = fillMenu
canvas.create_image(xMenu, yMenu, image=imgMenu, anchor=tk.NW)
#draw.rounded_rectangle([(xMenu+10,yMenu+10), (xMenu+50,yMenu+30)],radius=20,outline="white",fill="white")
dessinerInter(xMenu+10, yMenu + 10)
dessinerInter(xMenu+10, yMenu + 50,fillBouton="#00ff00",posBouton=DROITE)
# Démarrer la boucle principale de Tkinter
root.mainloop()
