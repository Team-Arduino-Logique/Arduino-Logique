# ArduinoLogique
Projet design 4
# Description du projet

## 1) Philosophie du code

Le point d'entrée principal du projet est la fonction `circuit`, qui prend en entrée un modèle correspondant à une liste de description de circuit. Cette fonction est récursive, ce qui permet de gérer une imbriquation infinie de listes et donc d'avoir une structure hiérarchique illimitée pour la création ou l'installation de composants.

Cette approche rend le code modulaire (en théorie, car il reste encore quelques ajustements à effectuer).

## 2) Exemples

La suite des explications sera illustrée par des exemples afin d'être à la fois plus pragmatique et plus claire:
  - créer une plaquette
  - créer une puce
  - créer un cable
  - créer une entrée/sortie
  - créer un circuit

### a) Créer une plaquette:
Il existe 4 types de platine standart:

#### Types de Breadboard

##### - Mini Breadboard
- **170 points** : Une petite platine souvent utilisée pour des circuits simples ou des prototypes de petite taille.
- **Dimensions approximatives** : 45 mm x 34 mm.

##### - Half Size Breadboard
- **400 points** : Une platine de taille intermédiaire.
- **Dimensions approximatives** : 82 mm x 54 mm.
- **Distribution** : 300 points de connexion en zone centrale et 100 points pour les rails d'alimentation.

##### - Full Size Breadboard
- **830 points** : Une platine de taille standard couramment utilisée.
- **Dimensions approximatives** : 165 mm x 54 mm.
- **Distribution** : 630 points de connexion en zone centrale et 200 points pour les rails d'alimentation.

##### - Large Breadboard
- **1660 points** : Une grande platine pour des projets plus complexes.
- **Dimensions approximatives** : 200 mm x 160 mm.
- **Distribution** : 1260 points de connexion en zone centrale et 400 points pour les rails d'alimentation.

Le code permet de créer toutes ces plaques ou d'autres plus exotiques.
Le code exemple qui suit va nous permettre de concevoir la mini plaque de 170 points.

Nous commençons par créer la plaque avec son fond:

```python

import tkinter as tk
import platineEssai as pe
from tkinter import font

fen = tk.Tk()
fen.title("Laboratoire virtuel de circuit logique - GIF-1002")

# Créer un canvas (surface sur laquelle on dessine)
canvas = tk.Canvas(fen, width=1500, height=900)
canvas.pack()

xPlaque, yPlaque = 50,10
pe.init(canvas)
plaqueMini170 = [(pe.planche,1,{"lgLigne":17, "lgColonne":10, "sepAlim":[], "sepDistribution":[(2,4.5)]})]
pe.circuit(canvas,xPlaque ,yPlaque, modele = plaqueMini170)

fen.mainloop()
```

