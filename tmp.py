from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
import sys
import math
import time
import numpy as np
import pyqtgraph as pg

class Frame:
    def __init__(self, position, time):
        self.position = position
        self.time = time

    def speed(self, frame):
        d = distance(*self.position, *frame.position)
        time_delta = abs(frame.time - self.time)
        if time_delta == 0:
            return None
        else:
            return d / time_delta

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_current_cursor_position():
    pos = QtGui.QCursor.pos()
    return pos.x(), pos.y()

def get_current_frame():
    return Frame(get_current_cursor_position(), time.time())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Realtime-Digital-Filter-Designer")
        self.setMouseTracking(True)

        self.last_frame = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.calculate_speed)
        self.timer_interval = 50  # Set an initial interval in milliseconds (e.g., 50ms)
        self.mouse_inside = False

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setGeometry(QtCore.QRect(10, 10, 400, 300))
        self.plot_widget.showGrid(x=True, y=True)

    def calculate_speed(self):
        if self.last_frame is not None and self.mouse_inside:
            new_frame = get_current_frame()
            speed = new_frame.speed(self.last_frame)

            if speed is not None:
                frequency = speed * 10  # Adjust the scaling factor as needed
                self.plot_signal(frequency)

            self.last_frame = new_frame

    def plot_signal(self, frequency):
        x = np.linspace(0, 2 * np.pi, 1000)
        y = np.cos(frequency * x)
        self.plot_widget.clear()
        self.plot_widget.plot(x, y, pen=pg.mkPen('b'))

    def eventFilter(self, source, event):
        if source == self:
            if event.type() == QtCore.QEvent.MouseMove:
                self.x = event.x()
                self.y = event.y()
                self.mouse_inside = True
                self.timer.start(self.timer_interval)
                self.last_frame = get_current_frame()

            elif event.type() == QtCore.QEvent.Leave:
                self.mouse_inside = False
                self.timer.stop()

        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
