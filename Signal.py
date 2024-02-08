import numpy as np

class Signal:
  def __init__(self):
    self.xAxis = np.arange(0, 10, 0.001)
    self.yAxis = []
    self.amplitude = []
    self.frequency = []
  
  def appendAmplitude(self, amplitude):
    self.amplitude.append(amplitude)

  def appedFrequency(self, frequency):
    self.frequency.append(frequency)

  def appendYAxis(self):
    index = len(self.amplitude)-1
    print("cos: ", np.cos(2 * np.pi * self.frequency[index] * self.xAxis[index]))
    print("amp: ", self.amplitude[index])

    
    
    self.yAxis.append(np.cos(self.frequency[index] * self.xAxis[index]) * self.amplitude[index])

  
