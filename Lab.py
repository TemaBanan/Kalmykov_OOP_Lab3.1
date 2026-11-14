from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication

class Krug:
    radius = 20  # одинаковый для всех кругов радиус

    def __init__(self, x, y):
        self._x = x  # координаты центра круга
        self._y = y
        self.radius = Krug.radius
        print(f'Был создан круг по координатам x: {x}, y: {y}!')

    def draw_krug(self, painter):
        painter.setPen(QColor(0, 255, 0))
        painter.drawEllipse(self._x - self.radius, self._y - self.radius,
                            self.radius * 2, self.radius * 2)

class Storage:  # собственный объект-контейнер (внутри список, снаружи ведёт себя как список с курсором)
    def __init__(self):
        self._kontainer = []
        self._tekush_index = 0

    def add_krug(self, krug):
        self._kontainer.append(krug)

    def first(self):
        self._tekush_index = 0

    def next(self):
        self._tekush_index += 1

    def end_of_list(self):
        return self._tekush_index >= len(self._kontainer)

    def get_object(self):
        if not self.end_of_list():
            return self._kontainer[self._tekush_index]
        return None

class Holst(QWidget):
    def __init__(self):
        super().__init__()
        self.storage = Storage()

    def paintEvent(self, event):  # отрисовка всех кругов из контейнера
        painter = QPainter(self)
        self.storage.first()
        while not self.storage.end_of_list():
            self.storage.get_object().draw_krug(painter)
            self.storage.next()

    def mousePressEvent(self, event):  # клик создаёт круг
        if event.button() == Qt.MouseButton.LeftButton:
            self.storage.add_krug(Krug(event.pos().x(), event.pos().y()))
            self.update()

class Prilojenie(QMainWindow):  # само приложение
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GUI')
        self.resize(800, 600)
        self.holst = Holst()
        self.setCentralWidget(self.holst)

def main():
    prilojenie = QApplication([])
    window = Prilojenie()
    window.show()
    prilojenie.exec()

if __name__ == '__main__':
    main()