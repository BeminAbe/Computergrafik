# import library
import mathutils
import bpy
import random


# define resolution
xRange = 1000
yRange = 1000

image = bpy.data.images.new("MyImage", width=xRange, height=yRange)
pixelVec = {}

# limits for normalization
max = 0.0
min = 10.0


scaling = 0.002
offset = random.random()*xRange

# iterate through all pixels
pixels = [None] * xRange * yRange
for x in range(xRange):
    for y in range(yRange):
        # perlin noise
        pixelVec[x, y] = mathutils.noise.hetero_terrain([(x+offset)*scaling, (y+offset)*scaling, 0], 1.0, 1.0, 1, 0, noise_basis='PERLIN_ORIGINAL')
        # check if value is greater than max or lesser than min
        if pixelVec[x, y] > max:
            max = pixelVec[x, y]
        if pixelVec[x, y] < min:
            min = pixelVec[x, y]

# normalize vector
for x in range(xRange):
    for y in range(yRange):

        pixel = pixelVec[x,y] -min / (max - min)
        r = pixel
        g = pixel
        b = pixel
        a = 1.0

        #set rgba's of each pixel of pixels
        pixels[(y * xRange) + x] = [r, g, b, a]



# flatten list
pixels = [chan for px in pixels for chan in px]

# assign pixels
image.pixels = pixels

# write image
image.filepath_raw = "//textures/moisturemap.png"
image.file_format = 'PNG'
image.save()
