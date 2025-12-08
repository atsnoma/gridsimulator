# gridsimulator
We are going to make a tactics-like game, even if it kills us.


------
Updated: madyucky 2025.11.21

Files and what they do in order of easy explanations:

config.py *******************************

Contains all of our magic numbers that need to be referenced across different files. This includes:
- Window Settings
- Grid Settings
- Colors
- Base Unit Stats
- Alignments (1 = ally, 2 = enemy)


grid.py **********************************

Contains all of the grid commands thus far.
- Grid size calculations and drawing the grid.


turn_manager.py **************************

Contains all of the code for processing turns and turn changes, mostly queried by input_manager
- Gives actions to player on player phase
- Marks units after they act so each unit acts once per turn
- Checks to end turn
- Removes dead units from active lists


input_manager.py *************************

Contains all of the code for processing player inputs
- Reads Mouse position and clicks
- Draws highlights when hovering over a grid square
- Changes color of unit when clicked to show selected state
- Handles logic for unit movement and attack issuing (on-click events)


unit.py ***********************************

Contains all of the code for units so that other systems can change their stuffs
- Unit class takes position, alignment, name at generation, but is unused at base and inherited into specialized units
- Initializes health, attack range, movement range for units; also sets alive to true, selected to false
- Processes unit drawing, determining unit movement with Manhattan distance, method for unit death
- Currently only has Archer subclass, many more to come


main.py **********************************

Contains the actual game with all of the code imported and brought together in one glorious while loop
- Initializes base settings like tick rate, window size, window name
- Loads units into lists, initializes turn_manager and input_manager
- Draws the grid and units, with logic to not draw dead units
- Just runs input_manager pretty much