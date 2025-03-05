import pygame

# Configurazioni
TILE_SIZE = 16  # Dimensione base della tile (modifica se necessario)
SCALE_FACTOR = .8  # Quanto ingrandire le tile per una migliore visibilità
TILE_DISPLAY_SIZE = TILE_SIZE * SCALE_FACTOR  # Tile ingrandite per la selezione

# Inizializza Pygame
pygame.init()

# Carica il tileset
tileset_image = pygame.image.load("Retro-Lines-16x16/Environment.png")

# Calcola dimensioni della finestra
tileset_width, tileset_height = tileset_image.get_width(), tileset_image.get_height()
window_width = tileset_width * SCALE_FACTOR
window_height = tileset_height * SCALE_FACTOR

# Scala il tileset per una migliore selezione
tileset_scaled = pygame.transform.scale(tileset_image, (window_width, window_height))

# Crea finestra
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Selettore di Tile")

# Variabili per la selezione
start_pos = None
end_pos = None
running = True

txt = ''
import math

while running:
    screen.fill((0, 0, 0))  # Sfondo nero
    screen.blit(tileset_scaled, (0, 0))  # Disegna il tileset

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click sinistro → Inizio selezione
                start_pos = event.pos
            elif event.button > 1:
                print(f'Clicked on {txt}')

    # Disegna rettangolo di selezione
    if start_pos:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        end_pos = (mouse_x, mouse_y)
        rect_x = min(start_pos[0], mouse_x)
        rect_y = min(start_pos[1], mouse_y)
        rect_w = abs(start_pos[0] - mouse_x)
        rect_h = abs(start_pos[1] - mouse_y)
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_w, rect_h), 1)

        start_x = math.floor(start_pos[0] / TILE_DISPLAY_SIZE)
        start_y = math.floor(start_pos[1] / TILE_DISPLAY_SIZE)
        end_x = math.ceil(end_pos[0] / TILE_DISPLAY_SIZE)
        end_y = math.ceil(end_pos[1] / TILE_DISPLAY_SIZE)

        pos_x = min(start_x, end_x)
        pos_y = min(start_y, end_y)
        size_x = abs(start_x - end_x)
        size_y = abs(start_y - end_y)

        # print(f"Selezione: Da ({start_x}, {start_y}) a ({end_x}, {end_y}) in unità di tile")
        txt2 = f"({pos_x}, {pos_y}, {size_x}, {size_y})"
        if txt != txt2:
            print(f"Selezione coo {txt2} in unità di tile")
            txt = txt2

    pygame.display.flip()

pygame.quit()
