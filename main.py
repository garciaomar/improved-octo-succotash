import os
from src import preprocessing as pre
from src import ocr as ocr

if __name__ == "__main__":
    directory = pre.convertPDF()
    for filename in os.listdir(directory):
        filepath = directory + "/" + filename
        img = pre.erase_lines(filepath)
        ocr.extract_text(filename, img)
