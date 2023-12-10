import pygame as pg
import os 
import sys

TILE_SIZE = 40 
GRID_SIZE = 20 

# Mapa de prueba (0 = pasto, 1 = caja, 2 = bloque)
MAP = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2],
    [2, 0, 0, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2],
    [2, 1, 1, 1, 2, 1, 2, 0, 0, 2, 2, 0, 0, 2, 1, 2, 1, 1, 1, 2],
    [2, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 2],
    [2, 1, 1, 1, 2, 1, 2, 0, 0, 2, 2, 0, 0, 2, 1, 2, 1, 1, 1, 2],
    [2, 0, 0, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2],
    [2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

SCREENRECT = pg.Rect(0, 0, TILE_SIZE*GRID_SIZE, TILE_SIZE*GRID_SIZE)

dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "../../assets/img/")

def load_tile_images():
    tile_images = []
    image_names = ["grass.png", "box.png", "block.png"]  # remplaza esto con los nombres de tus imágenes

    for name in image_names:
        try:
            image = pg.image.load(os.path.join(image_path, name)).convert_alpha()
            image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            tile_images.append(image)
        except FileNotFoundError:
            print(f"Archivo '{name}' no encontrado en '{image_path}'.")
            sys.exit(1)

    return tile_images

def load_player_images():
    player_images = []
    image_paths = ["player/player_down.png", "player/player_up.png", "player/player_left.png", "player/player_right.png"]

    for path in image_paths:
        try:
            image = pg.image.load(os.path.join(image_path, path)).convert_alpha()
            player_images.append(image)
        except FileNotFoundError:
            print(f"Archivo '{path}' no encontrado en '{image_path}'.")
            sys.exit(1)

    return player_images

def load_bomb_images():
    bomb_images = []
    image_paths = ["bomb/1.png", "bomb/2.png", "bomb/3.png", "explosion/1.png", "explosion/2.png", "explosion/3.png"]

    for path in image_paths:
        try:
            image = pg.image.load(os.path.join(image_path, path)).convert_alpha()
            bomb_images.append(image)
        except FileNotFoundError:
            print(f"Archivo '{path}' no encontrado en '{image_path}'.")
            sys.exit(1)

    return bomb_images

class Map():
    def __init__(self, grid):
        
        self.grid = grid
        
    def draw_map(self, screen, tile_images):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                # 0: pasto, 1: caja, 2: bloque
                if tile == 0:
                    screen.blit(tile_images[0], (x*TILE_SIZE, y*TILE_SIZE))
                elif tile == 1:
                    screen.blit(tile_images[1], (x*TILE_SIZE, y*TILE_SIZE))
                elif tile == 2:
                    screen.blit(tile_images[2], (x*TILE_SIZE, y*TILE_SIZE))

    def get_tile(self, x, y):

        if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
            return 1
        return self.grid[y][x]

    def update_map(self, x, y, tile_type):
        if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
            return
        if tile_type == 2:

            self.grid[y][x] = 0
        else:
            # Si se agregó una caja, actualizar la grilla del mapa con una caja
            self.grid[y][x] = tile_type
    