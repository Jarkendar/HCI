import matplotlib.pyplot as plt
import csv
import numpy as np


def readDataFromFile(name):
    file = open(name, "r")
    reader = csv.reader(file)
    first = True
    data = []
    for line in reader:
        if not first:
            rowArray = []
            for cell in line:
                rowArray.append(float(cell))
            data.append(rowArray)
        else:
            first = False
    return data


def main():
    heightMatrix = readDataFromFile("big_dem.csv")


if __name__ == '__main__':
    main()
