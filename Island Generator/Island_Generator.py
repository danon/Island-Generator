
# Island Generator
# created by tBane

import numpy as np
import time

def clear_map(mapa):
	for y in range(0,map_hgh):
		for x in range(0,map_wdt):
			mapa[y][x] = '.'
	return

def charInRange(mapa, char, r, x, y):
	for yy in range(y-r, y+r+1):
		for xx in range(x-r, x+r+1):
			if xx>=0 and yy>=0 and xx<map_wdt and yy<map_hgh and mapa[yy][xx] == char:
				return True
	
	return False

def generate_island(mapa, cx, cy, radius, neighbours, iter):
	if iter > 0:
			for y in range(int(cy-radius),int(cy+radius)):
				for x in range(int(cx-radius),int(cx+radius)):
					if y>= 0 and x>=0 and y<map_hgh and x<map_wdt:
						if (np.pow(cx-x,2)+np.pow(cy-y,2) < np.pow(radius,2)*0.995):
							mapa[y][x]='#'
						
			for i in range(1, neighbours):
				
				angle = np.random.uniform(0, 2*np.pi)
				r = radius*np.random.uniform(1/2, 6/8)
				cx2 = cx + 2*r*np.sin(angle)
				cy2 = cy + 2*r*np.cos(angle)
				
				generate_island(mapa, cx2, cy2, r, neighbours, iter-1)
	return

def add_sands(mapa):
	for y in range(0,map_hgh):
		for x in range(0,map_wdt):	
			if mapa[y][x]== '#' and charInRange(mapa, '.', 2, x, y):
				mapa[y][x] = ':'
			
	return

def generate_map():
	if map_wdt < map_hgh:
		radius = map_wdt
	else:
		radius = map_hgh
		
	radius = radius*1/4
	
	cx = map_wdt/2
	cy = map_hgh/2
	
	ngbrs = np.random.randint(4, 8)
	
	generate_island(mapa, cx, cy, radius, ngbrs, 2)
	add_sands(mapa)
	return

##############################

map_wdt = 48
map_hgh =24
mapa = np.empty((map_hgh, map_wdt), dtype=str)

##############################

while True:
	clear_map(mapa)
	generate_map()
	
	for y in range(0,map_hgh):
		for x in range(0,map_wdt):		
			print(mapa[y][x], end='')
		print('')
	
	print("\n\n\n")
	time.sleep(1)