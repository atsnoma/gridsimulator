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
        self.phase = "move"
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
                    continue  # skip units that acted or are dead
                if u.x == tile_x and u.y == tile_y:
                    if self.turn_manager.is_unit_active(u):
                        u.selected = True
                        self.selected_unit = u
                        self.phase = "move"
                        self.selected_unit.original_position = (tile_x, tile_y)
                        return
            return

        ## If a unit IS selected, remove tiles containing a unit from valid move spaces, then allow moves
        if self.phase == "move":
            all_moves = self.selected_unit.get_move_tiles(config.GRID_WIDTH, config.GRID_HEIGHT)
            valid_move_tiles = []
            for tile in all_moves:
                blocked = False
                for u in units:
                    if u.alive and (u.x, u.y) == tile and u is not self.selected_unit:
                        blocked = True
                        break
                if not blocked:
                    valid_move_tiles.append(tile)
            
            if (tile_x, tile_y) in valid_move_tiles:
                # If legal, move the unit and send to action phase
                self.selected_unit.move_unit(tile_x, tile_y)
                self.phase = "action"
                return
            else:
                # Clicked invalid tile → cancel selection, revert if moved
                self.selected_unit.handle_action(action_type="cancel_move")
                self.selected_unit.selected = False
                self.selected_unit = None
                self.phase = "move"
                return
        
        if self.phase == "action":
            # Set target variable and get valid attack tiles
            target = None
            valid_attack_tiles = self.selected_unit.get_attack_tiles(config.GRID_WIDTH, config.GRID_HEIGHT)

            for u in units:
                # If the clicked unit for action is not an ally, then it will be accepted as a target
                if u.alive and self.selected_unit.alignment != u.alignment:
                    if (u.x, u.y) == (tile_x, tile_y) and (tile_x, tile_y,) in valid_attack_tiles:
                            target = u
                            break
            if target:
                self.selected_unit.handle_action(target=target, action_type="attack") # No menu yet, just straight attacks
                self.turn_manager.mark_unit_acted(self.selected_unit)
                self.turn_manager.check_end_turn()
                self.selected_unit.selected = False
                self.selected_unit = None
                self.phase = "move"
                return
            
            elif (tile_x, tile_y) == (self.selected_unit.x, self.selected_unit.y):
                # If clicking on self in action phase, passes the unit's turn.
                self.selected_unit.handle_action(action_type="wait")
                self.turn_manager.mark_unit_acted(self.selected_unit)
                self.turn_manager.check_end_turn()
                self.selected_unit.selected = False
                self.selected_unit = None
                self.phase = "move"
                return
            
            else:
                # If clicking on an invalid area, goes back to move selection
                self.selected_unit.handle_action(action_type="cancel_move")
                self.phase = "move"
                return
        ## If nothing clicked, nothing happens
        print("Yes I exist")
        self.turn_manager.mark_unit_acted(self.selected_unit)
        self.turn_manager.check_end_turn()
        self.selected_unit.selected = False
        self.selected_unit = None
        self.phase = "move"
            

    def draw_hover(self, screen):
        if self.hovered_tile != (None, None):
            rect = pygame.Rect(
                self.hovered_tile[0] * config.TILE_SIZE,
                self.hovered_tile[1] * config.TILE_SIZE,
                config.TILE_SIZE,
                config.TILE_SIZE
            )
            pygame.draw.rect(screen, config.HOVER_COLOR, rect, 3)
    
    def draw_range(self, screen, unit):
        ##Draw a highlight around all tiles a selected unit can move to or attack to.
        if self.phase == "move":
            tiles = unit.get_move_tiles(config.GRID_WIDTH, config.GRID_HEIGHT)
            color = (0, 100, 255)
        elif self.phase == "action":
            tiles = unit.get_attack_tiles(config.GRID_WIDTH, config.GRID_HEIGHT)
            color = (255, 100, 0)
    
        for tx, ty in tiles:
            rect = pygame.Rect(tx * config.TILE_SIZE, ty * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE)
            pygame.draw.rect(screen, color, rect, 3)  # blue border

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