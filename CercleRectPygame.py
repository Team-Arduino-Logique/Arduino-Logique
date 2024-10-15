import pygame
import sys

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
circle_center = (400, 300)
circle_radius = 50
circle_color = RED

# Variables pour le drag-and-drop
dragging_rect = False
dragging_circle = False
offset_x = 0
offset_y = 0

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
                elif ((event.pos[0] - circle_center[0]) ** 2 + (event.pos[1] - circle_center[1]) ** 2) ** 0.5 < circle_radius:
                    dragging_circle = True
                    offset_x = circle_center[0] - event.pos[0]
                    offset_y = circle_center[1] - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâcher le clic gauche
                dragging_rect = False
                dragging_circle = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_rect:
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y
            elif dragging_circle:
                circle_center = (event.pos[0] + offset_x, event.pos[1] + offset_y)

    # Remplir l'écran avec la couleur blanche
    screen.fill(WHITE)

    # Dessiner les formes
    pygame.draw.rect(screen, rect_color, rect)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
