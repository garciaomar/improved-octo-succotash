import os
from classes import BoundingBox

#Removes xml tags from the words obtained from the bounding boxes
def removeTags(word, count):
    if count == 1:
        return word[word.index('>') + 1 : word.index("</")]
    elif count == 2:
        return word[word.find('>', word.index('>') + 1) + 1 : word.index("</")]
    else:
        return word

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
    bboxes = list()
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
            print(elements)
            for element in elements:
                coords = None
                word = None
                if element.find("ocrx_word") != -1 and element.find("bbox") != -1:
                    word = element[element.index('>') + 1 : -2].strip()
                    if '<' in word:
                        word = removeTags(word, word.count('</'))
                    start = element.index('bbox')
                    end = element[start : ].index(';')
                    coords = element[start + 5: start + end]
                    bbox = BoundingBox(word, coords)
                    if word == 'Aguascalientes':
                        top = bbox.word
                    elif word == 'TOTAL':
                        bottom = bbox.word
                    bboxes.append(bbox)
    if len(bboxes) > 0:
        lines.append(bboxes)

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
