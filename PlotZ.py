from numpy import arange, pi, cos, sin, arctan


class plotZ:
    def __init__(self, poles, zeros, scale):
        self.poles = poles
        self.zeros = zeros
        self.scale = scale
    def setData(self, poles ,zeros,scale):
        self.poles = poles
        self.zeros = zeros
        self.scale = scale

    def complex_dist(self, x, y):
        return ((y[1]-x[1])**2 + (y[0]-x[0])**2)**(1/2)
    
    def plot_magnitude_response(self, sensitivity=0.005, color="b"):
        points = []
        for point in arange(0, 1*pi, sensitivity):
            x = cos(point)
            y = sin(point)
            a = 1
            for zero in self.zeros:
                a *= self.complex_dist(zero, [x, y])
            for pole in self.poles:
                temp = self.complex_dist(pole, [x, y])
                if temp!=0: a /= temp
                else: a /= 1e-400
            points.append(a)
        return [arange(0, 1*pi, sensitivity), points]
    def phase_amount(self, x, y):
        range_x = x[0] - y[0]
        range_y = x[1] - y[1]
        return arctan(range_y/range_x)
    def plot_phase_response(self, sensitivity=0.005, color="r"):
        points = []
        for point in arange(0, 1*pi, sensitivity):
            x = cos(point)
            y = sin(point)
            a = 0
            for zero in self.zeros:
                a += self.phase_amount(zero, [x, y])
            for pole in self.poles:
                a -= self.phase_amount(pole, [x, y])
            points.append(a)
        return [arange(0, 1*pi, sensitivity), points]
