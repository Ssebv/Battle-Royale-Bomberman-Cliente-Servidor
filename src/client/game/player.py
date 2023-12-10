import pygame as pg
from .map import *
from .inventory import *
from .bomb import *

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        
        self.image = load_player_images()[0]
        self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3
        self.life = 3
        self.kills = 0
        self.is_alive = True
        self.inventory = Inventory()
        self.inventory.add_bomb(Bomb()) 
        self.bombs_thrown = []  
        self.direction = None

    def update(self, keys_pressed, game_map): 
        dx, dy = 0, 0
        
        if keys_pressed[pg.K_w]:
            self.image = load_player_images()[1]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            dy -= self.speed
            self.direction = 'up'

        elif keys_pressed[pg.K_s]:
            self.image = load_player_images()[0]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            dy += self.speed
            self.direction = 'down'

        elif keys_pressed[pg.K_a]:
            self.image = load_player_images()[2]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            dx -= self.speed
            self.direction = 'left'

        elif keys_pressed[pg.K_d]:
            self.image = load_player_images()[3]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            dx += self.speed
            self.direction = 'right'

        temp_x = self.rect.x + dx
        temp_y = self.rect.y + dy

        new_rect = pg.Rect(temp_x, temp_y, self.rect.width, self.rect.height)

        for row in range(len(game_map.grid)):
            for col in range(len(game_map.grid[row])):
                if game_map.grid[row][col] != 0:
                    block_rect = pg.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if new_rect.colliderect(block_rect):
                        if dx > 0:
                            self.rect.right = block_rect.left
                        elif dx < 0:
                            self.rect.left = block_rect.right
                        if dy > 0:
                            self.rect.bottom = block_rect.top
                        elif dy < 0:
                            self.rect.top = block_rect.bottom
                        return new_rect
            
        self.rect.x = temp_x
        self.rect.y = temp_y
        
        return new_rect 
            
    def throw_bomb(self, position):
        if self.inventory.has_bomb():
            bomb = self.inventory.bombs[0] 
            bomb.place_bomb(position)  

            self.inventory.remove_bomb(bomb)  
            self.bombs_thrown.append(bomb)  
            return bomb

        else:
            print("No hay bombas en el inventario")
            return None

    def draw(self, screen):
        if self.image is not None and self.rect is not None:
            screen.blit(self.image, self.rect)
            
    def render(self, screen):
        if self.direction == 'up':
            self.image = load_player_images()[1]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)) 
        elif self.direction == 'down':
            self.image = load_player_images()[0]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        elif self.direction == 'left':
            self.image = load_player_images()[2]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        elif self.direction == 'right':
            self.image = load_player_images()[3]
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

            


            
        