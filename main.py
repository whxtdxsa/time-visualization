from PySide6 import QtWidgets
import sys

from module.clock_class import MovingLineClock

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    clock = MovingLineClock(size= 100)
    clock.show()
    sys.exit(app.exec())