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
        self.bottom_left_y = int(elements[3])

    #Determines if two bounding boxes are in the same row 
    def sameRow(self, bbox):
        top = fabs(self.top_right_y - bbox.top_right_y)
        bottom = fabs(self.bottom_left_y - bbox.bottom_left_y)
        return top < treshold and bottom < treshold
    
    #Determines if two bounding boxes are part of the same word
    def same(self, bbox):
        if self.content is None or other.content is None:
            return False
        before = fabs(bbox.bottom_left_x - self.top_right_x)
        after = fabs(self.top_right_x - bbox.bottom_left_x)
        return after < threshold or before < threshold

    #Merge the words of two bounding boxes
    def merge(self, bbox):
        if self.content[-1].isdigit() and bbox.content[0].isdigit():
            self.word = '%s%s' % (self.word, bbox.word)
        else:
            self.word = '%s %s' % (self.word, other.word)              
        self.xlr = max(self.bottom_left_x, bbox.bottom_left_x)
        self.xul = min(self.top_right_x, bbox.top_right_x)
        self.ylr = max(self.bottom_left_y, bbox.bottom_left_y)
        self.yul = min(self.top_right_y, bbox.top_right_y)