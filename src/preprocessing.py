import os
import sys

def convertPDF():
    if len(sys.argv) != 4:
        print("Numero de argumentos invalido.\n> python main.py [pdf_fuente] [desdePagina] [hastaPagina]")
    else:
        path = sys.argv[1]
        filename = path[10:-4]
        os.system("mkdir images/" + filename)
        output = "images/" + filename + "/tabla.png"
        fromPage = sys.argv[2]
        toPage = sys.argv[3]
        os.system("convert " + path + "[" + fromPage + "-" + toPage + "] " + "-alpha off " + output)
        