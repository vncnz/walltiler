import pygame

# Inizializza Pygame
pygame.init()

# Impostazioni schermo
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TILE_SIZE = 32
BACKGROUND_COLOR = (0, 0, 0)

# Carica il tileset
tileset_image = pygame.image.load("Retro-Lines-16x16/Environment.png")
# tileset_image = pygame.transform.scale(tileset_image, (tileset_image.get_width() * (TILE_SIZE // 16),
#                                                        tileset_image.get_height() * (TILE_SIZE // 16)))

# Crea la finestra di disegno (non viene mostrata, serve solo per generare l'immagine)
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BACKGROUND_COLOR)

# Funzione per estrarre tile dal tileset
def get_tile(x, y, w=1, h=1, size=16):
    """ Copy a tile from selected coordinates and resize it """
    rect = pygame.Rect(x * size, y * size, w * size, h * size)
    # print(f'{x * size}, {y * size}, {w * size}, {h * size}')
    tile = tileset_image.subsurface(rect)
    return pygame.transform.scale(tile, (TILE_SIZE * w, TILE_SIZE * h))

# Mappatura degli elementi (posizione in pixel)
areas_y = {
    "normal": 0,
    "sun": 13,
    "hot": 26,
    "cold": 39,
    "water": 54
}
tile_map = {
    "sun1": (0, 69, 3, 3),
    "sun2": (3, 69, 3, 3),
    "sun3": (6, 69, 3, 3),
    "sun4": (9, 69, 3, 3),
    "sun5": (12, 69, 3, 3),
    "sun6": (15, 69, 3, 3),
    "moon1": (0, 66, 3, 3),
    "moon2": (3, 66, 3, 3),
    "moon3": (6, 66, 3, 3),
    "moon4": (9, 66, 3, 3),
    "moon5": (12, 66, 3, 3),
    "moon6": (15, 66, 3, 3),
}

for tp, y in areas_y.items():
    winds = {
        "wind1": (0, 72, 1, 1),
        "wind2": (1, 72, 2, 1),
        "wind3": (3, 72, 2, 1),
        "wind4": (5, 72, 2, 1),
        "wind5": (7, 72, 2, 1),
        "wind6": (9, 72, 2, 1)
    }
    for w,c in winds.items():
        tile_map[f'{tp}_{w}'] = (c[0], c[1] - 72 + 9 + y, c[2], c[3])
    terrains = {
        "t1a": (0, 0, 1, 1),
        "t2a": (1, 0, 1, 1),
        "t3a": (2, 0, 1, 1),
        "t4a": (2, 1, 1, 1),
        "t5a": (2, 2, 1, 1),
        "t6a": (1, 2, 1, 1),
        "t7a": (0, 2, 1, 1),
        "t8a": (0, 1, 1, 1),
    }
    for w,c in terrains.items():
        tile_map[f'{tp}_{w}'] = (c[0], c[1] + y, c[2], c[3])

to_draw = [
    # {"tile": (0, 0), "pos": (100, 500)},  # Esempio: terreno
    # {"tile": (1, 0), "pos": (148, 500)},  # Proseguimento del terreno
    # {"tile": (3, 1), "pos": (500, 200)},  # Sole
    # {"tile": (0, 2), "pos": (600, 500)},  # Cactus o albero
    { "tile": "normal_wind1", "pos": (7, 5) },
    { "tile": "normal_wind2", "pos": (7, 6) },
    { "tile": "normal_wind3", "pos": (7, 7) },
    { "tile": "normal_wind4", "pos": (7, 8) },
    { "tile": "normal_wind5", "pos": (7, 9) },
    { "tile": "normal_wind6", "pos": (7, 10) },

    { "tile": "normal_t2a", "pos": (11, 3) },
]

# Disegna le tile sulla superficie
for item in to_draw:
    tile_x, tile_y, tile_w, tile_h = tile_map[item["tile"]]
    pos_x, pos_y = item["pos"]
    tile = get_tile(tile_x, tile_y, tile_w, tile_h)
    screen.blit(tile, (pos_x * TILE_SIZE, pos_y * TILE_SIZE))

# Salva l'immagine finale
pygame.image.save(screen, "sfondo_generato.png")
# print("Sfondo generato e salvato come 'sfondo_generato.png'.")

# Termina Pygame
pygame.quit()
