import random
import time
import numpy as np
import pygame as pg
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Colours:
    """Stores constants for colouur values
    """
    background: Tuple[int] = (10, 10, 10)
    grid: Tuple[int] = (40, 40, 40)
    alive: Tuple[int] = (255, 255, 255)
    

def display_grid(screen: pg.Surface, grid: np.ndarray, cellSize: int) -> None:
    for row, col in np.ndindex(grid.shape):
        colour = Colours.background if grid[row, col] == 0 else Colours.alive
        pg.draw.rect(screen, colour, (col * cellSize, row * cellSize, cellSize-1, cellSize-1))
    pg.display.update()


def update(grid: np.ndarray):
    nextGrid = np.zeros((grid.shape[0], grid.shape[1]))
    for row, col in np.ndindex(grid.shape):
        numNeighbours = np.sum(grid[row-1:row+2, col-1:col+2]) - grid[row, col]  # the number of alive neighbours this cell currently has
        
        if grid[row, col] == 1:  # if cell is currently alive
            if 2 <= numNeighbours <= 3:
                nextGrid[row, col] = 1
            
        else:  # else current cell must be dead
            nextGrid[row, col] = int(numNeighbours == 3)
    grid = nextGrid
    return grid
            
    

def main():
    pg.init()
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    CELL_SIZE = 7
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    grid = np.zeros((WINDOW_HEIGHT // CELL_SIZE, WINDOW_WIDTH // CELL_SIZE))
    
    screen.fill(Colours.grid)
    pg.display.flip()
    display_grid(screen, grid, CELL_SIZE)
    
    running = False
    mouseHeld = False
    placeType = 1
    while True:
        for event in pg.event.get():
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                if not mouseHeld:
                    mouseHeld = True
                    placeType = int(not bool(grid[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE]))
                grid[min(WINDOW_HEIGHT-1, pos[1]) // CELL_SIZE, min(pos[0], WINDOW_WIDTH-1) // CELL_SIZE] = placeType
                display_grid(screen, grid, CELL_SIZE)
                continue
            else:
                mouseHeld = False
            
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                    display_grid(screen, grid, CELL_SIZE)
                elif event.key == pg.K_f:
                    grid = np.ones((WINDOW_HEIGHT // CELL_SIZE, WINDOW_WIDTH // CELL_SIZE))
                    display_grid(screen, grid, CELL_SIZE)
        screen.fill(Colours.grid)
        
        if running:
            grid = update(grid)
            display_grid(screen, grid, CELL_SIZE)
            
        time.sleep(0.01)

if __name__ == "__main__":
    main()