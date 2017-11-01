import csv
import numpy as np
from PIL import Image
import colorsys as cs


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


def gradient_rgb_bgr(v, light=1):
    pieces = 2
    colors = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    i = int(np.floor(pieces * v)) % pieces
    r, g, b = interpolateColor(colors[i], colors[i + 1], i + 1, pieces, v)

    hue, saturation, lightness = cs.rgb_to_hsv(r, g, b)
    lightness = light / 4 + 0.75

    return cs.hsv_to_rgb(hue, saturation, lightness)


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


def convertHeightToRGBsWithShadow(heights, maxHeight, cosinuses):
    rgbMatrix = []
    for y in range(0, 500):
        row = []
        for x in range(0, 500):
            r, g, b = gradient_rgb_bgr(heights[y][x] / maxHeight, cosinuses[x][y])
            row.append([r, g, b])
        rgbMatrix.append(row)
    return rgbMatrix


def calculateCosinusesAlpha(heightMatrix, s):
    cosinuses = []
    for y in range(0, 499):
        rowCoses = []
        for x in range(0, 499):
            v = [0, 1, heightMatrix[x][y] - heightMatrix[x][y + 1]]
            h = [1, 0, heightMatrix[x][y] - heightMatrix[x + 1][y]]
            p = [v[1] * h[2] - v[2] * h[1], v[2] * h[0] - v[0] * h[2], v[0] * h[1] - v[1] * h[0]]
            cos = (p[0] * s[0] + p[1] * s[1] + p[2] * s[2]) / (
                np.sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2]) * np.sqrt(s[0] * s[0] + s[1] * s[1] + s[2] * s[2]))
            rowCoses.append(abs(cos))
        rowCoses.append(1)
        cosinuses.append(rowCoses)
    row = []
    for i in range(0, 500):
        row.append(1)
    cosinuses.append(row)
    return cosinuses


def createMap(rgbMatrix, name):
    image = Image.new("RGB", (len(rgbMatrix), len(rgbMatrix[0])), "white")  # create image
    pixels = image.load()
    for row in range(image.size[0]):
        for column in range(image.size[1]):
            pixels[row, column] = (int(rgbMatrix[column][row][0] * 255)
                                   , int(rgbMatrix[column][row][1] * 255)
                                   , int(rgbMatrix[column][row][2] * 255))
    image.save(name)


def main():
    heightMatrix, maxHeight = readDataFromFile("big_dem.csv")
    rgbMatrix = convertHeightsToRGBs(heightMatrix, maxHeight)

    sun = [0, 0, 100]
    coses = calculateCosinusesAlpha(heightMatrix, sun)

    rgbMatrixShadow = convertHeightToRGBsWithShadow(heightMatrix, maxHeight, coses)

    createMap(rgbMatrix, "map.bmp")
    createMap(rgbMatrixShadow, "mapShadow.bmp")


if __name__ == '__main__':
    main()
