#!/usr/bin/env python3

"""
A python implimentation of the wave function collapse algorithm
"""
from collections import namedtuple

def run(x: int, y: int, pixel_size: tuple, tiles: dict=None):
	"""
	The main function for running the algorithm
	x           : The amount of tiles in the x direction
	y           : The amount of tiles in the y direction
	pixel_size  : tuple for the amount of pixels
	tiles       : dict of the tiles
	"""

	from random import shuffle

	assert tiles # Makes sure that tiles have been passed
	board = [ [None for j in range(x)] for i in range(y) ] # This is where all the values are held
	filled_set = set() # A Set with the (x, y) coordinates of every tile that exists

	def find_possible_neighbors(j, i) -> set:
		"""
		Function for returning squares near i & j
		in appropriate range
		j : x value
		i : y value
		"""
		outset = {
			(j, i - 1),
			(j + 1, i),
			(j, i + 1),
			(j - 1, i)
		}
		return { entry for entry in outset if (0 <= entry[0] < x) and (0 <= entry[1] < y) } # returns entries in range

	def find_entropy(j, i):
		"""
		function for finding the entropy of a potential tile

		returns tuple: (int: amount_of_entries, tuple: (x, y), set: set_of_tiles)
		"""

		# tile to top
		if (j, i - 1) in filled_set:
			ref = board[i - 1][j]
			if ref is not None:
				ref = ref.bottom[::-1]
				localset = set()
				for tile in tiles:
					if tiles[tile].top == ref: localset.add(tile)
		else:
			localset = set()
			for tile in tiles:
				localset.add(tile)
		outset = localset

		# tile to right
		if (j + 1, i) in filled_set:
			ref = board[i][j + 1]
			if ref is not None:
				ref = ref.left[::-1]
				localset = set()
				for tile in tiles:
					if tiles[tile].right == ref: localset.add(tile)
		else:
			localset = set()
			for tile in tiles:
				localset.add(tile)
		outset &= localset

		# tile to bottom
		if (j, i + 1) in filled_set:
			ref = board[i + 1][j]
			if ref is not None:
				ref = ref.top[::-1]
				localset = set()
				for tile in tiles:
					if tiles[tile].bottom == ref: localset.add(tile)
		else:
			localset = set()
			for tile in tiles:
				localset.add(tile)
		outset &= localset

		# tile to left
		if (j - 1, i) in filled_set:
			ref = board[i][j - 1]
			if ref is not None:
				ref = ref.right[::-1]
				localset = set()
				for tile in tiles:
					if tiles[tile].left == ref: localset.add(tile)
		else:
			localset = set()
			for tile in tiles:
				localset.add(tile)
		outset &= localset

		return (len(outset), (j, i), outset)

	def draw_image(filename: str = "image"):
		"""
		Function for drawing the generated data to file
		"""
		from PIL import Image

		data = []

		for i in board:
			for j in range(len(board[0][0].image)):
				data.append([])
				for k in i:
					data[-1] = [*data[-1], *[l for l in k.image[j]]]

		im = Image.new("RGBA", pixel_size, (255, 255, 255, 255))
		data = [ [ data[int(len(data) * (i / pixel_size[1]))][int(len(data[1]) * (j / pixel_size[0]))] for j in range(pixel_size[0])] for i in range(pixel_size[1]) ]
		data2 = []
		for i in data:
			for j in i:
				data2.append(j)
		im.putdata(data2)
		im.save(f"{filename}.png")

	while x * y > len(filled_set):
		to_go_through = set() # A set of squares to go to
		for tile in filled_set: # Adds potential neighbors for each filled_set
			to_go_through |= find_possible_neighbors(*tile)
		to_go_through -= filled_set # Removes filled tiles from potential squares
		if len(to_go_through) == 0: to_go_through = {(0, 0)} # If it doesn't want to go through tiles, just go to the top left

		entropies = [ find_entropy(*tile) for tile in to_go_through ] # Gets entropies for each square to go through
		entropies.sort() # sorts by smallest entropy (least possibilities)
		entropies = [ tile for tile in entropies if tile[0] == entropies[0][0] ] # gets all the tiles with equivalent entropy values
		shuffle(entropies) # shuffles values
		entropies = entropies[0] # picks a random value
		xy = entropies[1] # sets xy coordinate of chosen entropy (set in `find_entropy()` function)
		entropies = list(entropies[2]) # sets the possible tiles that could go at that entropy value
		if len(entropies) == 0: return False # Returns if no possible square is found
		shuffle(entropies) # shuffles the tiles that could go to xy
		board[xy[1]][xy[0]] = tiles[entropies[0]] # Sets the board at the xy value to be a chosen tile
		filled_set.add(xy) # adds the added tile to the `filled_set` set

	draw_image() # Saves the generated image
	return True

def rotate_tile(tile, n: int, depth: int = 0):
	"""
	Function for rotating a tile
	tile  : the data from the tile that is being rotated
	n     : the amount of 90 deg clockwise rotations being done
	depth : the amount of recursions done
	"""

	if depth >= n:
		return tile

	(x, y) = (len(tile.image[0]), len(tile.image))

	adjs_args = [ tile[(i - 1) % 4] for i in range(4) ] # Gets a list of rotated edges

	color_data = zip(*tile.image) # Transposes List
	color_data = [ list(i[::-1]) for i in color_data ] # flips the data over the y axis

	return rotate_tile(tile = adjs(*adjs_args, color_data), n = n, depth = depth + 1)

def get_tiles(tiles_path: str = "tiles/circuit"):
	"""
	Function that just returns the dictionary of tiles
	"""

	import os
	from glob import glob
	from PIL import Image

	basedir = os.path.abspath(".")
	os.chdir(tiles_path)

	tiles = {}

	old_file_lookup_table = {
		"0.png": (0, 0, 0, 0),
		"1.png": (1, 1, 1, 1),
		"2.png": (1, 2, 1, 1),
		"3.png": (1, 3, 1, 3),
		"4.png": (4, 2, 5, 0),
		"5.png": (5, 1, 1, 4),
		"6.png": (1, 2, 1, 2),
		"7.png": (3, 2, 3, 2),
		"8.png": (3, 1, 2, 1),
		"9.png": (2, 2, 1, 2),
		"10.png": (2, 2, 2, 2),
		"11.png": (2, 2, 1, 1),
		"12.png": (1, 2, 1, 2)
	}

	file_lookup_table = {
		"0.png": ("AAA", "AAA", "AAA", "AAA"),
		"1.png": ("BBB", "BBB", "BBB", "BBB"),
		"2.png": ("BBB", "BCB", "BBB", "BBB"),
		"3.png": ("BBB", "BDB", "BBB", "BDB"),
		"4.png": ("ABB", "BCB", "BBA", "AAA"),
		"5.png": ("ABB", "BBB", "BBB", "BBA"),
		"6.png": ("BBB", "BCB", "BBB", "BCB"),
		"7.png": ("BDB", "BCB", "BDB", "BCB"),
		"8.png": ("BDB", "BBB", "BCB", "BBB"),
		"9.png": ("BCB", "BCB", "BBB", "BCB"),
		"10.png": ("BCB", "BCB", "BCB", "BCB"),
		"11.png": ("BCB", "BCB", "BBB", "BBB"),
		"12.png": ("BBB", "BCB", "BBB", "BCB")
	}

	for filename in glob("*"):

		im = Image.open(filename).getdata()
		temp_image = []

		# Assumes tiles are squares and are all the same size
		im_size = len(im)
		im_size = (int(im_size ** .5), int(im_size ** .5))

		for y in range(im_size[1]):
			temp_image.append([])
			for x in range(im_size[0]):
				try:
					temp_image[-1].append(im[x + y * im_size[1]])
				except:
					print(len(im), x, y, im_size[1])

		if filename in file_lookup_table: sides = file_lookup_table[filename]
		else: sides = (0, 0, 0, 0)
		tiles[filename] = adjs(*sides, temp_image)

	os.chdir(basedir)

	return tiles

def get_all_rotations(tiles):

	"""
	Function for getting all possible rotations of each tile
	by the edge of the image
	"""

	tile_keys = [i for i in tiles]

	# Initialises the Tiles by getting all the rotations
	for i in tile_keys: # Doesn't use just tiles here because dict can't change size while being itterated on
		# Goes through each tile that exists
		if i not in {"0.png", "1.png"}:
			for j in range(1, 4):
				# Goes through all 3 rotations (a rotation of 0 and 4 is the same so it needs to check 3 more)
				new_tile = rotate_tile(tiles[i], j) # Gets a new potential tile to add
				tiles[f"{i}##{j}"] = new_tile

	return tiles

def get_all_adjacencies(tiles):
	"""
	Function that sets all the adjacencies of all the tiles in the `tiles` dict based on image data

	This may be a good function to revisit with the principal of having the values listed clockwise and requiring a reasonable lettering scheme
	"""
	new_tiles = {}

	for tile in tiles:
		sides = []
		sides.append(tiles[tile].image[0]) # top
		sides.append( [tiles[tile].image[i][-1] for i in range(len(tiles[tile].image))] ) # right
		sides.append(tiles[tile].image[-1]) # bottom
		sides.append( [tiles[tile].image[i][0] for i in range(len(tiles[tile].image))] ) # left
		sides = [ str(i) for i in sides ]
		new_tiles[tile] = adjs(*sides, tiles[tile].image)
	return new_tiles

def forever_for():
	"""
	Fancy function that works in a for loop that will go forever
	"""
	i = 0
	while True:
		yield i
		i += 1

# Setting up Tiles

adjs = namedtuple("Adjacencies", "top right bottom left image")

tiles = get_tiles()
tiles = get_all_rotations(tiles)
# tiles = get_all_adjacencies(tiles)

xy = 16                 # The amount of tiles in the x and y directions
image_dimensions = 1024 # The dimensions of the image generated

for i in forever_for():
	if run(x = xy, y = xy, pixel_size = (1024, 1024), tiles=tiles): break
	print(f" - No Solution in Attempt #{i}"); i+=1

input("\n ~ FINISHED")
