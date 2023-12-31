from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider, QMenu
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
import sys
import math
import time
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class Frame:
    def __init__ (self, position, time):
        self.position = position
        self.time = time

    def speed (self, frame):
        d = distance (*self.position, *frame.position)
        time_delta = abs (frame.time - self.time)
        if time_delta == 0:
            return None
        else:
            return d / time_delta

def distance (x1, y1, x2, y2):
    return math.sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_current_cursor_position ():
    pos = QCursor.pos ()
    return pos.x (), pos.y ()

def get_current_frame ():
    return Frame (get_current_cursor_position (), time.time ())

# class MainWindow(QtWidgets.QMainWindow):
      

#      # Mainwindow constructor
#       def __init__(self, *args, **kwargs):
#           super(MainWindow, self).__init__(*args, **kwargs)
#           uic.loadUi('mainwindow.ui', self)
#           self.setWindowIcon(QtGui.QIcon('icons/filterIcon.png'))
#           self.setWindowTitle("Realtime-Digital-Filter-Designer")
#           self.setMouseTracking(True)
#           self.customSignalPaddingWidget.setMouseTracking(True)
#           self.customSignalPaddingWidget.installEventFilter(self)
#           self.last_frame = None
#           self.timer = QTimer(self)
#           self.timer.timeout.connect(self.calculate_speed)
#           self.timer_interval = 50  # Set an initial interval in milliseconds (e.g., 100ms)
#           self.mouse_inside = False

#       def calculate_speed(self):
#         if self.last_frame is not None and self.mouse_inside:
#             new_frame = get_current_frame()
#             speed = new_frame.speed(self.last_frame)
#             if speed is not None:
#                 print(f"Cursor Speed: {speed} pixels per second")
#             self.last_frame = new_frame

#       def eventFilter(self, source, event):
#         if source == self.customSignalPaddingWidget:
#             if event.type() == QtCore.QEvent.Enter: 
#                 # if event.type() == QtCore.QEvent.MouseMove:
#                     self.mouse_inside = True
#                     self.timer.start(self.timer_interval)
#                     self.last_frame = get_current_frame()
#             elif event.type() == QtCore.QEvent.Leave:
#                 self.mouse_inside = False
#                 self.timer.stop()
#             elif event.type() == QtCore.QEvent.MouseMove:
#                 self.x = event.x()
#                 self.y = event.y()
#                 # print(f"Mouse Coordinates:({self.x}, {self.y})")
#                 # print("Mouse is over the widget and within its boundaries")
#         return super().eventFilter(source, event)