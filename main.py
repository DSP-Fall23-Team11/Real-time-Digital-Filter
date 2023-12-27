# Imports
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider, QMenu
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
import sys

from pyqtgraph import PlotWidget
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow):

     # Mainwindow constructor
      def __init__(self, *args, **kwargs):

          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('mainwindow.ui', self)
          self.setWindowIcon(QtGui.QIcon('icons/filterIcon.png'))
          self.setWindowTitle("Realtime-Digital-Filter-Designer")



def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
