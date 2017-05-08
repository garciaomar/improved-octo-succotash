import os
from src import preprocessing as pre
from src import ocr as ocr

if __name__ == "__main__":
    directory = pre.convertPDF()
    for filename in os.listdir(directory):
        filepath = directory + "/" + filename
        binary_filepath = filepath[:-4] + "_binary.png"
        if os.path.isfile(binary_filepath):
            pass
        else:
            img = pre.erase_lines(filepath)
            hocr_file = ocr.extract_text(filename, directory)
