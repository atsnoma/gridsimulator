'''
***************************************************************************
Filename: main.py
Author: mafiaofplums
Date: 2025.11.21
Modifications: mafiaofplums - 2025.11.21
Description: This module demonstrates:
1) Integration of all other files for the game loop
2) Need replace the Create Units block with importing whole levels
3) Keep the while loop focused on drawing, or calling single methods referring to other files
***************************************************************************
'''

import pygame
from grid import Grid
from unit import Unit, Archer
from input_manager import InputManager
from turn_manager import TurnManager
import config

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Grid Simulator")
clock = pygame.time.Clock()

## Create Units
player_units = [
    Archer(1, 1),
    Archer(2, 1),
]

enemy_units = [
    Archer(5, 5, config.ENEMY),
    Archer(6, 5, config.ENEMY),
]

# All units together for InputManager drawing / clicks
all_units = player_units + enemy_units


# Create grid, unit(s), and input manager
grid = Grid()
units = all_units
turn_manager = TurnManager(player_units, enemy_units)
input_manager = InputManager(turn_manager)

## *******************************************************

running = True
while running:
    running = input_manager.process_events(units)

    screen.fill(config.BACKGROUND_COLOR)
    grid.draw(screen)
    input_manager.draw_hover(screen)
    for u in units:
        if u.alive:
            u.draw(screen)
    if input_manager.selected_unit:
        input_manager.draw_move_range(screen, input_manager.selected_unit)
    pygame.display.flip()
    clock.tick(config.FPS)