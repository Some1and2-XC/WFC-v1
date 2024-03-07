#!/usr/bin/env python3

from WFC import run

def forever_for():
	"""
	Fancy function that works in a for loop that will go forever
	"""
	i = 0
	while True:
		yield i
		i += 1

xy = 64                 # The amount of tiles in the x and y directions
image_dimensions = 2048 # The dimensions of the image generated

for i in forever_for():
	if run(x = xy, y = xy, pixel_size = (image_dimensions, image_dimensions)): break
	print(f" - No Solution in Attempt #{i}", end="\r"); i+=1

input("\n ~ FINISHED")
