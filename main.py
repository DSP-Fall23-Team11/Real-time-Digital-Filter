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
from AllPass import *
import pyqtgraph as pg
import numpy as np
from speed import *
from PlotZ import plotZ
from scipy.signal import zpk2tf, lfilter,freqz_zpk
import csv
import numpy as np
from scipy import signal
from Signal import Signal
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        uic.loadUi('UI/mainwindow.ui', self)
        self.apply_stylesheet("ManjaroMix.qss")
        # self.showMaximized()
        self.allPassFilters = []
        init_connectors(self)
        self.initalize()
        self.ZPlotter = plotZ(self.poles ,self.zeros, self.scale) 
        self.plot()
        #################################################
        self.setMouseTracking(True)
        self.padWidgetGraph.setMouseTracking(True)
        self.padWidgetGraph.installEventFilter(self)
       # self.importButton.hide()
        self.last_frame = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.calculate_speed)
        self.timer_interval = 50  # Set an initial interval in milliseconds (e.g., 100ms)
        self.mouse_inside = False
        self.modifiedSignal=[]
        self.listofCheckedFilters=[]
        self.allPassComboBox.setEditable(True)
        
        self.x = 0
        self.y = 0
        self.speed = 0
        self.zeroA= []
        self.poleA= []
        self.viewBox =self.inputSignalGraph.getViewBox()
        self.viewBox1 =self.filteredSignalGraph.getViewBox()
        self.initalizeGraph()

        self.generatedSignal = Signal()

        self.initalizeAllPassLibrary()
        ###################
        self.pauseFlag1 = False
        self.xAxis = [0]
        self.yAxis = [0]
        
   


    def browseFile(self):
        self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls)" )
        if self.fileName[0]:  
                    self.openFile(self.fileName[0])
                   
    def openFile(self, path:str):
                self.inputSignalGraph.clear()
                timeArr, amplitudeArr = [],[]
                length = len(path)
                fileExtentsion = path[length-3:]
                if fileExtentsion == "csv" or fileExtentsion == "txt" or fileExtentsion == "xls":
                    with open(path, 'r') as file:
                        csv_data = csv.reader(file, delimiter=',')
                        for row in csv_data:
                            timeArr.append(float(row[0]))
                            amplitudeArr.append(float(row[1]))
                self.signalInitialization(self.inputSignalGraph,timeArr,amplitudeArr)            
    def signalInitialization(self,choosenGraph,timeArr, amplitudeArr):       
            self.graph = choosenGraph.plot(
                    name="Channel "+str(1))
            choosenGraph.showGrid(x= True, y= True)
            maxTime,minTime,maxAmp,minAmp = 0,0,0,0
            if len(timeArr):
                if len(timeArr)> maxTime:
                    maxTime = len(timeArr)
            if len(timeArr):
                if len(timeArr )< minTime:
                    minTime = len(timeArr)
            if len(amplitudeArr):
                if max(amplitudeArr ) > maxAmp:
                    maxAmp = max(amplitudeArr)           
            if len(amplitudeArr):
                if min(amplitudeArr ) < minAmp:
                    minAmp = min(amplitudeArr)           
        
            choosenGraph.plotItem.setLimits(
             xMin=minTime, xMax=maxTime, yMin=minAmp, yMax=maxAmp+0.2     
            )
            choosenGraph.setYRange(minAmp,maxAmp)
            self.pauseFlag1 = False
            self.pointsPlotted1 = 0
            self.startTime1 = QtCore.QTimer()
            self.startTime1.setInterval(90)
            self.startTime1.timeout.connect(lambda:self.signalPlotting(choosenGraph,timeArr,amplitudeArr))
            self.startTime1.start()      

    def  signalPlotting(self,choosenGraph,timeArr,amplitudeArr):
           if len(amplitudeArr)>0:
                self.xAxis[0] = timeArr[:self.pointsPlotted1]
                self.yAxis[0] = amplitudeArr[:self.pointsPlotted1]
           self.pointsPlotted1 += 5
           if(len(self.xAxis[0]) >10 ):
                choosenGraph.setXRange(self.xAxis[0][-1]-0.1,self.xAxis[0][-1])
                self.filteredSignalGraph.setXRange(self.xAxis[0][-1]-0.1,self.xAxis[0][-1])
           if len(amplitudeArr)>0:
                if len(timeArr) > self.pointsPlotted1:
                    self.graph.setData(self.xAxis[0], self.yAxis[0]) 
           self.plotSignal(False)         
     
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
  #TODO Ref
    

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

    def initalizeAllPassLibrary(self):
        self.allPassLib.setColumnCount(2)
        self.allPassLib.setHorizontalHeaderLabels(["Filter", "Apply"])
        self.allPassLib.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.allPassLib.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.allPassLib.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.allPassLib.setAlternatingRowColors(True)
        self.allPassLib.setShowGrid(False)
        defaultAllPassLib = ["-0.9", "-0.2", "0.9", "-0.9+2j"]
        self.allPassFilters = []  # Initialize the list
        self.allPassLib.setRowCount(len(defaultAllPassLib)) 
        for index, a in enumerate(defaultAllPassLib):
            filter_value = complex(a)
            item = QTableWidgetItem(str(filter_value))
            self.allPassFilters.append(str(filter_value)) 
            self.allPassLib.setItem(index, 0, item)
        for i in range(self.allPassLib.rowCount()):
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(lambda state, i=i: self.applyCheckedFilters(i,state))
            layout = QHBoxLayout()
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            self.allPassLib.setCellWidget(i, 1, widget)
   


    def filterLib(self, text):
        if self.allPassComboBox.findText(text) == -1:
            self.allPassComboBox.addItem(text)
            filter_value = complex(text)
            self.allPassFilters.append(str(filter_value))
            row = self.allPassLib.rowCount()
            self.allPassLib.insertRow(row)
            item = QTableWidgetItem(str(filter_value))
            self.allPassLib.setItem(row, 0, item)
            # print("CHIPPI CHIPPI CHAPPA CHAPPA", self.allPassFilters)
        for i in range(self.allPassLib.rowCount()):
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            layout = QHBoxLayout()
            checkbox.stateChanged.connect(lambda state, i=i: self.applyCheckedFilters(i,state))
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            self.allPassLib.setCellWidget(i, 1, widget)
            
    def applyCheckedFilters(self, row, state):
        if state == QtCore.Qt.Checked:
            self.listofCheckedFilters.append(complex(self.allPassLib.item(row, 0).text()))     
        else:
            self.listofCheckedFilters.remove(complex(self.allPassLib.item(row, 0).text()))
        print(self.listofCheckedFilters)

    def filter_real_time_signal(self, input_signal,zeros=None,poles=None):
        print(zeros , "before")
        zeros = [complex(x[0], x[1]) for x in zeros]
        poles = [complex(x[0], x[1]) for x in poles]
        print(zeros,"after")
        # Transfer Function
        numerator, denominator = signal.zpk2tf(zeros, poles, 1)
        filtered_audio = signal.lfilter(numerator, denominator, input_signal)
        return filtered_audio

    def filter_order(self,zeros, poles):
        numerator_order = len(zeros)
        denominator_order = len(poles)
        
        return max(numerator_order, denominator_order)

    def plotSignal(self,isPad=True):
        if (self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)] > 0.1999999999999999) and isPad == True:
            self.viewBox.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
            self.viewBox1.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
        if (isPad == True):
            self.inputSignalGraph.clear()
            real_values_list = [x.real if isinstance(x, complex) else x for x in self.generatedSignal.yAxis]
            self.inputSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],real_values_list,pen="b")
        self.zeroA = self.zeros
        self.poleA = self.poles
        if(isPad == True):
              filterOrder = self.filter_order(self.zeroA,self.poleA)
              if(len(self.generatedSignal.yAxis)<=filterOrder):
                       filteredSignal = self.filter_real_time_signal(self.generatedSignal.yAxis,self.zeroA,self.poleA)
                       self.RealTimePts = filteredSignal
                       self.filteredSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],filteredSignal.real,pen="r")
              else:
                       tmpPoints = self.filter_real_time_signal(self.generatedSignal.yAxis[len(self.generatedSignal.yAxis)-filterOrder:],self.zeroA,self.poleA) 
                       tmpData = self.generatedSignal.yAxis
                       tmpData[len(self.generatedSignal.yAxis)-filterOrder:] = tmpPoints         
                       real_values_list = [x.real if isinstance(x, complex) else x for x in tmpData]
                       self.generatedSignal.yAxis = real_values_list
                       self.filteredSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],real_values_list,pen="r")
        elif(len(self.yAxis[0])>10):
              filteredSignal = self.filter_real_time_signal(self.yAxis[0],self.zeroA,self.poleA)    
              self.filteredSignalGraph.plot(self.xAxis[0],filteredSignal.real,pen="r")    
              
    
    def plotSelectedResponse(self,text):
        self.allPassResponse.clear()
        a_coeff = complex(text)
        yAxis = []
        xAxis = np.linspace(0, np.pi, 1000)

        for xValue in xAxis:
            Hap = (np.exp(-1j * xValue) - np.conjugate(a_coeff)) / (1 - a_coeff * np.exp(-1j * xValue))
            yAxis.append(np.angle(Hap))

        self.allPassResponse.plot(xAxis, yAxis, pen="b")

    def plotAllPassResponse(self):
        listofFilters = self.listofCheckedFilters
        zeros = [complex(z[0], z[1]) for z in self.zeros]
        poles = [complex(p[0], p[1]) for p in self.poles]
        for idx, a in enumerate(listofFilters):
            zeroF = 1/np.conj(a)
            poleF = a
            zeros.append(zeroF)
            poles.append(poleF)
        self.zeroA= zeros
        self.poleA= poles
        w,response = freqz_zpk(zeros,poles,1)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        widgets =  [ self.phaseGraphWidget]
        data = [phase]
        titles = [ "Phase Response"]
        for index ,widget in enumerate(widgets):
            widget.canvas.axes.clear()
            widget.canvas.axes.plot(w , data[index] , color ="b")
            widget.canvas.axes.set_title(titles[index])    
            widget.canvas.draw()


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
                self.speed = speed
                self.setSignalPoint(self.speed,self.x)
                self.plotSignal()
            self.last_frame = new_frame
            

            
    def initalizeGraph(self):
        self.viewBox.setXRange(0, 0.2)
        self.viewBox.setYRange(-300, 300)
        self.viewBox1.setXRange(0, 0.2)
        self.viewBox1.setYRange(-300, 300)
        self.filteredSignalGraph.enableAutoRange(axis = self.viewBox1.YAxis)

    


    def plotSignal(self,isPad=True):
        if (self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)] > 0.1999999999999999) and isPad == True:
            self.viewBox.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
            self.viewBox1.setXRange(self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)]-.199999999999, self.generatedSignal.xAxis[len(self.generatedSignal.yAxis)])
        if (isPad == True):
            self.inputSignalGraph.clear()
            self.inputSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],self.generatedSignal.yAxis,pen="b")
        self.zeroA = self.zeros
        self.poleA = self.poles
        if(isPad == True):
              filteredSignal = self.filter_real_time_signal(self.generatedSignal.yAxis,self.zeroA,self.poleA)
              self.filteredSignalGraph.plot(self.generatedSignal.xAxis[0:len(self.generatedSignal.yAxis)],filteredSignal.real,pen="r")
        elif(len(self.yAxis[0])>10):
              filteredSignal = self.filter_real_time_signal(self.yAxis[0],self.zeroA,self.poleA)    
              self.filteredSignalGraph.plot(self.xAxis[0],filteredSignal.real,pen="r")

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
        return super().eventFilter(source, event)



def init_connectors(self):
    self.clearAllBtn.clicked.connect(lambda:self.clear())
    self.clearAllPolesBtn.clicked.connect(lambda:self.clearAllPoles())
    self.clearAllZerosBtn.clicked.connect(lambda:self.clearAllZeros())
    self.addButton.clicked.connect(lambda:self.filterLib(self.allPassComboBox.currentText()) )
    self.allPassLib.itemPressed.connect(lambda: self.plotSelectedResponse(self.allPassLib.currentItem().text()))
    self.allPassLib.itemPressed.connect(lambda: self.allPassLib.currentItem().text())    
    self.applyFilter.clicked.connect(lambda: self.plotAllPassResponse())
    self.importButton.clicked.connect(lambda: self.browseFile())

   

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
