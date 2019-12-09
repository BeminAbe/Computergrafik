# import necessary packages
import bpy # blender python interface
import numpy as np

import random
import math






#random.seed(1)



# texture size
sidelength = 3

vertices = {}


for x in range(0, sidelength):
    for y in range(0, sidelength): 
        vertices[x,y] = 1
        

        
        
        
def perform_diamond_step(array, minx, miny, maxx, maxy):
    #if(maxx-minx = 0) return
    array[
        minx+(maxx-minx)/2,
        miny+(maxy-miny)/2
        ] = (array[minx,miny] + array[minx,maxy] + array[maxx,miny] + array[maxx,maxy]) / 4 + random.random()
    return array

def perform_square_step(array, x, y, distance):
    sum = 0
    count = 0
    
    if (x-distance)>=0:
        sum = sum + array[x-distance,y]
        count = count + 1    
    if (x+distance)<math.sqrt(len(array)):
        sum = sum + array[x+distance,y]
        count = count + 1
    
    if (y-distance)>=0:
        sum = sum + array[x,y-distance]
        count = count + 1
    if (y+distance)<math.sqrt(len(array)):
        sum = sum + array[x,y+distance]
        count = count + 1
    
    if count > 0: 
        array[x,y] = sum/count + random.random()
    
    return array

def perform_diamond_square(array, minx, miny, maxx, maxy):
   
    midx = minx+(maxx-minx)/2
    midy = miny+(maxy-miny)/2
    
    
    perform_diamond_step(array, minx, miny, maxx, maxy)
    dist = (maxx - minx) / 2
    
    
    perform_square_step(array, minx, midy, dist)
    perform_square_step(array, maxx, midy, dist)

    perform_square_step(array, midx, miny, dist)
    perform_square_step(array, midx, maxy, dist)
    
    if dist <= 1: return 1
    
    perform_diamond_square(array,minx,miny,midx,midy)
    perform_diamond_square(array,minx,midy,midx,maxy)
    
    perform_diamond_square(array,midx,miny,maxx,midy)
    perform_diamond_square(array,midx,midy,maxx,maxy)    
    
    return array

def clamp_diamond_square(array):
    minval = array[0,0]
    maxval = array[0,0]
    
    for x in range(0, sidelength):
        for y in range(0, sidelength): 
            if array[x,y] > maxval: maxval = array[x,y]
            if array[x,y] < minval: minval = array[x,y]
                
    for x in range(0, sidelength):
        for y in range(0, sidelength): 
            array[x,y] = (array[x,y] - minval ) / (maxval - minval)
    return array


perform_diamond_square(vertices, 0,0,sidelength-1,sidelength-1)

clamp_diamond_square(vertices)


print("-----")

for x in range(0, sidelength):
    for y in range(0, sidelength): 
        print(vertices[x,y])
    print()
print("-----")



