'''
***************************************************************************
Filename: unit.py
Author: SkyScaryNew
Date: 2025.11.21
Modifications: SkyScaryNew - 2025.11.21
Description: This module demonstrates:
1) Unit Class for units, including drawing them and getting their movement range
2) Future: Unit subclasses? Unit health, stats, etc.
***************************************************************************
'''

import pygame
import config


## Unit Class
class Unit:
    def __init__(self, x, y, alignment, name):
        ## Determines unit spawn location, color, movement range
        self.x = x
        self.y = y
        self.alignment = alignment
        self.name = name
        self.health = config.BASEHEALTH
        self.alive = True
        self.selected = False
        self.attack_range = config.BASERANGE
        self.move_range = config.BASEMOVE

    def draw(self, screen, tile_size=config.TILE_SIZE):
        ## Draws the unit, changes color based on selection or not.
        if self.selected:
            color = (0, 255, 0)  # green for selected
        elif self.alignment == config.ALLY:
            color = (0, 0, 255)  # blue for player units
        elif self.alignment == config.ENEMY:
            color = (255, 0, 0)  # red for enemies
        else:
            color = (100, 100, 100) # Gray for default

        rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, color, rect)
        
    def get_move_tiles(self, grid_width=config.GRID_WIDTH, grid_height=config.GRID_HEIGHT):
        tiles = []
        for dx in range(-self.move_range, self.move_range + 1):
            for dy in range(-self.move_range, self.move_range + 1):
                if abs(dx) + abs(dy) <= self.move_range:
                    tx = self.x + dx
                    ty = self.y + dy
                    if 0 <= tx < grid_width and 0 <= ty < grid_height:
                        tiles.append((tx, ty))
        return tiles
    
    def basic_attack(self, target):
        damage = 3  # flat damage for now
        target.health -= damage
        if target.health <= 0:
            target.health = 0  # optional clamp
            target.unit_death()
        else:
            print(f"{target.name} has {target.health} remaining!")

            
    
    def unit_death(self):
        print(f"{self.name} has died!")
        self.alive = False  # mark as dead
        
## Subclass for Archer Unit
class Archer(Unit):
    def __init__(self, x, y, alignment=config.ALLY, name="Archer"):
        super().__init__(x, y, alignment, name)
        self.move_range = config.BASEMOVE - 1
        self.attack_range = config.BASERANGE + 2
        self.health = config.BASEHEALTH - 2
