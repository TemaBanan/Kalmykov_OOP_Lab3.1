from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication

class Krug:
    radius = 20  # одинаковый для всех кругов радиус

    def __init__(self, x, y):
        self._x = x  # координаты центра круга
        self._y = y
        self.radius = Krug.radius
        self.is_selected = False  # выделен ли круг
        print(f'Был создан круг по координатам x: {x}, y: {y}!')

    def draw_krug(self, painter):
        if self.is_selected:
            painter.setPen(QColor(85, 107, 47))  # выделенные красим в оливковый
        else:
            painter.setPen(QColor(0, 255, 0))  # по умолчанию лаймовый
        painter.drawEllipse(self._x - self.radius, self._y - self.radius,
                            self.radius * 2, self.radius * 2)

    def contains(self, x, y):  # круг сам решает, попала ли в него точка
        distance = ((x - self._x) ** 2 + (y - self._y) ** 2) ** 0.5
        return distance <= self.radius

    def print_removed(self):
        print(f'Круг удалён! Координаты центра: x: {self._x}, y: {self._y}')

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

    def clear_selection(self):
        for krug in self._kontainer:
            krug.is_selected = False

    def remove_selected(self):
        for krug in self._kontainer:
            if krug.is_selected:
                krug.print_removed()
        self._kontainer = [krug for krug in self._kontainer if not krug.is_selected]

class Holst(QWidget):
    def __init__(self):
        super().__init__()
        self.storage = Storage()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):  # отрисовка всех кругов из контейнера
        painter = QPainter(self)
        self.storage.first()
        while not self.storage.end_of_list():
            self.storage.get_object().draw_krug(painter)
            self.storage.next()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            clicked_on_circle = False
            self.storage.first()
            while not self.storage.end_of_list():
                krug = self.storage.get_object()
                if krug.contains(x, y):
                    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                        krug.is_selected = not krug.is_selected  # Ctrl+клик: добавить/убрать из выделения
                    else:
                        self.storage.clear_selection()  # обычный клик: выделяем только этот круг
                        krug.is_selected = True
                    clicked_on_circle = True
                    break
                self.storage.next()
            if not clicked_on_circle:  # клик по пустому месту: новый круг
                self.storage.clear_selection()
                self.storage.add_krug(Krug(x, y))
            self.update()

    def keyPressEvent(self, event):  # Del удаляет выделенные круги
        if event.key() == Qt.Key.Key_Delete:
            self.storage.remove_selected()
            self.update()

    def resizeEvent(self, event):  # отладочный вывод при изменении размера
        super().resizeEvent(event)
        print(f'Размер формы изменен: {event.size().width()}x{event.size().height()}')
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