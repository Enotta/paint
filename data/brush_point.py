from PyQt6.QtGui import *


class BrushPoint:
    def __init__(self, x, y, color, thickness, alpha):
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness
        self.alpha = alpha

    def draw(self, painter):
        self.color.setAlpha(self.alpha)
        painter.setBrush(QBrush(self.color))
        painter.setPen(self.color)
        painter.drawEllipse(self.x - 5, self.y - 5, self.thickness, self.thickness)