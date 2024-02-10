import random
import time
import numpy as np
import pygame as pg

from typing import Tuple, List, Any

# PyGame constants:
WIDTH: int = 80
HEIGHT: int = 60
CELL_SIZE: int = 1

# Smoothlife constants:
r_a: int = 12
alpha_m: float = 0.147
alpha_n: float = 0.028
b_1: float = 0.278
b_2: float = 0.365
d_1: float = 0.267
d_2: float = 0.445

def sigma_1(x: float, a: float, alpha: float) -> float:
    return 1/(1 + np.exp(-(x-a)*4/alpha))

def sigma_2(x: float, a: float, b: float) -> float:
    return sigma_1(x,a, alpha_n) * (1 - sigma_1(x, b, alpha_n))

def sigma_m(x: float, y: float, m: float) -> float:
    return x * (1 - sigma_1(m, 0.5, alpha_m)) + y * sigma_1(m, 0.5, alpha_m)

def s(n: float, m: float) -> float:
    return sigma_2(n, sigma_m(b_1, d_1, m), sigma_m(b_2, d_2, m))



def display_grid(screen: pg.Surface, grid: np.ndarray) -> None:
    for row, col in np.ndindex(grid.shape):
        colour = grid[row][col]
        if colour < 0: colour = 0
        if colour > 1: colour = 1
        colour = (colour, colour, colour)
        print(colour)
        pg.draw.rect(screen, colour, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pg.display.update()

def update_map(grid: np.ndarray, nextGrid: np.ndarray) -> None:
    for xi in range(WIDTH): 
        for yi in range(HEIGHT):
            m: float = 0  # the integral value
            M: int = 0  # the scaling factor M
            n: float = 0  # the integral value
            N: int = 0  # the scaling factor
            r_i: float = r_a / 3
            
            for dx in range(-(r_a-1), r_a, 1):
                for dy in range(-(r_a-1), r_a, 1):
                    x = (((xi+dx)%WIDTH + WIDTH)%WIDTH) // CELL_SIZE
                    y = (((yi+dy)%HEIGHT + HEIGHT)%HEIGHT) // CELL_SIZE
                    if dx**2 + dy**2 <= r_i**2:
                        m += grid[y][x]
                        M += 1
                    else:
                        n += grid[y][x]
                        N += 1
            m /= M
            n /= N
            nextGrid[yi][xi] = 2*s(n,m) - 1


def main_pg():
    # initialise pygame
    pg.init()
    
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    grid = np.random.rand(HEIGHT // CELL_SIZE, WIDTH  // CELL_SIZE)
    nextGrid = np.zeros((HEIGHT // CELL_SIZE, WIDTH  // CELL_SIZE))
    screen.fill((30, 30, 30))
    pg.display.flip()
    
    
    running = False
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                    display_grid(screen, grid)
                    
            if running:
                update_map(grid, nextGrid)
                grid, nextGrid = nextGrid, grid
                display_grid(screen, grid)
            time.sleep(0.01)

def main_cl() -> None:
    # todo: implement terminal-based display
    pass
if __name__ == "__main__":
    main_pg()
    