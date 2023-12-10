from .bomb import *

class Inventory:
    def __init__(self):
        self.bombs = []  

    def add_bomb(self, bomb):
        self.bombs.append(bomb) 

    def remove_bomb(self, bomb):
        if self.bombs:
            self.bombs.remove(bomb)  
        else:
            print("No hay bombas en el inventario")

    def has_bomb(self):
        return len(self.bombs) > 0  

