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
class Point:
    x: int
    y: int

    def points_near_in_rect(self, distance: int) -> Iterator['Point']:
        for y in range(int(self.y - distance), int(self.y + distance)):
            for x in range(int(self.x - distance), int(self.x + distance)):
                yield Point(x, y)

@dataclass
class Map:
    __mapa: np.ndarray[tuple[int, int]]
    __width: int
    __height: int

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__mapa = np.empty((height, width), dtype=Tile)

    def tile_at(self, point: Point) -> Tile:
        return self.__mapa[point.y][point.x]

    def center(self) -> Point:
        return Point(self.__width // 2, self.__height // 2)

    def valid(self, point: Point) -> bool:
        return 0 <= point.y < self.__height and 0 <= point.x < self.__width

    def set_tile(self, point: Point, tile: Tile) -> None:
        self.__mapa[point.y][point.x] = tile

    def shortest_side(self) -> int:
        return min(self.__width, self.__height)

    def all_points(self) -> Iterator[Point]:
        for y in range(0, self.__height):
            for x in range(0, self.__width):
                yield Point(x, y)

    def fill(self, tile: Tile) -> None:
        for point in self.all_points():
            self.set_tile(point, tile)

    def is_tile_in_range(self, point: Point, range_: int, tile: Tile) -> bool:
        for yy in range(point.y - range_, point.y + range_ + 1):
            for xx in range(point.x - range_, point.x + range_ + 1):
                c = Point(xx, yy)
                if self.valid(c) and self.tile_at(c) == tile:
                    return True
        return False

def main():
    window_size = (600, 480)
    tile_size = 8
    width = int(window_size[0] / tile_size)
    height = int(window_size[1] / tile_size)
    renderer = sdl_init_renderer(window_size)
    while True:
        map = generate_map(width, height)
        render_map(renderer, map, tile_size)

def generate_map(width: int, height: int) -> Map:
    map = Map(width, height)
    map.fill(Tile.WATER)
    add_grass_to(map, map.shortest_side() // 4)
    add_sands_to(map)
    return map

def add_grass_to(map: Map, radius: int):
    generate_island(
        map,
        center=map.center(),
        radius=radius,
        neighbours=np.random.randint(4, 7),
        iterations=radius / pow(radius / 8, 2))

def add_sands_to(map: Map):
    for point in map.all_points():
        if map.tile_at(point) == Tile.GRASS:
            if map.is_tile_in_range(point, 2, Tile.WATER):
                map.set_tile(point, Tile.SAND)

def generate_island(map: Map, center: Point, radius, neighbours, iterations):
    if iterations > 0:
        for point in grass_points(map, center, radius):
            map.set_tile(point, Tile.GRASS)
        for i in range(1, int(neighbours)):
            angle = np.random.uniform(0, 2 * np.pi)
            r = radius * np.random.uniform(1 / 2, 6 / 8)
            generate_island(
                map,
                Point(
                    center.x + 2 * r * np.sin(angle),
                    center.y + 2 * r * np.cos(angle),
                ),
                r,
                np.random.randint(4, 7),
                iterations - 1)

def grass_points(map: Map, center: Point, radius: int) -> Iterator[Point]:
    for point in center.points_near_in_rect(radius):
        if map.valid(point):
            if np.pow(center.x - point.x, 2) + np.pow(center.y - point.y, 2) < np.pow(radius, 2) * 0.995:
                yield Point(point.x, point.y)

def sdl_init_renderer(window_size: tuple[int, int]) -> sdl2.ext.Renderer:
    sdl2.ext.init()
    window = sdl2.ext.Window("Island Generator", window_size)
    window.show()
    return sdl2.ext.Renderer(window)

def render_map(renderer: sdl2.ext.Renderer, map: Map, tile_size: int):
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            sdl2.ext.quit()
            sys.exit(0)
    renderer.color = sdl2.ext.Color(48, 48, 48)
    renderer.clear()
    render_map_tiles(renderer, map, tile_size)
    renderer.present()
    time.sleep(1)

def render_map_tiles(renderer, map: Map, tile_size: int):
    for point in map.all_points():
        renderer.color = tile_color(map.tile_at(point))
        renderer.fill(sdl2.SDL_Rect(
            tile_size * point.x,
            tile_size * point.y,
            tile_size,
            tile_size))

def tile_color(tile: Tile) -> sdl2.ext.Color:
    if tile == Tile.WATER:
        return sdl2.ext.Color(64, 64, 192)
    if tile == Tile.SAND:
        return sdl2.ext.Color(192, 192, 128)
    if tile == Tile.GRASS:
        return sdl2.ext.Color(64, 128, 64)
