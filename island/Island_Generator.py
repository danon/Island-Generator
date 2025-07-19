import os
import sys

os.environ["PYSDL2_DLL_PATH"] = r"..\SDL2-2.32.2-win32-x64"
import sdl2
import sdl2.ext

import numpy as np
import time

WINDOW_SIZE = (600, 480)

tile_size = 8

map_wdt = int(WINDOW_SIZE[0] / tile_size)
map_hgh = int(WINDOW_SIZE[1] / tile_size)

water = '.'
sands = ':'
grass = '#'

def clear_map(width: int, height: int):
    mapa = np.empty((height, width), dtype=str)
    for y in range(0, height):
        for x in range(0, width):
            mapa[y][x] = '.'
    return mapa

def char_in_range(mapa, width, height, char, r, x, y) -> bool:
    for yy in range(y - r, y + r + 1):
        for xx in range(x - r, x + r + 1):
            if 0 <= xx < width and 0 <= yy < height and mapa[yy][xx] == char:
                return True

    return False

def generate_island(mapa, width, height, cx, cy, radius, neighbours, iter):
    if iter > 0:
        for y in range(int(cy - radius), int(cy + radius)):
            for x in range(int(cx - radius), int(cx + radius)):
                if 0 <= y < height and 0 <= x < width:
                    if np.pow(cx - x, 2) + np.pow(cy - y, 2) < np.pow(radius, 2) * 0.995:
                        mapa[y][x] = '#'

        for i in range(1, int(neighbours)):
            angle = np.random.uniform(0, 2 * np.pi)
            r = radius * np.random.uniform(1 / 2, 6 / 8)
            nn = np.random.randint(4, 7)
            cx2 = cx + 2 * r * np.sin(angle)
            cy2 = cy + 2 * r * np.cos(angle)

            generate_island(mapa, width, height, cx2, cy2, r, nn, iter - 1)

def add_sands_to(mapa, width, height):
    for y in range(0, height):
        for x in range(0, width):
            if mapa[y][x] == grass and char_in_range(mapa, width, height, water, 2, x, y):
                mapa[y][x] = sands

def generate_map(width, height):
    mapa = clear_map(width, height)

    if width < height:
        radius = width
    else:
        radius = height

    radius = radius * 1 / 4

    cx = width / 2
    cy = height / 2

    ngbrs = np.random.randint(4, 7)
    iterations = radius / pow(radius / 8, 2)

    generate_island(mapa, width, height, cx, cy, radius, ngbrs, iterations)
    add_sands_to(mapa, width, height)
    return mapa

def draw_map(renderer, mapa, width, height):
    for y in range(height):
        for x in range(width):
            tile = mapa[y][x]

            if tile == water:
                renderer.color = sdl2.ext.Color(64, 64, 192)

            if tile == sands:
                renderer.color = sdl2.ext.Color(192, 192, 128)

            if tile == grass:
                renderer.color = sdl2.ext.Color(64, 128, 64)

            rect = sdl2.SDL_Rect(tile_size * x, tile_size * y, tile_size, tile_size)
            renderer.fill(rect)

def run_application(
        window_color: sdl2.ext.Color,
        width: int,
        height: int,
):
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

        mapa = generate_map(width, height)
        renderer.color = window_color
        renderer.clear()
        draw_map(renderer, mapa, width, height)
        renderer.present()
        time.sleep(1)

def main():
    run_application(
        window_color=sdl2.ext.Color(48, 48, 48),
        width=map_wdt,
        height=map_hgh
    )
