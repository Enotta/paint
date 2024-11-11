from PyQt6 import QtWidgets, uic

import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import QColorDialog, QFileDialog, QMenu
from data.shapes import Line, Circle, Rectangle
from data.brush_point import BrushPoint


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        # Характеристики кисти
        self.color = QColor(255, 2, 0)  # Текущий цвет
        self.thickness = 5  # Ширина
        self.alpha = 255  # Прозрачность
        self.fill_figure = False  # Заливки
        self.instrument = 'brush'  # Кисть

        # Окно изначально
        uic.loadUi('forms/mypaint4.ui', self)
        self.setGeometry(100, 100, 1280, 720)
        self.set_menu_bar()

        self.objects = []  # Фигуры на экране

        self.verticalSlider.valueChanged.connect(self.update_thickness)  # Слайдер толщины
        self.verticalSlider_2.valueChanged.connect(self.update_alpha)  # Слайдер прозрачности

    def marker(self):
        self.instrument = 'marker'

    def rubber(self):
        self.instrument = 'rubber'

    def brush(self):
        self.instrument = 'brush'

    def line(self):
        self.instrument = 'line'

    def circle(self):
        self.instrument = 'circle'

    def rectangle(self):
        self.instrument = 'rectangle'

    def update_thickness(self, value):
        self.thickness = value

    def update_alpha(self, value):
        self.alpha = value

    def red(self):
        self.color = QColor(255, 0, 0, self.alpha)

    def black(self):
        self.color = QColor(0, 0, 0, self.alpha)

    def blue(self):
        self.color = QColor(0, 0, 255, self.alpha)

    def colours(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def fill(self):
        if self.fill_figure:
            self.fill_figure = False
        else:
            self.fill_figure = True

    def clear(self):
        self.objects.clear()
        self.update()

    def load_canvas(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.label_3.setScaledContents(True)
        pixmap = QPixmap(fname)

        self.label_3.setPixmap(pixmap)
        self.label_3.resize(0.5 * pixmap.size())
        self.update()

    def save_canvas(self):
        fname = \
            QFileDialog.getSaveFileName(self, 'Сохранить холст', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)')[
                0]
        if fname:
            pixmap = QPixmap(self.label_3.size())  # Создаем пиксмап размером с виджет
            painter = QPainter(pixmap)
            painter.begin(self.label_3)  # Начало рисования на пиксмапе
            # Рисуем картинку, если она есть
            if self.label_3.pixmap():
                painter.drawPixmap(self.label_3.geometry().topLeft(), self.label_3.pixmap())
            # Рисуем объекты, созданные на холсте
            for obj in self.objects:
                obj.draw(painter)
            painter.end()
            pixmap.save(fname)

    # def set_canvas(self):
    #     painter = QPainter()
    #     painter.begin(self)
    #     rec = Rectangle(1248, 699, -1103, -637, QColor(255, 255, 255, 255), 255, True)
    #     rec.draw(painter)
    #     painter.end()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            if ((type(obj) is BrushPoint) and
                    self.label_3.x() <= obj.x <= self.label_3.x() + self.label_3.width() and
                    self.label_3.y()+40 <= obj.y <= self.label_3.y() + self.label_3.height()):
                obj.draw(painter)
            elif (type(obj) is Line and self.label_3.x() <= obj.sx <= self.label_3.x() + self.label_3.width() and
                  self.label_3.y()+40 <= obj.sy <= self.label_3.y() + self.label_3.height()):
                obj.draw(painter)
            elif (type(obj) is Circle and self.label_3.x() <= obj.cx <= self.label_3.x() + self.label_3.width() and
                  self.label_3.y()+40 <= obj.cy <= self.label_3.y() + self.label_3.height()):
                obj.draw(painter)
            elif (type(obj) is Rectangle and self.label_3.x() <= obj.rx <= self.label_3.x() + self.label_3.width() and
                  self.label_3.y()+40 <= obj.ry <= self.label_3.y() + self.label_3.height()):
                print(obj.x, obj.y, obj.rx, obj.ry, obj.color)
                obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        if self.instrument == 'brush':
            self.objects.append(BrushPoint(event.pos().x(), event.pos().y(), self.color, self.thickness, self.alpha))
            self.update()
        if self.instrument == 'line':
            self.objects.append(
                Line(event.pos().x(), event.pos().y(), event.pos().x(), event.pos().y(), self.color, self.thickness,
                     self.alpha))
            self.update()
        if self.instrument == 'circle':
            self.objects.append(
                Circle(event.pos().x(), event.pos().y(), event.pos().x(), event.pos().y(), self.color, self.alpha,
                       self.fill_figure))
            self.update()
        if self.instrument == 'rectangle':
            self.objects.append(
                Rectangle(event.pos().x(), event.pos().y(), event.pos().x(), event.pos().y(), self.color, self.alpha,
                          self.fill_figure))
            self.update()
        if self.instrument == 'marker':
            self.objects.append(BrushPoint(event.pos().x(), event.pos().y(), self.color, 40, 128))
            self.update()

    def mouseMoveEvent(self, event):
        if self.instrument == 'brush':
            self.objects.append(BrushPoint(event.pos().x(), event.pos().y(), self.color, self.thickness, self.alpha))
            self.update()

        if self.instrument == 'line':
            self.objects[-1].ex = event.pos().x()
            self.objects[-1].ey = event.pos().y()
            self.update()

        if self.instrument == 'circle':
            self.objects[-1].x = event.pos().x()
            self.objects[-1].y = event.pos().y()
            self.update()

        if self.instrument == 'rectangle':
            self.objects[-1].x = event.pos().x() - self.objects[-1].rx
            self.objects[-1].y = event.pos().y() - self.objects[-1].ry
            self.update()

        if self.instrument == 'rubber':
            self.erase(event.pos())
            self.update()

        if self.instrument == 'marker':
            self.objects.append(BrushPoint(event.pos().x(), event.pos().y(), self.color, 40, 128))
            self.update()

    def erase(self, position):
        """Удаляет объекты, пересекающиеся с позицией ластика."""
        to_remove = []
        for obj in self.objects:
            if isinstance(obj, BrushPoint):  # Если это точка кисти
                if (obj.x - position.x()) ** 2 + (obj.y - position.y()) ** 2 <= self.thickness ** 2:
                    to_remove.append(obj)
            elif isinstance(obj, Line):  # Если это линия
                if self.is_line_nearby(obj, position):
                    to_remove.append(obj)
            elif isinstance(obj, Circle):  # Если это круг
                if self.is_circle_nearby(obj, position):
                    to_remove.append(obj)
            elif isinstance(obj, Rectangle):  # Если это прямоугольник
                if self.is_rectangle_nearby(obj, position):
                    to_remove.append(obj)

        # Удаляем найденные объекты
        for obj in to_remove:
            self.objects.remove(obj)

    def is_line_nearby(self, line, position):
        """Проверка, пересекает ли линия точку ластика."""
        # Тут можно добавить более сложную логику для проверки, если линия близка к точке
        return False

    def is_circle_nearby(self, circle, position):
        """Проверка, пересекает ли круг точку ластика."""
        distance = ((circle.cx - position.x()) ** 2 + (circle.cy - position.y()) ** 2) ** 0.5
        return distance <= self.thickness  # Ластик должен иметь радиус, чтобы удалять круги

    def is_rectangle_nearby(self, rectangle, position):
        """Проверка, пересекает ли прямоугольник точку ластика."""
        # Для упрощения: проверяем, находится ли точка внутри прямоугольника
        return (rectangle.rx <= position.x() <= rectangle.rx + rectangle.x and
                rectangle.ry <= position.y() <= rectangle.ry + rectangle.y)

    def set_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = QMenu("&Файл", self)

        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_canvas)
        file_menu.addAction(load_action)

        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_canvas)
        file_menu.addAction(save_action)

        file_menu.addSeparator()
        clear_action = QAction("Очистить", self)
        clear_action.triggered.connect(self.clear)
        file_menu.addAction(clear_action)
        file_menu.addSeparator()

        exit_action = QAction("Выйти", self)
        exit_action.triggered.connect(lambda: self.close())
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

        shape_menu = menu_bar.addMenu("&Фигура")
        circle_action = QAction("Окружность", self)
        circle_action.triggered.connect(self.circle)
        shape_menu.addAction(circle_action)

        line_action = QAction("Линия", self)
        line_action.triggered.connect(self.line)
        shape_menu.addAction(line_action)

        rectangle_action = QAction("Прямоугольник", self)
        rectangle_action.triggered.connect(self.rectangle)
        shape_menu.addAction(rectangle_action)

        shape_menu.addSeparator()
        fill_action = QAction("Заливка", self)
        fill_action.triggered.connect(self.fill)
        shape_menu.addAction(fill_action)

        brushes_menu = menu_bar.addMenu("&Кисти")

        brush_action = QAction("Карандаш", self)
        brush_action.triggered.connect(self.brush)
        brushes_menu.addAction(brush_action)

        marker_action = QAction("Маркер", self)
        marker_action.triggered.connect(self.marker)
        brushes_menu.addAction(marker_action)

        rubber_action = QAction("Ластик", self)
        rubber_action.triggered.connect(self.rubber)
        brushes_menu.addAction(rubber_action)

        colour_menu = menu_bar.addMenu("&Цвет")

        red_action = QAction("Красный", self)
        red_action.triggered.connect(self.red)
        colour_menu.addAction(red_action)

        blue_action = QAction("Синий", self)
        blue_action.triggered.connect(self.blue)
        colour_menu.addAction(blue_action)

        black_action = QAction("Чёрный", self)
        black_action.triggered.connect(self.black)
        colour_menu.addAction(black_action)

        colour_menu.addSeparator()

        colours_action = QAction("Цвет на выбор", self)
        colours_action.triggered.connect(self.colours)
        colour_menu.addAction(colours_action)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec())
