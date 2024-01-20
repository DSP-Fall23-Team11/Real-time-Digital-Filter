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
