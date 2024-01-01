import numpy as np

class Signal:
  def __init__(self):
    self.xAxis = np.linspace(0, 100, 100, endpoint=False)
    self.yAxis = []
    self.amplitude = []
    self.frequency = []
  
  def appendAmplitude(self, amplitude):
    self.amplitude.append(amplitude)

  def appedFrequency(self, frequency):
    self.frequency.append(frequency)

  def appendYAxis(self):
    index = len(self.amplitude)-1
    # print("index: ", index)
    # print("amplitude: ", self.amplitude[index])
    # print("ampLen: ", len(self.amplitude))
    # print("frequency: ", self.frequency[index])
    # print("freqLen: ", len(self.frequency))
    # print("xAxis: ", self.xAxis[index])
    self.yAxis.append(np.cos(2 * np.pi * self.frequency[index] * self.xAxis[index]) * self.amplitude[index])

  
