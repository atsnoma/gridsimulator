'''
***************************************************************************
Filename: input_manager.py
Author: BarretxFtXfL
Date: 2025.11.21
Modifications: BarretxFtXfL- 2025.11.21
Description: This module demonstrates:
1) InputManager class for handling mouse position and clicks
2) Also handles showing unit movement range on click since it is an on-click event
3) Future: Will this handle opening menus??
***************************************************************************
'''

import pygame
import config

class InputManager:
    def __init__(self, turn_manager):
        self.turn_manager = turn_manager
        self.selected_unit = None
        self.hovered_tile = (None, None)

    def get_hovered_tile(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_tile = (mouse_pos[0] // config.TILE_SIZE,
                             mouse_pos[1] // config.TILE_SIZE)
        return self.hovered_tile

    def handle_click(self, units):
        ## Get the tile that the mouse is hovering over
        tile_x, tile_y = self.hovered_tile
        ## If no unit is selected and a valid unit is on the tile, make it selected
        if self.selected_unit is None:
            for u in units:
                if not u.alive:
                    continue  # skip dead units
                if u.x == tile_x and u.y == tile_y:
                    if self.turn_manager.is_unit_active(u):
                        u.selected = True
                        self.selected_unit = u
                        break
        ## If a unit IS selected, check that a valid unit is on the tile, check if valid target, and ranged attack
        else:
            for u in units:
                if not u.alive:
                    continue  # skip dead units
                if u.x == tile_x and u.y == tile_y:
                    if self.selected_unit.alignment != u.alignment:
                        self.selected_unit.basic_attack(u)
                        self.turn_manager.mark_unit_acted(self.selected_unit)
                        self.turn_manager.check_end_turn()
                        self.selected_unit.selected = False
                        self.selected_unit = None
                        return
        ## If unit is selected and clicks a valid tile, move it and end turn. Otherwise nothing happens.                
            valid_tiles = self.selected_unit.get_move_tiles(config.GRID_WIDTH, config.GRID_HEIGHT)
            if (tile_x, tile_y) in valid_tiles:
                self.selected_unit.x = tile_x
                self.selected_unit.y = tile_y
                self.turn_manager.mark_unit_acted(self.selected_unit)
                self.turn_manager.check_end_turn()
            self.selected_unit.selected = False
            self.selected_unit = None
            

    def draw_hover(self, screen):
        if self.hovered_tile != (None, None):
            rect = pygame.Rect(
                self.hovered_tile[0] * config.TILE_SIZE,
                self.hovered_tile[1] * config.TILE_SIZE,
                config.TILE_SIZE,
                config.TILE_SIZE
            )
            pygame.draw.rect(screen, config.HOVER_COLOR, rect, 3)
    
    def draw_move_range(self, screen, unit):
        ##Draw a highlight around all tiles a selected unit can move to.
        if unit.selected:
            move_tiles = unit.get_move_tiles()
            for possiblex, possibley in move_tiles:
                rect = pygame.Rect(
                    possiblex * config.TILE_SIZE,
                    possibley * config.TILE_SIZE,
                    config.TILE_SIZE,
                    config.TILE_SIZE
                )
                pygame.draw.rect(screen, (0, 100, 255), rect, 3)  # blue border

    # Optional: process all events
    def process_events(self, units):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left mouse click
                self.handle_click(units)
        self.get_hovered_tile()
        return True