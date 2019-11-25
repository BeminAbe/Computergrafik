import mathutils
import bpy

# main entry point
if __name__ == "__main__":

    xRange = 1000
    yRange = 1000
    image = bpy.data.images.new("MyImage", width=xRange, height=yRange)
    pixelVec = {}

    max = 0.0
    min = 10.0
    
    scaling = 0.002


    pixels = [None] * xRange * yRange
    for x in range(xRange):
        for y in range(yRange):
            pixelVec[x, y] = mathutils.noise.hetero_terrain([x*scaling, y*scaling, 0], 1.0, 1.0, 1, 0, noise_basis='PERLIN_ORIGINAL')
            if pixelVec[x, y] > max:
                max = pixelVec[x, y]
            if pixelVec[x, y] < min:
                min = pixelVec[x, y]

    for x in range(xRange):
        for y in range(yRange):
            # assign RGBA to something useful
            r = pixelVec[x,y] -min / (max - min)
            g = pixelVec[x,y] -min / (max - min)
            b = pixelVec[x,y] -min / (max - min)
            a = 1.0
            
            
            print(r)
            pixels[(y * xRange) + x] = [r, g, b, a]

            
            
    # flatten list
    pixels = [chan for px in pixels for chan in px]

    # assign pixels
    image.pixels = pixels

    # write image
    image.filepath_raw = "//textures/moisturemap.png"
    image.file_format = 'PNG'
    image.save()



