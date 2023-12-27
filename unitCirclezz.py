import numpy as np
import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

# Create the QApplication instance before creating any widgets
app = QApplication(sys.argv)

image = np.random.normal(size=(500, 400))
plt1 = pg.PlotWidget()
plt1_imageitem = pg.ImageItem(image)
plt1.addItem(plt1_imageitem)
roi_circle = pg.CircleROI([250, 250], [120, 120], pen=pg.mkPen('r', width=2))
plt1.addItem(roi_circle)
plt1.show()

# Start the application event loop
sys.exit(app.exec_())
