from math import fabs

class BoundingBox:

    treshold = 20
    same_word_treshold = 10
    
    #Initiate the class
    def __init__(self, word, coords):
        self.word = word
        elements = coords.split(' ')
        self.top_right_x = int(elements[0])
        self.top_right_y = int(elements[1])
        self.bottom_left_x = int(elements[2])
        self.bottom_left_y = int(elements[3])
    
    #Return as a string
    def __str__(self):
        return '%s' % self.word

    #Determines if two bounding boxes are in the same row 
    def sameRow(self, bbox):
        global treshold
        top = fabs(self.top_right_y - bbox.top_right_y)
        bottom = fabs(self.bottom_left_y - bbox.bottom_left_y)
        return top < treshold and bottom < treshold

    #Determines if two bounding boxes are part of the same word
    def sameWord(self, bbox):
        global same_word_treshold
        if self.word is None or bbox.word is None:
            return False
        before = fabs(bbox.bottom_left_x - self.top_right_x)
        after = fabs(self.top_right_x - bbox.bottom_left_x)
        return (after < same_word_treshold or before < same_word_treshold) and self.sameRow(bbox)

    #Merge the words of two bounding boxes
    def merge(self, bbox):
        if self.word[-1].isdigit() and bbox.word[0].isdigit():
            self.word = '%s%s' % (self.word, bbox.word)
        else:
            self.word = '%s %s' % (self.word, bbox.word)              
        self.bottom_left_x = max(self.bottom_left_x, bbox.bottom_left_x)
        self.top_right_x = min(self.top_right_x, bbox.top_right_x)
        self.bottom_left_y = max(self.bottom_left_y, bbox.bottom_left_y)
        self.top_right_y = min(self.top_right_y, bbox.top_right_y)