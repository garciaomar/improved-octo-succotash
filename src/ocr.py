import os

def extract_text(filename, img):
    name = filename[:-4]
    outputfile = name + "_out"
    os.chdir("/textfiles")
    os.system("tesseract " + filepath + outputfile)
