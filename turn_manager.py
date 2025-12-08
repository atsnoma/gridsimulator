'''
***************************************************************************
Filename: turn_manager.py
Author: FungusPlatypus
Date: 2025.11.21
Modifications: Fungusplatypus - 2025.11.21
Description: This module demonstrates:
1) TurnManager class for handling turns, creating logic for InputManager to restrict unit actions by faction
2) Need to convert factions like player_units to ALLY potentially (as used in unit.py)
3) Future: Need for a third neutral faction? Where does Cutscene Logic go?
***************************************************************************
'''

import pygame
import config

class TurnManager:
    def __init__(self, player_units, enemy_units):
        self.player_units = player_units
        self.enemy_units = enemy_units
        self.current_team = "player"  # "player" or "enemy"
        self.units_acted = set()      # track units that already acted this turn
    
    def start_turn(self, team):
        ## Start new turn for team
        ## Clears has_acted and has_moved flags, though only has_acted needs to be cleared
        self.current_team = team
        self.units_acted.clear()
        if team == "player":
            for u in self.player_units:
                u.has_acted = False
                u.has_moved = False
        else:
            for u in self.enemy_units:
                u.has_acted = False
                u.has_moved = False
        ## Animations here maybe
    
    def end_turn(self):
        ##Switch to the other team.
        if self.current_team == "player": 
            next_team = "enemy" 
        else:
            next_team = "player"
        self.start_turn(next_team)

    def is_unit_active(self, unit):
        ##Return True if this unit can act this turn.
        if self.current_team == "player" and unit in self.player_units:
            return unit not in self.units_acted
        elif self.current_team == "enemy" and unit in self.enemy_units:
            return unit not in self.units_acted
        return False

    def mark_unit_acted(self, unit):
        ##Mark a unit as having finished its action.
        self.units_acted.add(unit)


    def check_end_turn(self):
        self.remove_dead_units(self.player_units, self.enemy_units)
        all_acted = True
        if self.current_team == "player":
            for u in self.player_units:
                if u not in self.units_acted:
                    all_acted = False
        else:
            for u in self.enemy_units:
                if u not in self.units_acted:
                    all_acted = False
        if all_acted:
            self.end_turn()

    def remove_dead_units(self, player_units, enemy_units):
        player_units[:] = [u for u in player_units if u.alive]
        enemy_units[:] = [u for u in enemy_units if u.alive]