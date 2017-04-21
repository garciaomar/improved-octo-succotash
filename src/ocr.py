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
                    content = element[element.index('">') + 2 : -2].strip()
                    if 'bbox' in element:
                        start = element.index('bbox')
                        end = element[start : ].index('"')
                        bbox = element[start + 5: start + end]
                    word = wordbox(bbox, content)
                    if content == 'Aguascalientes':
                        top = word
                    elif content == 'TOTAL':
                        bottom = word
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
