from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QSlider, QComboBox, QGraphicsRectItem,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor,QMouseEvent,QPixmap, QPainter, QCursor
from PyQt5.QtCore import Qt, QRectF,pyqtSignal,QFile,QTextStream
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal, QPoint ,QTimer, QFile, QTextStream
from PyQt5.QtCore import QTimer, QFile, QTextStream
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider, QMenu
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
from sympy.functions import arg
from sympy import symbols, I, E, conjugate, Abs
import sys
import logging
import time
import pyqtgraph as pg
import numpy as np
from speed import *
from PlotZ import plotZ
from scipy.signal import zpk2tf, lfilter

from Signal import Signal
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        uic.loadUi('UI/mainwindow.ui', self)
        self.apply_stylesheet("ManjaroMix.qss")
        # self.showMaximized()
        init_connectors(self)
        self.initalize()
        self.ZPlotter = plotZ(self.poles ,self.zeros, self.scale) 
        self.plot()
        #################################################
        self.setMouseTracking(True)
        self.padWidgetGraph.setMouseTracking(True)
        self.padWidgetGraph.installEventFilter(self)
        self.last_frame = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.calculate_speed)
        self.timer_interval = 50  # Set an initial interval in milliseconds (e.g., 100ms)
        self.mouse_inside = False
        self.modifiedSignal=[]
        self.allPassComboBox.setEditable(True)

        self.x = 0
        self.y = 0
        self.speed = 0

        self.viewBox =self.inputSignalGraph.getViewBox()
        self.viewBox1 =self.filteredSignalGraph.getViewBox()
        self.initalizeGraph()

        self.generatedSignal = Signal()

        

    

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(),self.pix)

    def responsePlot(self, widgets:list, data:list, titles:list):
        for index,widget in enumerate(widgets):
            widget.canvas.axes.clear()
            widget.canvas.axes.plot(data[index][0] , data[index][1] , color ="b")
            widget.canvas.axes.set_title(titles[index])    
            widget.canvas.draw()

    def processZPlotting(self):
      # TODO Call plotz
      # TODO Set labels for the mag / phase plots
        magnitudePlotData = []
        phasePlotData = []
        magnitudePlotData = self.ZPlotter.plot_magnitude_response()
        phasePlotData = self.ZPlotter.plot_phase_response()
        widgets = [self.magGraphWidget , self.phaseGraphWidget]
        data = [magnitudePlotData,phasePlotData]
        titles= ["Magnitude Response" , "Phase Response"]
        self.responsePlot(widgets,data,titles)

    
    def initalize(self):
        self.scaleRate = 1
        self.scale = 100 # 100 for z-plane
        self.delRange = 10/self.scale # deletion range for deletion box & click
        self.sizePole = 4 # cross length: (-4, -4), (-4, 4), (4, -4), (4, 4): -4 to 4 from up to down and from left to right
        self.sizeZero = 7 # circle length: -7/2 to 7/2 from up to down and from left to right
        self.sensitivity = 0.005 # 0.005 for z-plane
        self.filterData = [] # ...[-1] is last pole/zero ('s coordinates) added to map
        self.zeros, self.poles = [], [] # added poles/zeros
        self.dragFlag = False # true when mouse clicked and moves  used in drag and drop
    
        self.Height = int(self.unitCircleGraphWidget.height())
        self.Width = int(self.unitCircleGraphWidget.width())
        self.middleHeight = int(self.Height/2)
        self.middleWidth  = int(self.Width /2)

        



    def plot(self):
        self.pix = QPixmap(self.unitCircleGraphWidget.rect().size())
        self.pix.fill(Qt.white)
        painter = QPainter(self.pix)
        painter.drawLine(0,self.middleHeight , self.Width, self.middleHeight)
        painter.drawLine(self.middleWidth ,0, self.middleWidth, self.Height)
        painter.drawEllipse(self.middleWidth-int(1*self.scale), self.middleHeight-int(1*self.scale), int(2*self.scale), int(2*self.scale))
        indexFactor = 3
        for i in np.arange(self.middleHeight%(self.scale/10), self.Height+self.scale/10+1, self.scale/10):
                i = int(i)
                if i%self.scale==self.middleHeight%self.scale: indexFactor = int(indexFactor*2)
                painter.drawLine(self.middleWidth-indexFactor, i, self.middleWidth+indexFactor, i)
                if i%self.scale==self.middleHeight%self.scale: indexFactor = int(indexFactor/2)
        for i in np.arange(self.middleWidth%(self.scale/10), self.Width+self.scale/10+1, self.scale/10):
                i = int(i)
                if i%self.scale==self.middleWidth%self.scale: indexFactor = int(indexFactor*2)
                painter.drawLine(i, self.middleHeight-indexFactor, i, self.middleHeight+indexFactor)
                if i%self.scale==self.middleWidth%self.scale: indexFactor = int(indexFactor/2)
        for pole in self.poles:
            xx = int(self.scale*pole[0])
            yx = int(self.scale*pole[1])
            x = int(xx + self.middleWidth)
            y = int(-yx + self.middleHeight)
            painter.drawLine(x-self.sizePole, y-self.sizePole, x+self.sizePole, y+self.sizePole) 
            painter.drawLine(x-self.sizePole, y+self.sizePole, x+self.sizePole, y-self.sizePole) 
        for zero in self.zeros:
            xx = int(self.scale*zero[0])
            yx = int(self.scale*zero[1])
            x = int(xx + self.middleWidth)
            y = int(-yx + self.middleHeight)
            painter.drawEllipse(x-int(self.sizeZero/2), y-int(self.sizeZero/2), self.sizeZero, self.sizeZero)      
        self.update() 
        self.processZPlotting()     

    def filter_real_time_signal(self, input_signal):
        # Use the ZeroPole filter equation to filter the input signal
        # print(self.zeros)
        zeros = [complex(z[0], z[1]) for z in self.zeros]
        poles = [complex(p[0], p[1]) for p in self.poles]

        # zeros_poly = np.poly(np.array(self.zeros)[:, 0] + 1j * np.array(self.zeros)[:, 1])
        # filtered_signal = lfilter([1], zeros_poly, input_signal, axis=-1, zi=None)
        numerator, denominator = zpk2tf(zeros,poles,1)
        filtered_signal_y = np.real(lfilter(numerator, denominator, input_signal.copy()))
        return filtered_signal_y
        

    def mouseReleaseEvent(self, event):
        self.dragFlag = False
        QWidget.setCursor(self, QCursor(Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        if not self.deleteCheckBox.isChecked() and (event.buttons()==Qt.LeftButton or event.buttons()==Qt.RightButton) and len(self.filterData)>0:
            begin = event.pos()
            x = -self.middleWidth+begin.x() 
            y = self.middleHeight-begin.y()

            if abs(x)>self.middleWidth or abs(y)> self.middleHeight:
                return
            QWidget.setCursor(self, QCursor(Qt.ClosedHandCursor))

            if not self.dragFlag:
                self.delete([x/self.scale, y/self.scale], draw=False)
                self.dragFlag = True
            else:
                self.delete(self.filterData[-1], draw=False)
            self.add([x/self.scale, y/self.scale], "pole" if event.buttons()==Qt.LeftButton else "zero")

    def mousePressEvent(self, event):
        QWidget.setCursor(self, QCursor(Qt.PointingHandCursor))
        begin = event.pos()
        x = -self.middleWidth+begin.x() 
        y = self.middleHeight-begin.y()  

        if self.deleteCheckBox.isChecked():
            self.delete([x/self.scale, y/self.scale], draw=True)
        elif self.search([x/self.scale, y/self.scale])==False:
            self.dragFlag = True
            self.add([x/self.scale, y/self.scale], "pole" if event.buttons()==Qt.LeftButton else "zero")   

    def search(self, pos):
        for i in self.filterData[::-1]:
            if abs(i[0]-pos[0])<self.delRange and (abs(i[1]-pos[1])<self.delRange or abs(i[1]+pos[1])<self.delRange):
                if self.poles.count(i)>0 or self.poles.count([i[0], -i[1]])>0 or self.zeros.count(i)>0 or self.zeros.count([i[0], -i[1]]):
                    return True
        return False

        
    def add(self, pos, case, draw=True):
        self.filteredSignalGraph.clear()
        if abs(pos[0])>self.middleWidth/self.scale or abs(pos[1])>self.middleHeight/self.scale:
            self.dragFlag = False
            return
        if -5/self.scale<pos[1]<5/self.scale: pos[1] = 0
        if -5/self.scale<pos[0]<5/self.scale: pos[0] = 0
        self.filterData.append(pos)
        if case=="pole":
            if pos[1]==0 or not self.addConjugateCheckBox.isChecked(): self.poles.append(pos)
            else: self.poles.append(pos); self.poles.append([pos[0], -pos[1]])
           # self.statusBar.showMessage(f"Pole is added to ({round(pos[0], 2)}, {round(pos[1], 2)}). Current case: {'Divergent' if len(self.zeros)>len(self.poles) else 'Convergent'}{' to some constant' if len(self.zeros)==len(self.poles) else ''}. P:{int(len(self.poles))}, Z:{int(len(self.zeros))}")
        elif case=="zero":
            if pos[1]==0 or not self.addConjugateCheckBox.isChecked(): self.zeros.append(pos)
            else: self.zeros.append(pos); self.zeros.append([pos[0], -pos[-1]])
          #  self.statusBar.showMessage(f"Zero is added to ({round(pos[0], 2)}, {round(pos[1], 2)}). Current case: {'Divergent' if len(self.zeros)>len(self.poles) else 'Convergent'}{' to some constant' if len(self.zeros)==len(self.poles) else ''}. P:{int(len(self.poles))}, Z:{int(len(self.zeros))}")
        if draw: self.plot()   

    def addFilter(self):
        filter_value = complex(self.allPassComboBox.currentText())
        self.allPassLibrary.addItem(str(filter_value))
              
    
    def plotAllPassResponse(self,a):
        a = complex(a)
        self.allPassResponse.clear()
        x_values = np.linspace(0, np.pi, 1000)
        yAxis = []
        for xValue in x_values:
            Hap = (np.exp(-1j * xValue) - np.conjugate(a)) / (1 - a * np.exp(-1j * xValue))
            yAxis.append(np.angle(Hap))         
        self.allPassResponse.plot(x_values, yAxis, pen="b")
        self.modifiedSignal= self.generatedSignal.yAxis*np.exp(1j * np.angle(yAxis))
        

    

    def delete(self, pos, draw=True):
        for i in self.filterData[::-1]:
            if abs(i[0]-pos[0])<self.delRange and (abs(i[1]-pos[1])<self.delRange or abs(i[1]+pos[1])<self.delRange):
                if self.poles.count(i)>0 or self.poles.count([i[0], -i[1]])>0:
                    if i[1]==0 or not self.addConjugateCheckBox.isChecked(): self.poles.remove(i)
                    else: self.poles.remove(i); self.poles.remove([i[0], -i[1]])
                   # self.statusBar.showMessage(f"Pole is deleted from ({round(i[0], 2)}, {round(i[1], 2)}). Current case: {'Divergent' if len(self.zeros)>len(self.poles) else 'Convergent'}{' to some constant' if len(self.zeros)==len(self.poles) else ''}. P:{int(len(self.poles))}, Z:{int(len(self.zeros))})")
                elif self.zeros.count(i)>0 or self.zeros.count([i[0], -i[1]]):
                    if i[1]==0 or not self.addConjugateCheckBox.isChecked(): self.zeros.remove(i)
                    else: self.zeros.remove(i); self.zeros.remove([i[0], -i[1]])
                 #   self.statusBar.showMessage(f"Zero is deleted from ({round(i[0], 2)}, {round(i[1], 2)}). Current case: {'Divergent' if len(self.zeros)>len(self.poles) else 'Convergent'}{' to some constant' if len(self.zeros)==len(self.poles) else ''}. P:{int(len(self.poles))}, Z:{int(len(self.zeros))})")
                else:
                    print("Mama got an error")
                self.filterData.remove(i)
                break
        if draw: self.plot()

    def clear(self):
        self.initalize()
        self.ZPlotter.setData(self.poles ,self.zeros, self.scale)
        self.plot()    
    def clearAllZeros(self):
        self.zeros = []
        self.filterData = []
        for  i in self.poles:
          self.filterData.append(i)
        self.ZPlotter.setData(self.poles ,self.zeros, self.scale) 
        self.plot()     
    def clearAllPoles(self):
        self.poles = []
        self.filterData = []
        for  i in self.zeros:
          self.filterData.append(i)
        self.ZPlotter.setData(self.poles ,self.zeros, self.scale) 
        self.plot()     

    def apply_stylesheet(self, stylesheet_path):
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            qss = stream.readAll()
            self.setStyleSheet(qss)
        else:
            print(f"Failed to open stylesheet file: {stylesheet_path}")

    def setSignalPoint(self,speed,amp):
        self.generatedSignal.appendAmplitude(amp)
        self.generatedSignal.appedFrequency(speed/200)
        self.generatedSignal.appendYAxis()    
    def calculate_speed(self):
        if self.last_frame is not None and self.mouse_inside:
            new_frame = get_current_frame()
            speed = new_frame.speed(self.last_frame)
            if speed is not None and speed > 0:
                # print(f"Cursor Speed: {speed} pixels per second")
                # print(f"Cursor Position: ({self.x}, {self.y})")
                self.speed = speed
                self.setSignalPoint(self.speed,self.x)
                self.plotSignal()
            self.last_frame = new_frame

            

            # print("signal points", self.generatedSignal.yAxis)
            
    def initalizeGraph(self):
        self.viewBox.setXRange(0, 0.2)
        self.viewBox.setYRange(-300, 300)
        self.viewBox1.setXRange(0, 0.2)
        self.viewBox1.setYRange(-300, 300)
            
    def plotSignal(self):
        if (self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)] > 0.1999999999999999):
            self.viewBox.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
            self.viewBox1.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
        
        self.inputSignalGraph.clear()
        self.inputSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],self.generatedSignal.yAxis,pen="b")
        filteredSignal = self.filter_real_time_signal(self.generatedSignal.yAxis)
        magnitude = np.abs(filteredSignal)
        self.filteredSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],filteredSignal,pen="r")
        # self.filter_real_time_signal(self.generatedSignal.yAxis)


    def eventFilter(self, source, event):
        if source == self.padWidgetGraph:
            if event.type() == QtCore.QEvent.Enter: 
                # if event.type() == QtCore.QEvent.MouseMove:
                    self.mouse_inside = True
                    self.timer.start(self.timer_interval)
                    self.last_frame = get_current_frame()
            elif event.type() == QtCore.QEvent.Leave:
                self.mouse_inside = False
                self.timer.stop()
            elif event.type() == QtCore.QEvent.MouseMove:
                self.x = event.x()
                self.y = event.y()

                # print(f"Mouse Coordinates:({self.x}, {self.y})")
                # print("Mouse is over the widget and within its boundaries")
        return super().eventFilter(source, event)







def init_connectors(self):
    self.clearAllBtn.clicked.connect(lambda:self.clear())
    self.clearAllPolesBtn.clicked.connect(lambda:self.clearAllPoles())
    self.clearAllZerosBtn.clicked.connect(lambda:self.clearAllZeros())
    self.addButton.clicked.connect(lambda:self.addFilter())
    self.allPassLibrary.itemPressed.connect(lambda: self.plotAllPassResponse(self.allPassLibrary.currentItem().text()))
    self.applyFilter.clicked.connect(lambda: self.applyallPassFilter())
    # self.AllPassLibrary.


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
