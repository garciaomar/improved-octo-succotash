import os

def extract_text(filename, img):
    name = filename[:-4]
    outputfile = name + "_out"
    options = "-l spa hocr"
    os.chdir("/textfiles")
    os.system("tesseract " + filepath + outputfile + options)
    return outputfilename

def parse(filepath):
    try:
        hocr = open(filepath, 'r')
    except:
        print("File not found")
        quit()
    xml_tags = ['div', 'p', 'html', 'title', 'meta', 'head', 'body', 'doctype', '?xml']
    ignore_tags = list()
    table = dict()
    for tag in xml_tags:
        ignore_tags.append(tag + '>')
        ignore_tags.append('<' + tag)

    for line in hocr.readlines():
        ignored = False
        for tag in ignore_tags:
            if tag in line:
                ignored = True
                break
        if ignored:
            continue
