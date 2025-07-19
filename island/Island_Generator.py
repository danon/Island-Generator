import enum
import os
import sys
from dataclasses import dataclass
from typing import Iterator

os.environ["PYSDL2_DLL_PATH"] = r"..\SDL2-2.32.2-win32-x64"
import sdl2
import sdl2.ext
import numpy as np
import time

class Tile(enum.StrEnum):
    WATER = '.'
    SAND = ':'
    GRASS = '#'

@dataclass
class Cell:
    x: int
    y: int

@dataclass
class Map:
    mapa: np.ndarray[tuple[int, int]]
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.mapa = np.empty((height, width), dtype=Tile)

    def tile_at(self, cell: Cell) -> Tile:
        return self.mapa[cell.y][cell.x]

    def set_tile(self, cell: Cell, tile: Tile) -> None:
        self.mapa[cell.y][cell.x] = tile

    def shortest_side(self) -> int:
        return min(self.width, self.height)

    def all_cells(self) -> Iterator[Cell]:
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield Cell(x, y)

    def fill(self, tile: Tile) -> None:
        for cell in self.all_cells():
            self.set_tile(cell, tile)

    def is_tile_in_range(self, cell: Cell, range_: int, tile: Tile) -> bool:
        x = cell.x
        y = cell.y
        for yy in range(y - range_, y + range_ + 1):
            for xx in range(x - range_, x + range_ + 1):
                cell = Cell(xx, yy)
                if 0 <= xx < self.width and 0 <= yy < self.height and self.tile_at(cell) == tile:
                    return True

        return False

def main():
    window_size = (600, 480)
    tile_size = 8
    run_application(
        window_color=sdl2.ext.Color(48, 48, 48),
        width=int(window_size[0] / tile_size),
        height=int(window_size[1] / tile_size),
        tile_size=tile_size,
        window_size=window_size,
    )

def run_application(
        window_color: sdl2.ext.Color,
        width: int,
        height: int,
        tile_size: int,
        window_size,
):
    sdl2.ext.init()
    window = sdl2.ext.Window("Island Generator", window_size)
    window.show()
    renderer = sdl2.ext.Renderer(window)
    while True:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                sdl2.ext.quit()
                sys.exit(0)
        renderer.color = window_color
        renderer.clear()
        draw_map(
            renderer,
            generate_map(width, height),
            tile_size)
        renderer.present()
        time.sleep(1)

def generate_map(width: int, height: int) -> Map:
    map = Map(width, height)
    map.fill(Tile.WATER)
    add_grass_to(map, map.shortest_side() / 4)
    add_sands_to(map)
    return map

def add_grass_to(map: Map, radius: int) -> Map:
    generate_island(
        map,
        center_x=map.width / 2,
        center_y=map.height / 2,
        radius=radius,
        neighbours=np.random.randint(4, 7),
        iterations=radius / pow(radius / 8, 2))

def add_sands_to(map: Map):
    for cell in map.all_cells():
        if map.tile_at(cell) == Tile.GRASS:
            if map.is_tile_in_range(cell, 2, Tile.WATER):
                map.set_tile(cell, Tile.SAND)

def generate_island(map: Map, center_x, center_y, radius, neighbours, iterations):
    if iterations > 0:
        for y in range(int(center_y - radius), int(center_y + radius)):
            for x in range(int(center_x - radius), int(center_x + radius)):
                if 0 <= y < map.height and 0 <= x < map.width:
                    if np.pow(center_x - x, 2) + np.pow(center_y - y, 2) < np.pow(radius, 2) * 0.995:
                        map.set_tile(Cell(x, y), Tile.GRASS)

        for i in range(1, int(neighbours)):
            angle = np.random.uniform(0, 2 * np.pi)
            r = radius * np.random.uniform(1 / 2, 6 / 8)
            generate_island(
                map,
                center_x + 2 * r * np.sin(angle),
                center_y + 2 * r * np.cos(angle),
                r,
                np.random.randint(4, 7),
                iterations - 1)

def draw_map(renderer, map: Map, tile_size: int):
    for cell in map.all_cells():
        renderer.color = tile_color(map.tile_at(cell))
        renderer.fill(sdl2.SDL_Rect(tile_size * cell.x, tile_size * cell.y, tile_size, tile_size))

def tile_color(tile: Tile) -> sdl2.ext.Color:
    if tile == Tile.WATER:
        return sdl2.ext.Color(64, 64, 192)
    if tile == Tile.SAND:
        return sdl2.ext.Color(192, 192, 128)
    if tile == Tile.GRASS:
        return sdl2.ext.Color(64, 128, 64)
