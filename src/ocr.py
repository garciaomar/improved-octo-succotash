#!/usr/bin/env python
# -*- coding: latin-1 -*-

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

#Removes xml tags from the words obtained from the bounding boxes
def remove_tags(word, count):
    if count == 1:
        return word[word.index('>') + 1 : word.index("</")]
    elif count == 2:
        return word[word.find('>', word.index('>') + 1) + 1 : word.index("</")]

def is_CIE_code(text):
    if len(text) > 2:
        if text[0].isalpha() and text[1].isdigit() and text[2].isdigit():
            return True
    return False

def compose_filename(data):
    cies = ""
    for code in data['CIE']:
        cies += code + '_'
    return "%s%s_%s" % (cies, data['week'], data['year'])

def stateTypo(string1, string2):
    cost = 0
    if len(string1) != len(string2):
        return False
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            cost += 1
    return cost <= 2

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
    filename = dict()
    filename['CIE'] = list()
    epiweekFound = True
    states = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", "Chiapas", "Chihuahua", "Distrito Federal", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

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
            for element in elements:
                coords = None
                word = None
                if element.find("ocrx_word") != -1 and element.find("bbox") != -1:
                    word = element[element.index('>') + 1 : -2].strip()
                    if '<' in word:
                        word = remove_tags(word, word.count('</'))
                    if is_CIE_code(word):
                        filename['CIE'].append(word.strip(','))
                    start = element.index('bbox')
                    end = element[start : ].index(';')
                    coords = element[start + 5: start + end]
                    bbox = BoundingBox(word, coords)
                    if word == 'Aguascalientes':
                        top = bbox.word
                    elif word == 'TOTAL':
                        bottom = bbox.word
                    last = None
                    try:
                        last = bboxes[-1]
                    except:
                        pass
                    if last is not None and bbox.sameWord(last):
                        last.merge(bbox)
                        bboxes.pop()
                        bboxes.append(last)
                    else:
                        bboxes.append(bbox)
            if epiweekFound:
                filename['year'] = bboxes[-1].word
                filename['week'] = bboxes[-2].word.strip(',')
                epiweekFound = False

    #Separar por filas
    position = 0
    rows = dict()
    while position < len(bboxes):
        bbox = bboxes[position]
        if bbox not in rows:
            rows[bbox] = [bbox]
        remove = list()
        for other in bboxes:
            if bbox != other:
                if bbox.sameRow(other):
                    rows[bbox].append(other)
                    remove.append(other)
        if len(remove) > 0:
            for merged in remove:
                bboxes.remove(merged)
            position = 0
        else:
            position += 1

    #Fixes misspelled state names
    only_states = dict()
    total = list()
    for key in rows:
        for j in range(len(states)):
            #First word in the dictionary of rows
            word = rows[key][0].word
            statename = states[j]
            if stateTypo(word, statename):
                rows[key][0].word = statename
        #Keep only the rows with states
        correct_state = rows[key][0].word
        if correct_state in states:
            only_states[correct_state] = rows[key]
        if correct_state == "TOTAL":
            total = rows[key]


    #Format to csv
    ouputpath = "salidas/" + compose_filename(filename) + ".csv"
    output_words = open(ouputpath, "w")

    year = int(filename['year'])
    output_words.write("Estado, , , , , Datos, , , \n")
    output_words.write(", , %s, , %s, , %s, , %s\n" % (year, year -1, year, year -1))
    output_words.write(", Semana, Acum-M, Acum-F, Acum, Semana, Acum-M, Acum-F, Acum\n")

    for key in sorted(only_states):
        length = len(only_states[key])
        #State name first
        statename = str(only_states[key].pop(0))
        output_words.write(statename + ", ")
        if length < 9:
            for i in range(9 - length):
                output_words.write("NA, ")
        index = 0
        for elem in only_states[key]:
            word = elem.word
            if word.isdigit():
                output_words.write(word)
            else:
                output_words.write("NA")
            index += 1
            if index < length - 1:
                output_words.write(', ')
        output_words.write('\n')
    i = 0
    length = len(total)
    head = str(total.pop(0))
    output_words.write(head + ", ")
    if length < 9:
        for i in range(9 - length):
            output_words.write("NA, ")
    for elem in total:
        output_words.write(elem.word)
        i += 1
        if i < len(total):
            output_words.write(', ')
    output_words.close()