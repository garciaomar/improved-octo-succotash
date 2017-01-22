import os
from src import preprocessing as pre

if __name__ == "__main__":
    directory = pre.convertPDF()
    for filename in os.listdir(directory):
        filepath = directory + "/" + filename
        pre.erase_lines(filepath)
