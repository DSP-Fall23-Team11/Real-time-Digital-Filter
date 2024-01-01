class Plotting():
    def __init__(self,plotWidget,xmin=0,xmax=1,ymin=0,ymax=1):
        self.plotWidget = plotWidget
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
    

    def setLimits(self):
        self.plotWidget.setXRange(xMin= self.xmin , xMax = self.xmax , yMin = self.ymin , yMax = self.ymax)