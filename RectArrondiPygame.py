import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BEIGE = (220, 220, 220)
#CREME = (230, 230, 230)
#GRIS = (192, 192, 192)
CREME = (255, 0, 0)
GRIS = (0, 0, 255)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop Shapes Example")

# Définir les formes
rect_x, rect_y, rect_w, rect_h = 50, 50, 800, 400
rect_color = BEIGE
rect_radius = 5

half_circle_center = (106, 106)
half_circle_radius = 6
half_circle_colorH = GRIS
half_circle_colorB = CREME

# Variables pour le drag-and-drop
dragging_rect = False
dragging_half_circle = False
offset_x = 0
offset_y = 0

# Fonction pour dessiner un rectangle avec des coins arrondis
def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

# Fonction pour dessiner un demi-cercle plein
def draw_half_circle(surface, color, center, radius, angleD, angleF):
    points = [center]
    for angle in range(angleD*10,angleF*10):
        x = center[0] + radius * math.cos(math.radians(angle/10.0))
        y = center[1] - radius * math.sin(math.radians(angle/10.0))
        points.append((x, y))
    points.append((center[0] + radius, center[1]))  # Ajouter le point à l'extrémité droite
    pygame.draw.polygon(surface, color, points)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if rect_x <= event.pos[0] <= rect_x + rect_w and rect_y <= event.pos[1] <= rect_y + rect_h:
                    dragging_rect = True
                    offset_x = rect_x - event.pos[0]
                    offset_y = rect_y - event.pos[1]
                elif ((event.pos[0] - half_circle_center[0]) ** 2 + (event.pos[1] - half_circle_center[1]) ** 2) ** 0.5 < half_circle_radius and event.pos[1] < half_circle_center[1]:
                    dragging_half_circle = True
                    offset_x = half_circle_center[0] - event.pos[0]
                    offset_y = half_circle_center[1] - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâcher le clic gauche
                dragging_rect = False
                dragging_half_circle = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_rect:
                rect_x = event.pos[0] + offset_x
                rect_y = event.pos[1] + offset_y
            elif dragging_half_circle:
                half_circle_center = (event.pos[0] + offset_x, event.pos[1] + offset_y)

    # Remplir l'écran avec la couleur blanche
    screen.fill(WHITE)

    # Dessiner les formes
    draw_rounded_rect(screen, rect_color, (rect_x, rect_y, rect_w, rect_h), rect_radius)
    #draw_half_circle(screen, half_circle_colorH, half_circle_center, half_circle_radius,0,180)
    #draw_half_circle(screen, half_circle_colorB, half_circle_center, half_circle_radius,180,360)
    #pygame.draw.arc(screen, "blue", [210, 75, 150, 125], math.pi, 3 * math.pi / 2, 2)
    pygame.draw.circle(screen, half_circle_colorH, half_circle_center, half_circle_radius, 0, draw_top_right=True, draw_top_left=True)
    pygame.draw.circle(screen, half_circle_colorB, half_circle_center, half_circle_radius, 0, draw_bottom_right=True, draw_bottom_left=True)
    pygame.draw.arc(screen,half_circle_colorH,[100,200,12,12],0,math.pi,width=1)
    
    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
