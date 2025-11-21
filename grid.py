'''
***************************************************************************
Filename: grid.py
Author: jt steele
Date: 2025.11.21
Modifications: jt steele - 2025.11.21
Description: This module demonstrates:
1) A Grid class for drawing the grid beneath the maps, based on constraints in config.py
***************************************************************************
'''

import pygame
import config

class Grid:
    '''
    Easiest class of my life... hopefully. We will have to undraw and redraw the grid in between battle phases,
    hopefully that will not be too hard. It is a million years away though so whatever
    '''
    def __init__(self, width=config.GRID_WIDTH, height=config.GRID_HEIGHT, tile_size=config.TILE_SIZE):
        self.width = width
        self.height = height
        self.tile_size = tile_size

    '''
    At default, the grid is 10x10, so the function draws a funny little 10x10 grid of tiles at size 48.
    '''
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(screen, config.GRID_COLOR, rect, 1)