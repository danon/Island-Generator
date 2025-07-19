import enum
import os
import sys

os.environ["PYSDL2_DLL_PATH"] = r"..\SDL2-2.32.2-win32-x64"
import sdl2
import sdl2.ext
import numpy as np
import time

class Tile(enum.StrEnum):
    WATER = '.'
    SAND = ':'
    GRASS = '#'

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
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                sdl2.ext.quit()
                sys.exit(0)
        renderer.color = window_color
        renderer.clear()
        draw_map(
            renderer,
            generate_map(width, height),
            width,
            height,
            tile_size)
        renderer.present()
        time.sleep(1)

def generate_map(width: int, height: int):
    mapa = generate_filled_map(width, height, Tile.WATER)
    radius = min(width, height) * 1 / 4
    generate_island(
        mapa,
        width,
        height,
        width / 2,
        height / 2,
        radius=radius,
        neighbours=np.random.randint(4, 7),
        iterations=radius / pow(radius / 8, 2))
    add_sands_to(mapa, width, height)
    return mapa

def generate_filled_map(width: int, height: int, tile: Tile):
    map = np.empty((height, width), dtype=str)
    for y in range(0, height):
        for x in range(0, width):
            map[y][x] = tile
    return map

def add_sands_to(mapa, width, height):
    for y in range(0, height):
        for x in range(0, width):
            if mapa[y][x] == Tile.GRASS and char_in_range(mapa, width, height, Tile.WATER, 2, x, y):
                mapa[y][x] = Tile.SAND

def generate_island(mapa, width, height, center_x, center_y, radius, neighbours, iterations):
    if iterations > 0:
        for y in range(int(center_y - radius), int(center_y + radius)):
            for x in range(int(center_x - radius), int(center_x + radius)):
                if 0 <= y < height and 0 <= x < width:
                    if np.pow(center_x - x, 2) + np.pow(center_y - y, 2) < np.pow(radius, 2) * 0.995:
                        mapa[y][x] = Tile.GRASS

        for i in range(1, int(neighbours)):
            angle = np.random.uniform(0, 2 * np.pi)
            r = radius * np.random.uniform(1 / 2, 6 / 8)
            generate_island(
                mapa,
                width,
                height,
                center_x + 2 * r * np.sin(angle),
                center_y + 2 * r * np.cos(angle),
                r,
                np.random.randint(4, 7),
                iterations - 1)

def char_in_range(mapa, width, height, char, r, x, y) -> bool:
    for yy in range(y - r, y + r + 1):
        for xx in range(x - r, x + r + 1):
            if 0 <= xx < width and 0 <= yy < height and mapa[yy][xx] == char:
                return True

    return False

def draw_map(renderer, mapa, width, height, tile_size):
    for y in range(height):
        for x in range(width):
            tile = mapa[y][x]

            if tile == Tile.WATER:
                renderer.color = sdl2.ext.Color(64, 64, 192)

            if tile == Tile.SAND:
                renderer.color = sdl2.ext.Color(192, 192, 128)

            if tile == Tile.GRASS:
                renderer.color = sdl2.ext.Color(64, 128, 64)

            rect = sdl2.SDL_Rect(tile_size * x, tile_size * y, tile_size, tile_size)
            renderer.fill(rect)
