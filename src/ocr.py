import os

def extract_text(filename, img):
    name = filename[:-4]
    outputfile = name + "_out"
    os.chdir("/textfiles")
    os.system("tesseract " + filepath + outputfile)
    return outputfilename

def parse_txt(filepath):
    txt = open(filepath, 'r')
    table = dict()

    #Remove header of the file
    i = 1
    while(i < 9):
        txt.readLines()
        i++
    #Tag every state
    for line in txt.readLines():
        if line != ""
            table = {line, []}
        if line == "TOTAL"
            break #stop tagging
