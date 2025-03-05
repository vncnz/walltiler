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
        "ta0": (0, 0, 1, 1),
        "tt1": (1, 0, 1, 1),
        "tt2": (2, 0, 1, 1),
        "tt3": (3, 0, 1, 1),
        "ta1": (4, 0, 1, 1),
        "tr1": (4, 1, 1, 1),
        "tr2": (4, 2, 1, 1),
        "tr3": (4, 3, 1, 1),
        "ta2": (4, 4, 1, 1),
        "tb1": (4, 3, 1, 1),
        "tb2": (4, 2, 1, 1),
        "tb3": (4, 1, 1, 1),
        "ta4": (4, 0, 1, 1),
        "tl1": (3, 0, 1, 1),
        "tl2": (2, 0, 1, 1),
        "tl3": (1, 0, 1, 1),
    }
    for w,c in terrains.items():
        tile_map[f'{tp}_{w}'] = (c[0], c[1] + y, c[2], c[3])

mode = "cold"
to_draw = [
    # {"tile": (0, 0), "pos": (100, 500)},  # Esempio: terreno
    # {"tile": (1, 0), "pos": (148, 500)},  # Proseguimento del terreno
    # {"tile": (3, 1), "pos": (500, 200)},  # Sole
    # {"tile": (0, 2), "pos": (600, 500)},  # Cactus o albero
    { "tile": f"{mode}_wind1", "pos": (7, 5) },
    { "tile": f"{mode}_wind2", "pos": (7, 6) },
    { "tile": f"{mode}_wind3", "pos": (7, 7) },
    { "tile": f"{mode}_wind4", "pos": (7, 8) },
    { "tile": f"{mode}_wind5", "pos": (7, 9) },
    { "tile": f"{mode}_wind6", "pos": (7, 10) },

    { "tile": f"{mode}_tt1", "pos": (10, 20) },
    { "tile": f"{mode}_tt2", "pos": (11, 20) },
    { "tile": f"{mode}_tt1", "pos": (12, 20) },
    { "tile": f"{mode}_tt3", "pos": (13, 20) },
    { "tile": f"{mode}_tt3", "pos": (14, 20) },
    { "tile": f"{mode}_ta1", "pos": (15, 20) },
    { "tile": f"{mode}_tr1", "pos": (15, 21) },
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
