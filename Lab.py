from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication


class Holst(QWidget):  # холст, на котором будем рисовать круги
    def __init__(self):
        super().__init__()


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