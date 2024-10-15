import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop Image Example")

# Charger l'image
image_path = "LedVerte.png"  # Remplacer par votre chemin d'image
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.topleft = (100, 100)

# Variables pour le drag-and-drop
dragging = False
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
                if image_rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = image_rect.x - event.pos[0]
                    offset_y = image_rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâcher le clic gauche
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                image_rect.x = event.pos[0] + offset_x
                image_rect.y = event.pos[1] + offset_y

    # Remplir l'écran avec la couleur blanche
    screen.fill(WHITE)

    # Dessiner l'image
    screen.blit(image, image_rect.topleft)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
