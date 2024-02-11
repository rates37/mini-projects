import random
import time
import numpy as np
import pygame as pg

from typing import Tuple, List, Any
from math import floor

# PyGame constants:
WIDTH: int = floor(600/1.5)
HEIGHT: int = floor(600/1.5)
CELL_SIZE: int = 10

# Terminal constants:
brightness = " ░▒▓█"
# brightness = " .-=coaA@#"

# Smoothlife constants:
r_a: int = 9
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
        colour = (colour*255, colour*255, colour*255)
        # print(colour)
        pg.draw.rect(screen, colour, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    pg.display.update()

def compute_delta_grid(grid: np.ndarray, nextGrid: np.ndarray) -> None:
    width = WIDTH //CELL_SIZE
    height = HEIGHT // CELL_SIZE
    for xi in range(width): 
        for yi in range(height):
            m: float = 0  # the integral value
            M: int = 0  # the scaling factor M
            n: float = 0  # the integral value
            N: int = 0  # the scaling factor
            r_i: float = r_a / 3
            
            for dx in range(-(r_a-1), r_a, 1):
                for dy in range(-(r_a-1), r_a, 1):
                    x = (((xi+dx)%width + width)%width)
                    y = (((yi+dy)%height + height)%height)
                    if dx**2 + dy**2 <= r_i**2:
                        m += grid[y][x]
                        M += 1
                    elif dx**2 + dy**2 <= r_a**2:
                        n += grid[y][x]
                        N += 1
            m /= M
            n /= N
            nextGrid[yi][xi] = 2*s(n,m) - 1


def restrict(val: float, lower: float=0, upper: float=1) -> float:
    if val < lower: return lower
    if val > upper: return upper
    return val


def main_pg():
    # initialise pygame
    pg.init()
    
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    grid = np.random.rand(HEIGHT // CELL_SIZE, WIDTH  // CELL_SIZE)
    nextGrid = np.zeros((HEIGHT // CELL_SIZE, WIDTH  // CELL_SIZE))
    screen.fill((30, 30, 30))
    pg.display.flip()
    display_grid(screen, grid)
    
    running = False
    i: int = 0
    
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
                compute_delta_grid(grid, nextGrid)
                for row, col in np.ndindex(grid.shape):
                    grid[row][col] = restrict(grid[row][col] + 0.05*nextGrid[row][col])
                display_grid(screen, grid)
                print("displayed!", i)
                i += 1
            time.sleep(0.1)


if __name__ == "__main__":
    main_cl_C()
    