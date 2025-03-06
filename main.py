import pygame
from urllib.request import urlopen
import json

lat = 0
lon = 0
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,is_day,precipitation,rain,weather_code,relative_humidity_2m,wind_speed_10m&timezone=auto&forecast_days=1&daily=sunrise,sunset,daylight_duration"

# with urlopen(url) as f:
#     data = json.load(f)
data = {
    'latitude': 0, 
    'longitude': 0, 
    'generationtime_ms': 0.07557868957519531, 
    'utc_offset_seconds': 3600, 
    'timezone': 'Europe/Rome', 
    'timezone_abbreviation': 'GMT+1', 
    'elevation': 0, 
    'current_units': {'time': 'iso8601', 'interval': 'seconds', 'temperature_2m': '°C', 'apparent_temperature': '°C', 'is_day': '', 'precipitation': 'mm', 'rain': 'mm', 'weather_code': 'wmo code', 'relative_humidity_2m': '%'}, 
    'current': {
        'time': '2025-03-06T11:30', 
        'interval': 900, 
        'temperature_2m': 16.2, 
        'apparent_temperature': 7.3, 
        'is_day': 1, 
        'precipitation': 0.0, 
        'rain': 0.0, 
        'weather_code': 0, 
        'relative_humidity_2m': 41,
        'wind_speed_10m': 30
    }, 
    'daily_units': {'time': 'iso8601', 'sunrise': 'iso8601', 'sunset': 'iso8601', 'daylight_duration': 's'}, 
    'daily': {
        'time': ['2025-03-06'], 
        'sunrise': ['2025-03-06T06:00'], 
        'sunset': ['2025-03-06T18:00'], 
        'daylight_duration': [40000.00]
    }
}

is_windy = data['current']['wind_speed_10m']
if is_windy < 2: is_windy = 0
is_hot = data['current']['apparent_temperature'] > 29.9
is_day = data['current']['is_day'] == 1

mode = "normal"
if data['current']['apparent_temperature'] > 25: mode = 'sun'
if data['current']['apparent_temperature'] > 30: mode = 'hot'
if data['current']['apparent_temperature'] < 5: mode = 'cold'

# exit()


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
        "ta1": (0, 0, 1, 1),
        "tt1": (1, 0, 1, 1),
        "tt2": (2, 0, 1, 1),
        "tt3": (3, 0, 1, 1),
        "ta2": (4, 0, 1, 1),
        "tr1": (4, 1, 1, 1),
        "tr2": (4, 2, 1, 1),
        "tr3": (4, 3, 1, 1),
        "ta3": (4, 4, 1, 1),
        "tb1": (4, 3, 1, 1),
        "tb2": (4, 2, 1, 1),
        "tb3": (4, 1, 1, 1),
        "ta4": (4, 0, 1, 1),
        "tl1": (3, 0, 1, 1),
        "tl2": (2, 0, 1, 1),
        "tl3": (1, 0, 1, 1),
        "tz1": (5, 0, 1, 1),
        "tz2": (6, 0, 1, 1),
        "tz3": (6, 1, 1, 1),
        "tz4": (5, 1, 1, 1),
        "obj1": (12, 1, 3, 2),
        "obj2": (15, 4, 3, 2),
        "obj3": (9, 1, 3, 3),
    }
    for w,c in terrains.items():
        tile_map[f'{tp}_{w}'] = (c[0], c[1] + y, c[2], c[3])

to_draw = [
    { "tile": f"{mode}_tt1", "pos": (4, 20) },
    { "tile": f"{mode}_tt2", "pos": (5, 20) },
    { "tile": f"{mode}_tt1", "pos": (6, 20) },
    { "tile": f"{mode}_tt3", "pos": (7, 20) },
    { "tile": f"{mode}_tt3", "pos": (8, 20) },
    { "tile": f"{mode}_ta2", "pos": (9, 20) },
    { "tile": f"{mode}_tr1", "pos": (9, 21) },
    { "tile": f"{mode}_tz4", "pos": (9, 22) },
    { "tile": f"{mode}_tt1", "pos": (10, 22) },
    { "tile": f"{mode}_tt2", "pos": (11, 22) },
    { "tile": f"{mode}_tt1", "pos": (12, 22) },
    { "tile": f"{mode}_tt3", "pos": (13, 22) },
    { "tile": f"{mode}_tt2", "pos": (14, 22) },
    { "tile": f"{mode}_tt1", "pos": (15, 22) },
    { "tile": f"{mode}_tt3", "pos": (16, 22) },
    { "tile": f"{mode}_obj1", "pos": (6, 18) },
    { "tile": f"{mode}_obj2", "pos": (12, 20) },
    { "tile": f"{mode}_obj3", "pos": (15, 20) },
]

if is_windy:
    to_draw += [
        { "tile": f"{mode}_wind1", "pos": (7, 10) },
        { "tile": f"{mode}_wind4", "pos": (13, 13) },
        { "tile": f"{mode}_wind2", "pos": (23, 9) },
        #{ "tile": f"{mode}_wind2", "pos": (7, 6) },
        #{ "tile": f"{mode}_wind3", "pos": (7, 7) },
        #{ "tile": f"{mode}_wind5", "pos": (7, 9) },
        #{ "tile": f"{mode}_wind6", "pos": (7, 10) }
    ]
    if is_windy > 3:
        to_draw.append({ "tile": f"{mode}_wind3", "pos": (19, 12) })

        if is_windy > 7:
            to_draw.append({ "tile": f"{mode}_wind4", "pos": (7, 16) })
            to_draw.append({ "tile": f"{mode}_wind6", "pos": (27, 15) })

            if is_windy > 10:
                to_draw.append({ "tile": f"{mode}_wind6", "pos": (21, 15) })

to_draw.append({ "tile": f"{'sun'if is_day else 'moon'}{'4' if is_hot else '1'}", "pos": (27, 10) })

def getMoonSurface ():
    ''' Returns the surface of the moon, flipped if needed '''
    # TODO!
    pass

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
