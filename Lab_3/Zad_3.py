from __future__ import division  # Division in Python 2.7
import matplotlib

matplotlib.use('Agg')  # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

import colorsys as cs


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400  # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('gradients.pdf')


def hsv2rgb(h, s, v):
    # TODO
    return (0, 0, 0)


def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    pieces = 2
    colors = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    i = int(np.floor(pieces * v)) % pieces
    r, g, b = interpolColor(colors[i], colors[i + 1], i + 1, pieces, v)
    return r, g, b


def gradient_rgb_gbr_full(v):
    pieces = 4
    colors = [[0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0]]
    i = int(np.floor(pieces * v)) % pieces
    r, g, b = interpolColor(colors[i], colors[i + 1], i + 1, pieces, v)
    return r, g, b


def gradient_rgb_wb_custom(v):
    pieces = 7
    colors = [[1, 1, 1], [1, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0]]
    i = int(np.floor(pieces * v)) % pieces
    r, g, b = interpolColor(colors[i], colors[i + 1], i + 1, pieces, v)
    return r, g, b


def gradient_hsv_bw(v):
    h, s, v = cs.rgb_to_hsv(v, v, v)
    return cs.hsv_to_rgb(h, s, v)


def calculateHue(startAngle, countAllPieces, value):
    return ((startAngle + value * startAngle * countAllPieces) / 360) % 1


def gradient_hsv_gbr(v):
    if v <= 0.5:
        s = abs(-abs(200 * v - 0.25) + 50) + 50
    else:
        s = abs(-abs(200 * (v - 0.5) - 0.25) + 50) + 50
    return cs.hsv_to_rgb(calculateHue(120, 2, v), s / 100, 1)


def gradient_hsv_unknown(v):
    return cs.hsv_to_rgb((120 - 120 * v) / 360, 0.5, 1)


def gradient_hsv_custom(v):
    return cs.hsv_to_rgb(2 * v % 1, 0.5 * v + 0.5, abs(0.5 * v - 0.5) + 0.5)


def calculateValuePieceOfColor(inColor, outColor, numberOfPiece, countAllPieces, value):
    if inColor > outColor:
        return numberOfPiece - countAllPieces * value
    else:
        return countAllPieces * value - numberOfPiece + 1


def interpolColor(fromColor, toColor, numberOfPiece, countAllPieces, value):
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


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()


    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
