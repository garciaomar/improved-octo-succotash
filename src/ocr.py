import os
from classes import BoundingBox

def extract_text(filename, filepath):
    name = filename[:-4]
    outputfile = "xmlfiles/" + name + "_out"
    options = " -l spa hocr"
    filepath += "/" + name + "_binary.png "
    os.system("tesseract " + filepath + outputfile + options)
    outputfile += ".hocr"
    return outputfile

def parse(filepath):
    try:
        hocr = open(filepath, 'r')
    except:
        print("File not found")
        quit()
    xml_tags = ['div', 'p', 'html', 'title', 'meta', 'head', 'body', 'doctype', '?xml']
    ignore_tags = list()
    table = dict()
    top = None
    bottom = None
    lines = list()
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
        if 'span' in line:
            elements = line.split('span')
            words = list()
            for element in elements:
                if 'ocrx_word' in element:
                    word = element[element.index('">') + 2 : -2].strip()
                    if 'bbox' in element:
                        start = element.index('bbox')
                        end = element[start : ].index('"')
                        coords = element[start + 5: start + end]
                    bbox = BoundingBox(coords, word)
                    if content == 'Aguascalientes':
                        top = bbox.word
                    elif content == 'TOTAL':
                        bottom = bbox.word
                    last = None
                    try:
                        last = words[-1]
                    except:
                        pass
                    if last is not None and word.same(last):
                        last.merge(word)
                    else:
                        words.append(word)
            if len(words) > 0:
                lines.append(words)
    hocr.close()
    kept = list()
    for line in lines:
        kept += line
    position = 0
    rows = dict()
    while position < len(kept):
        word = kept[position]
        if word not in rows:
            rows[word] = [word]
        remove = list()
        for other in kept:
            if word != other:
                if word.same(other):
                    word.merge(other)
                    remove.append(other)
                elif word.row(other):
                    rows[word].append(other)
                    remove.append(other)
        if len(remove) > 0:
            for absorbed in remove:
                kept.remove(absorbed)
            position = 0
        else:
            position += 1

    #Writing output file
    output_words = open("prueba.txt", "w")
    for word in kept:
        output_words.write(word)
    output_words.close()
