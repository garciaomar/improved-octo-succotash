import os
import sys
import Image
import numpy
from math import fabs

def convertPDF():
    if len(sys.argv) != 4:
        print("Invalid number of arguments.\n> python main.py [source_file] [fromPage] [toPage]")
        quit()
    else:
        path = sys.argv[1]
        #removes the file extension
        filename = path[10:-4]
        #creates a directory to store the output images
        if os.path.isdir("images/" + filename):
            pass
        else:
            os.system("mkdir images/" + filename)
        output = "images/" + filename + "/tabla.png"
        fromPage = sys.argv[2]
        toPage = sys.argv[3]
        #this options enhance the quality of the output images, aswell as cut the borders of the image
        options = " -quality 100 -sharpen 0x1.0 -alpha off -trim "
        os.system("convert -density 200 " + path + "[" + fromPage + "-" + toPage + "]" + options + output)
        #retuns the directory where the output images are stored
        return "images/" + filename

def erase_lines(filename):
    image = Image.open(filename)
    pixels = numpy.array(image)
    #(width, height, chanels) = numpy.shape(pixels)
    elems = list()
    elems = numpy.shape(pixels)
    width = elems[0]
    height = elems[1]

    black = 0
    white = 255
    treshold = 255 / 2
    color = 10
    extreme = 20
    gray = 192
    result = numpy.zeros((width, height), numpy.uint8)
    blacks = list()

    for column in xrange(width):
        for row in xrange(height):
            pixel = pixels[column, row]
            r = int(pixel[0])
            g = int(pixel[1])
            b = int(pixel[2])
    	    rgb_sum = r + g + b
            mean = rgb_sum / 3
            absolutes = [int(fabs(r - g)), int(fabs(r - b)), int(fabs(g - b))]
            #neither white or a shade of gray
            if max(absolutes) > color:
               #turns color pixels to white
    	       result[column, row] = white
               continue
            #turns dark pixels to pure black
            if rgb_sum < extreme:
    		    result[column, row] = black
    		    blacks.append((column, row))
    		    continue
            if mean < treshold:
    		    result[column, row] = black
    		    blacks.append((column, row))
    		    continue
            #if it is a brighter pixel
            #searching for the characters that are in white pixels instead of black
            if mean > 255 - extreme:
                acum = 0
                #right, bottom, left and top neighbor of the current pixel
                neighborhood = [(column + 1, row), (column, row + 1), (column - 1, row), (column, row - 1)]
                #check the current pixel neighborhood
                for neighbor in neighborhood:
                    try:
                        pixel2 = pixels[neighbor[0], neighbor[1]]
                    except IndexError:
                        continue
                    r2 = int(pixel2[0])
                    g2 = int(pixel2[1])
                    b2 = int(pixel2[2])
            	    rgb_sum2 = r2 + g2 + b2
                    mean2 = rgb_sum2 / 3
                    #difference between the current pixel and each of its neighbors
                    acum += fabs(mean - mean2)
                #if there is a considerable difference, then this pixel is considered to be part of a white character
                if acum > 1 and acum < 250:
    		        result[column, row] = black
    		        blacks.append((column, row))
                #no difference, then is a pixel of the background and stays white
                else:
                    result[column, row] = white

    #minimum pixels to be considered a verical line

    line = 30
    remaining = list()
    while len(blacks) > 0:
        pixel = blacks.pop(0)
        (column, row) = pixel
        if result[column, row] == black:
            ccount = 1
            pos = column
            while pos < width and result[pos, row] == black:
                pos += 1
                ccount += 1
            #erase vertical lines
            if ccount > line:
                for d in xrange(ccount):
            		if column + d < width:
                            	result[column + d, row] = white
            #not considered as a vertical line
            else:
                remaining.append(pixel)

    #minimum pixels to be considered a horizontal line
    line = 60
    for pixel in remaining:
        (column, row) = pixel
        if result[column, row] == black:
            rcount = 1
            pos = row
            while pos < height and result[column, pos] == black:
                pos += 1
                rcount += 1
            #erase horizontal lines
            if rcount > line:
                for d in xrange(rcount):
                    result[column, row + d] = white

    name = filename[:-4]
    data = Image.fromarray(result)
    outputname = name + "_binary.png"
    data.save(outputname)
    print("Saved binary image")
    return outputname

def dfs(pixels, column, row):
    cont = true
    while(cont):
        (width, height, chanels) = numpy.shape(pixels)
        pixel = pixels[column, row]
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        rgb_sum = r + g + b
        mean = rgb_sum / 3
        neighborhood = [(column + 1, row), (column, row + 1), (column - 1, row), (column, row - 1)]
        for neighbor in neighborhood:
            try:
                pixel2 = pixels[neighbor[0], neighbor[1]]
            except IndexError:
                continue
            r2 = int(pixel2[0])
            g2 = int(pixel2[1])
            b2 = int(pixel2[2])
            rgb2_sum = r2 + g2 + b2
            mean2 = rgb2_sum / 3
            if mean - mean2 == 0:
                column = neighbor[0]
                row = neighbor[1]
                cont = True
                break
            else:
                cont = False
                continue
