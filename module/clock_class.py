from PySide6 import QtCore, QtGui, QtWidgets
import math
import time

class MovingLineClock(QtWidgets.QWidget):
    SEC_COLOR = QtGui.QColor(31, 31, 31, 100)
    DEGREES_PER_SECOND = math.pi / 30

    def __init__(self, size=200):
        super().__init__()
        self.start_time = time.time()
        self.size = size

        self.setWindowTitle("Clock")
        self.resize(size, size)
        self.initTimer()
        
        self.old_pos = 0
        self.sec_histroy = []

        self.setWindowFlags(
              QtCore.Qt.FramelessWindowHint # Remove title
            | QtCore.Qt.WindowStaysOnTopHint # Place on the top
            | QtCore.Qt.SplashScreen # Not on the taskbar
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        quitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(quitAction)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def initTimer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # 매 초마다 update() 호출

    def draw_special_circle(self, painter, radius, sec_radian):
        # 부채꼴의 위치와 크기 동적 계산
        pie_x = -radius
        pie_y = -radius
        pie_width = radius * 2
        pie_height = radius * 2
        painter.setBrush(QtCore.Qt.white)

        # 부채꼴 그리기
        start_angle = 90 * 16
        span_angle = -sec_radian * 16 * 180 / math.pi
        painter.drawPie(pie_x, pie_y, pie_width, pie_height, start_angle, span_angle)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        tm = time.time() - self.start_time
        t_sec = round(tm % 60)

        radius = self.size * 0.9 / 2
        sec_radian = t_sec * self.DEGREES_PER_SECOND
        min_radian = (tm / 60) % 60 * self.DEGREES_PER_SECOND

        x = math.sin(sec_radian) * radius
        y = -math.cos(sec_radian) * radius

        painter.setPen(QtCore.Qt.white)
        painter.setBrush(QtGui.QBrush(self.SEC_COLOR))
        painter.drawEllipse(QtCore.QPoint(0, 0), radius, radius)

        for h_x, h_y in self.sec_histroy:
            painter.drawLine(0, 0, h_x, h_y)
        painter.drawLine(0, 0, x, y)
        
        self.sec_histroy.append([x, y])
        
        self.draw_special_circle(painter, radius, min_radian)

        if t_sec == 59:
            self.sec_histroy = []

        painter.end()
    
    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.old_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self.move(e.globalPosition().toPoint()-self.old_pos)