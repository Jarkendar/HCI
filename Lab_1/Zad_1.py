#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

import matplotlib.pyplot as plt
import numpy as np


def addFunctionToPlot(name, ax, colorName, mStyle, lastLines):
    file = open(name, "r")
    reader = csv.reader(file)
    first = 1
    averages = []
    sizes = []
    for line in reader:
        iterator = 0
        sumCell = 0
        lastLine = []
        if first == 0:
            if int(line[0]) == 199:
                for cell in line[2:]:
                    lastLine.append(float(cell) * 100)

            sizes.append(int(line[1]))
            data = list(line)[2:]
            for cell in data:
                sumCell = sumCell + float(cell)
                iterator = iterator + 1
            averages.append(sumCell / iterator)
        else:
            first = 0
    lastLines.append(lastLine)

    ax.plot(sizes, averages, color=colorName, marker=mStyle, markevery=25, markeredgecolor='black')


def main():
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(121)
    box = fig.add_subplot(122)
    ax2 = ax1.twiny()

    lastLines = []

    addFunctionToPlot("rsel.csv", ax1, 'b', 'o', lastLines)
    addFunctionToPlot("cel-rs.csv", ax1, 'g', 'v', lastLines)
    addFunctionToPlot("2cel-rs.csv", ax1, 'r', 'D', lastLines)
    addFunctionToPlot("cel.csv", ax1, 'black', 's', lastLines)
    addFunctionToPlot("2cel.csv", ax1, 'violet', 'd', lastLines)

    meanprops = dict(marker='o', color='b')
    boxprops = dict(color='b')

    box.boxplot(lastLines, 'b+', showmeans=True, meanprops=meanprops, boxprops=boxprops)
    box.set_yticks(np.arange(60, 101, 5))
    box.set_ylim(60, 100)
    box.yaxis.tick_right()
    box.set_xticklabels(["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"], rotation=15, family='serif')
    box.grid(linestyle=':')

    ax1.set_xlim(0, 500000)
    ax1.set_ylim(0.60, 1.00)
    ax1.set_xlabel("Rozegranych gier")
    ax1.set_ylabel("Odsetek wygranych gier")
    ax1.set_xticks(np.arange(0, 500001, 100000))
    ax1.set_yticks(np.arange(0.60, 1.01, 0.05))
    ax1.legend(["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"], numpoints=2)
    ax1.grid(linestyle=':')

    ax2.set_xlim(0, 200)
    ax2.set_xlabel("Pokolenie")
    ax2.set_xticks(np.arange(0, 201, 40))

    # plt.show()
    plt.savefig('myplot.pdf')  # zapis do pdf
    plt.show()
    plt.close()


if __name__ == '__main__':
    main()
