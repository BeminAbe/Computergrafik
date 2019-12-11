# import necessary packages
import bpy # blender python interface
import numpy as np
import random
import math
import bpy






############## texture size
pixelwidth = 512

# derived parameters for diamondsquare algorithm
nth = math.ceil(math. log(pixelwidth,2))
sidelength = 2**nth+1

# variable to store diamond square algoritm values
vertices = {}

# reduction factor for the diamond square algorithm
factor = 0.85

# iteration variable for the strenth of the random portion in the diamond square algorithm
strength = 1





###################### Functions


def custom_rand():
    rndval = (random.random()-0.5)*2
    return rndval


## clamp values of array between 0 and 1
def clamp_diamond_square(array):
    minval = array[0,0]
    maxval = array[0,0]
    
    for x in range(0, pixelwidth):
        for y in range(0, pixelwidth): 
            if array[x,y] > maxval: maxval = array[x,y]
            if array[x,y] < minval: minval = array[x,y]
                            
    if (maxval - minval) > 0:
        for x in range(0, sidelength):
            for y in range(0, sidelength): 
                array[x,y] = (array[x,y] - minval ) / (maxval - minval)
                
    return array


## function for reducing the strength of the random part added in the diamond square algorithm
def lower_strength(strength, factor):
    return strength*factor


## function to print out the diamond square array to console (only for development purposes)
def printvertex():
    print("-----")
    for y in range(0, sidelength): 
        linetext = ""
        for x in range(0, sidelength):
            linetext = linetext + str(vertices[x,y]) + "   "
        print(linetext)
    print("-----")





# initialize array with zeros
for x in range(0, sidelength):
    for y in range(0, sidelength): 
        vertices[x,y] = 0

# preload corners with random values
vertices[0,0] = custom_rand();
vertices[sidelength-1,0] = custom_rand();
vertices[0,sidelength-1] = custom_rand();
vertices[sidelength-1,sidelength-1] = custom_rand();
        









## run the diamond square algorithm
for index in range(1,nth+1):
    
    
    # the diamond step
    s = 2**(nth-index)
    
    for x in range(s,sidelength,s*2):
        for y in range(s,sidelength,s*2):
            vertices[x,y] = index
            
            vertices[x,y] = (
                vertices[x+s,y+s] + 
                vertices[x-s,y-s] + 
                vertices[x-s,y+s] + 
                vertices[x+s,y-s]
                )/4+custom_rand()*strength
            #vertices[x,y] = index*2-1
    
             
            
    
    strength = lower_strength(strength, factor)
    
    # the square step
    s = 2**(nth-index)
    for y in range(0,sidelength,s):
        ind = int(y / s)
        xs = 0
        if(ind%2==0):
            xs = s
        for x in range(xs,sidelength,s*2):
            count = 0
            sum = 0
            
            if(x-s>0):
                sum = sum + vertices[x-s,y]
                count = count + 1
                
            if(x+s<sidelength):
                sum = sum + vertices[x+s,y]
                count = count + 1
                
            if(y-s>0):
                sum = sum + vertices[x,y-s]
                count = count + 1
                
            if(y+s<sidelength):
                sum = sum + vertices[x,y+s]
                count = count + 1
            
            if(count>0):
                vertices[x,y] = sum/count + custom_rand()*strength
                
            #vertices[x,y] = index*2
                
    strength = lower_strength(strength, factor)

    
         
    


    
    
    


clamp_diamond_square(vertices)


#printvertex()




##save array as png file and cut off oversized area of said array (1025² may be calculated but 1000² will be stored)

size = pixelwidth, pixelwidth

# blank image
image = bpy.data.images.new("MyImage", width=size[0], height=size[1])

## For white image
# pixels = [1.0] * (4 * size[0] * size[1])

pixels = [None] * size[0] * size[1]
for x in range(size[0]):
    for y in range(size[1]):
        colval = vertices[x,y]
        pixels[(y * size[0]) + x] = [colval, colval, colval, 1]

# flatten list
pixels = [chan for px in pixels for chan in px]

# assign pixels
image.pixels = pixels

# write image
image.filepath_raw = bpy.path.abspath("//textures/heightmap.png")
image.file_format = 'PNG'
image.save()