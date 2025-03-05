import pygame
import sys

tileset_image = pygame.image.load("Retro-Lines-16x16/Environment.png")

# Impostazioni
TILE_SIZE = 16
GRID_WIDTH = 120  # FullHD / 16px
GRID_HEIGHT = 67
FULLHD_WIDTH = GRID_WIDTH * TILE_SIZE
FULLHD_HEIGHT = GRID_HEIGHT * TILE_SIZE
SCALE_FACTOR = 0.5  # Riduce la finestra di lavoro
ZOOM_MIN = 0.5
ZOOM_MAX = 2.0

pygame.init()
# tileset_image = pygame.image.load("tileset.png")
tileset_rect = tileset_image.get_rect()
TILESET_COLS = tileset_rect.width // TILE_SIZE

def update_window_size():
    global TILESET_WIDTH, TILESET_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_WIDTH, screen
    TILESET_WIDTH = int(tileset_image.get_width() * SCALE_FACTOR)
    TILESET_HEIGHT = int(tileset_image.get_height() * SCALE_FACTOR)
    SCREEN_WIDTH = int(FULLHD_WIDTH * SCALE_FACTOR)
    SCREEN_HEIGHT = int(FULLHD_HEIGHT * SCALE_FACTOR)
    WINDOW_WIDTH = SCREEN_WIDTH + TILESET_WIDTH
    screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))

update_window_size()
pygame.display.set_caption("Tile Editor")
clock = pygame.time.Clock()
selected_tile = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
tiles = []  # Lista delle tile posizionate

def draw_grid():
    for x in range(TILESET_WIDTH, WINDOW_WIDTH, int(TILE_SIZE * SCALE_FACTOR)):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, int(TILE_SIZE * SCALE_FACTOR)):
        pygame.draw.line(screen, (200, 200, 200), (TILESET_WIDTH, y), (WINDOW_WIDTH, y))

def draw_tileset():
    scaled_tileset = pygame.transform.scale(tileset_image, (TILESET_WIDTH, TILESET_HEIGHT))
    screen.blit(scaled_tileset, (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (selected_tile.x * SCALE_FACTOR, selected_tile.y * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR), 1)

def save_image():
    fullhd_surface = pygame.Surface((FULLHD_WIDTH, FULLHD_HEIGHT))
    fullhd_surface.fill((255, 255, 255))
    for tile in tiles:
        fullhd_tile = pygame.Rect(tile[0] / SCALE_FACTOR, tile[1] / SCALE_FACTOR, TILE_SIZE, TILE_SIZE)
        fullhd_surface.blit(tileset_image, fullhd_tile, tile[2])
    pygame.image.save(fullhd_surface, "wallpaper.png")
    print("Immagine salvata come wallpaper.png")

running = True
while running:
    screen.fill((255, 255, 255))
    draw_tileset()
    draw_grid()
    
    for tile in tiles:
        scaled_tile = pygame.Rect(tile[0] * SCALE_FACTOR + TILESET_WIDTH, tile[1] * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR, TILE_SIZE * SCALE_FACTOR)
        screen.blit(pygame.transform.scale(tileset_image.subsurface(tile[2]), (int(TILE_SIZE * SCALE_FACTOR), int(TILE_SIZE * SCALE_FACTOR))), scaled_tile)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_image()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < TILESET_WIDTH:
                tile_col = int(x / (TILE_SIZE * SCALE_FACTOR))
                tile_row = int(y / (TILE_SIZE * SCALE_FACTOR))
                selected_tile = pygame.Rect(tile_col * TILE_SIZE, tile_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            else:
                tile_x = int(((x - TILESET_WIDTH) / SCALE_FACTOR) // TILE_SIZE) * TILE_SIZE
                tile_y = int((y / SCALE_FACTOR) // TILE_SIZE) * TILE_SIZE
                if event.button == 1:
                    tiles.append((tile_x, tile_y, selected_tile.copy()))
                elif event.button == 3:
                    tiles = [tile for tile in tiles if not (tile[0] == tile_x and tile[1] == tile_y)]
        elif event.type == pygame.MOUSEWHEEL:
            SCALE_FACTOR += event.y * 0.2
            SCALE_FACTOR = max(ZOOM_MIN, min(ZOOM_MAX, SCALE_FACTOR))
            update_window_size()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
