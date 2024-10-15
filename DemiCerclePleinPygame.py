import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop Shapes Example")

# Définir les formes
rect = pygame.Rect(100, 100, 150, 100)
rect_color = BLUE
half_circle_center = (400, 300)
half_circle_radius = 50
half_circle_color = RED

# Variables pour le drag-and-drop
dragging_rect = False
dragging_half_circle = False
offset_x = 0
offset_y = 0

# Fonction pour dessiner un demi-cercle plein
def draw_half_circle(surface, color, center, radius):
    points = [center]
    for angle in range(180):
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
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
                if rect.collidepoint(event.pos):
                    dragging_rect = True
                    offset_x = rect.x - event.pos[0]
                    offset_y = rect.y - event.pos[1]
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
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y
            elif dragging_half_circle:
                half_circle_center = (event.pos[0] + offset_x, event.pos[1] + offset_y)

    # Remplir l'écran avec la couleur blanche
    screen.fill(WHITE)

    # Dessiner les formes
    pygame.draw.rect(screen, rect_color, rect)
    draw_half_circle(screen, half_circle_color, half_circle_center, half_circle_radius)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
