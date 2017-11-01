import matplotlib.pyplot as plt
import csv
import numpy as np


def calculateValuePieceOfColor(inColor, outColor, numberOfPiece, countAllPieces, value):
    if inColor > outColor:
        return numberOfPiece - countAllPieces * value
    else:
        return countAllPieces * value - numberOfPiece + 1


def interpolateColor(fromColor, toColor, numberOfPiece, countAllPieces, value):
    rFrom, gFrom, bFrom = fromColor
    rTo, gTo, bTo = toColor
    if rFrom != rTo:
        r = calculateValuePieceOfColor(rFrom, rTo, numberOfPiece, countAllPieces, value)
    else:
        r = rFrom
    if gFrom != gTo:
        g = calculateValuePieceOfColor(gFrom, gTo, numberOfPiece, countAllPieces, value)
    else:
        g = gFrom
    if bFrom != bTo:
        b = calculateValuePieceOfColor(bFrom, bTo, numberOfPiece, countAllPieces, value)
    else:
        b = bFrom
    return r, g, b


def gradient_rgb_bgr(v):
    pieces = 2
    colors = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    i = int(np.floor(pieces * v)) % pieces
    r, g, b = interpolateColor(colors[i], colors[i + 1], i + 1, pieces, v)
    return r, g, b


def readDataFromFile(name):
    file = open(name, "r")
    reader = csv.reader(file)
    first = True
    data = []
    maxHeight = 0.0
    for line in reader:
        if not first:
            rowArray = []
            for cell in line:
                rowArray.append(float(cell))
                if maxHeight < float(cell):
                    maxHeight = float(cell)
            data.append(rowArray)
        else:
            first = False
    return data, maxHeight


def convertHeightsToRGBs(heights, maxHeight):
    rgbMatrix = []
    for line in heights:
        row = []
        for cell in line:
            r, g, b = gradient_rgb_bgr(cell / maxHeight)
            row.append([r, g, b])
        rgbMatrix.append(row)
    return rgbMatrix


def main():
    heightMatrix, maxHeight = readDataFromFile("big_dem.csv")
    rgbMatrix = convertHeightsToRGBs(heightMatrix, maxHeight)


if __name__ == '__main__':
    main()
