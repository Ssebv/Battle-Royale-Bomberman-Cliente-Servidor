import pygame as pg
from .map import *

class Bomb:
    def __init__(self):
        
        self.images = [pg.transform.scale(img, (TILE_SIZE-8, TILE_SIZE-8)) for img in load_bomb_images()]
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.explode_time = 0.4
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.is_exploded = None
        self.is_active = None
        self.animation_completed = None
        self.hit_player = None
        self.in_inventory = True
        self.position = None
        
    
    def place_bomb(self, square_topleft):

        square_x, square_y = square_topleft
        bomb_x = square_x + (TILE_SIZE - self.rect.width) / 2
        bomb_y = square_y + (TILE_SIZE - self.rect.height) / 2
        self.rect.topleft = (bomb_x, bomb_y) 

        self.is_active = True
        self.elapsed_time = 0.0
        self.current_frame = 0
        self.animation_completed = False
        self.hit_player = False
        self.is_exploded = False
        
        self.position = (bomb_x, bomb_y)

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.explode_time:
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.animation_completed = True
                self.is_active = False
                
            else:
                self.image = self.images[self.current_frame]
                self.elapsed_time = 0.0
            
            if self.current_frame >= 3:
                self.is_exploded = True

    def draw(self, screen):
        if not self.animation_completed:
            screen.blit(self.image, self.rect)  
   