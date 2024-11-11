import sys

from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *


class Line:
    def __init__(self, sx, sy, ex, ey, color, thickness, alpha):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color = color
        self.thickness = thickness
        self.alpha = alpha

    def draw(self, painter):
        self.color.setAlpha(self.alpha)
        painter.setBrush(QBrush(QColor(self.color)))
        pen = QtGui.QPen(self.color, self.thickness)
        painter.setPen(pen)
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Circle:
    def __init__(self, cx, cy, x, y, color, alpha, fill_figure):
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.color = color
        self.alpha = alpha
        self.fill_figure = fill_figure

    def draw(self, painter):
        self.color.setAlpha(self.alpha)
        if self.fill_figure:
            painter.setBrush(QBrush(QColor(self.color)))
        else:
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QColor(self.color))
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, 2 * radius, 2 * radius)


class Rectangle:
    def __init__(self, rx, ry, x, y, color, alpha, fill_figure):
        self.rx = rx
        self.ry = ry
        self.x = x
        self.y = y
        self.color = color
        self.alpha = alpha
        self.fill_figure = fill_figure

    def draw(self, painter):
        self.color.setAlpha(self.alpha)
        if self.fill_figure:
            painter.setBrush(QBrush(QColor(self.color)))
        else:
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QColor(self.color))
        painter.drawRect(self.rx, self.ry, self.x, self.y)