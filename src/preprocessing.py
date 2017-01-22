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
    (width, height, chanels) = numpy.shape(pixels)

    black = 0
    white = 255
    treshold = 255 / 2
    color = 10
    extreme = 20
    gray = 192
    result = numpy.zeros((width,height), numpy.uint8)
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
            #shade of gray
        	#if max(absolutes) == 0:
    		#    if r > 0.9 * gray and r < 1.1 * gray: # intermediate
        	#    	result[column, row] = white
        	#    	continue
            #turns dark pixels to pure black
            if rgb_sum < extreme:
    		    result[column, row] = black
    		    blacks.append((column, row))
    		    continue
            if mean < treshold:
    		    result[column, row] = black
    		    blacks.append((column, row))
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
    data.save(name + "_binary.png")
