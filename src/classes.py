from math import fabs

class BoundingBox:

    treshold = 20

    #Initiate the class
    def __init__(self, word, coords):
        self.word = word
        elements = coords.strip()
        self.top_right_x = int(elements[0])
        self.top_right_y = int(elements[1])
        self.bottom_left_x = int(elements[2])
        self.bottom_left-y = int(elements[3])

    #Determines if two bounding boxes are in the same row 
    def sameRow(self, bbox):
        top = fabs(self.top_right_y - bbox.top_right_y)
        bottom = fabs(self.bottom_left_y - bbox.bottom_left_y)
        return top < treshold and bottom < treshold
