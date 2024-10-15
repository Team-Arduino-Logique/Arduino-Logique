import schemdraw
import schemdraw.elements as elm

# Création du dessin
d = schemdraw.Drawing()

# Ajout d'un circuit intégré avec des pins correctement définis
d += elm.Ic(pins=[
    elm.IcPin(name='A', pin=1, side='left'),
    elm.IcPin(name='B', pin=2, side='left'),
    elm.IcPin(name='Y', pin=3, side='right')
], label='74LS001')

# Affichage du dessin
d.draw()

