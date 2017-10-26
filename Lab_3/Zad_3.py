#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    r = 0
    g = 0
    if (v <= 0.5):
        g = 1.0 - v * 2
        b = v * 2
    else:
        r = v * 2 - 1
        b = 2.0 - v * 2
    return (r, g, b)


def gradient_rgb_gbr_full(v):
    r = 0
    g = 0
    if (v <= 0.25):
        g = 1
        b = v * 4
    elif (v <= 0.5):
        b = 1
        g = 1.0 - v * 4 + 1
    elif (v <= 0.75):
        b = 1
        r = v * 4 - 2
    else:
        r = 1
        b = 4.0 - 4 * v
    return (r, g, b)


def calcValue(entry, out, piece, all, value):
    if (entry > out):
        return piece - all * value
    else:
        return all * value - piece + 1


def inte(of, to, piece, all, value):
    a = of[0]
    d = of[1]
    c = of[2]
    x = to[0]
    y = to[1]
    z = to[2]
    if (a != x):
        r = calcValue(a, x, piece, all, value)
    else:
        r = a
    if (d != y):
        g = calcValue(d, y, piece, all, value)
    else:
        g = d
    if (c != z):
        b = calcValue(c, z, piece, all, value)
    else:
        b = c
    return r, g, b


def gradient_rgb_wb_custom(v):
    pieces = 7
    colors = [[1, 1, 1], [1, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0]]
    i = (int) (np.floor(pieces*v))%7
    r, g, b = inte(colors[i], colors[i + 1], i+1, pieces, v)
    return (r, g, b)


def gradient_hsv_bw(v):
    h, s, v = cs.rgb_to_hsv(v, v, v)
    return cs.hsv_to_rgb(h, s, v)


def gradient_hsv_gbr(v):
    h = 240 * v + 120
    if (v <= 0.5):
        s = abs(-abs(200 * v - 0.25) + 50) + 50
    else:
        s = abs(-abs(200 * (v - 0.5) - 0.25) + 50) + 50
    return cs.hsv_to_rgb(h / 360, s / 100, 1)


def gradient_hsv_unknown(v):
    return cs.hsv_to_rgb((120 - 120 * v) / 360, 0.5, 1)


def gradient_hsv_custom(v):
    return cs.hsv_to_rgb(2 * v % 1, 0.5 * v + 0.5, abs(0.5 * v - 0.5) + 0.5)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()


    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
