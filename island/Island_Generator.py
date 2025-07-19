import os
import sys

os.environ["PYSDL2_DLL_PATH"] = r"..\SDL2-2.32.2-win32-x64"
import sdl2
import sdl2.ext

import numpy as np
import time

WINDOW_COLOR = sdl2.ext.Color(48, 48, 48)
WINDOW_SIZE = (600, 480)

tile_size = 8

map_wdt = int(WINDOW_SIZE[0] / tile_size)
map_hgh = int(WINDOW_SIZE[1] / tile_size)
mapa = np.empty((map_hgh, map_wdt), dtype=str)

water = '.'
sands = ':'
grass = '#'

def clear_map():
    for y in range(0, map_hgh):
        for x in range(0, map_wdt):
            mapa[y][x] = '.'
    return

def char_in_range(char, r, x, y):
    for yy in range(y - r, y + r + 1):
        for xx in range(x - r, x + r + 1):
            if 0 <= xx < map_wdt and 0 <= yy < map_hgh and mapa[yy][xx] == char:
                return True

    return False

def generate_island(cx, cy, radius, neighbours, iter):
    if iter > 0:
        for y in range(int(cy - radius), int(cy + radius)):
            for x in range(int(cx - radius), int(cx + radius)):
                if 0 <= y < map_hgh and 0 <= x < map_wdt:
                    if np.pow(cx - x, 2) + np.pow(cy - y, 2) < np.pow(radius, 2) * 0.995:
                        mapa[y][x] = '#'

        for i in range(1, int(neighbours)):
            angle = np.random.uniform(0, 2 * np.pi)
            r = radius * np.random.uniform(1 / 2, 6 / 8)
            nn = np.random.randint(4, 7)
            cx2 = cx + 2 * r * np.sin(angle)
            cy2 = cy + 2 * r * np.cos(angle)

            generate_island(cx2, cy2, r, nn, iter - 1)

def add_sands():
    for y in range(0, map_hgh):
        for x in range(0, map_wdt):
            if mapa[y][x] == grass and char_in_range(water, 2, x, y):
                mapa[y][x] = sands

def generate_map():
    clear_map()

    if map_wdt < map_hgh:
        radius = map_wdt
    else:
        radius = map_hgh

    radius = radius * 1 / 4

    cx = map_wdt / 2
    cy = map_hgh / 2

    ngbrs = np.random.randint(4, 7)
    iterations = radius / pow(radius / 8, 2)

    generate_island(cx, cy, radius, ngbrs, iterations)
    add_sands()

def draw_map(renderer):
    for y in range(map_hgh):
        for x in range(map_wdt):
            tile = mapa[y][x]

            if tile == water:
                renderer.color = sdl2.ext.Color(64, 64, 192)

            if tile == sands:
                renderer.color = sdl2.ext.Color(192, 192, 128)

            if tile == grass:
                renderer.color = sdl2.ext.Color(64, 128, 64)

            rect = sdl2.SDL_Rect(tile_size * x, tile_size * y, tile_size, tile_size)
            renderer.fill(rect)

def run_application(window_color: sdl2.ext.Color):
    sdl2.ext.init()
    window = sdl2.ext.Window("Island Generator", WINDOW_SIZE)
    window.show()

    renderer = sdl2.ext.Renderer(window)

    while True:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                sdl2.ext.quit()
                sys.exit(0)

        generate_map()
        renderer.color = window_color
        renderer.clear()
        draw_map(renderer)
        renderer.present()
        time.sleep(1)

def main():
    run_application(
        WINDOW_COLOR
    )
