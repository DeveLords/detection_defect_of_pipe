import csv
import numpy as np


def readTemp(filename):
    fl = list()  
    with open(filename, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=';')
        next(file_reader)
        for raw in file_reader:
            fileName = raw[0][-12:].replace('IS2', 'jpg')
            coldPoint = raw[4].replace(',', '.')
            hotpoint = raw[5].replace(',','.')
            fl.append((fileName, coldPoint, hotpoint))
    return fl

infTemp = readTemp('file/output.csv')
print(infTemp)