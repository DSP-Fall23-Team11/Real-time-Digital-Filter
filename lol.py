import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Zeros specified as an array
zeros = np.array([1, 2, -1 + 1j, -1 - 1j])

# Poles (for illustration purposes)
poles = [0, -1]  # Replace with your specific poles

# Create the transfer function
numerator, denominator = signal.zpk2tf(zeros, poles, 1.0)

# Create the filter
sys = signal.TransferFunction(numerator, denominator)

# Generate a sample input signal
time = np.linspace(0, 1, 1000, endpoint=False)
input_signal = np.sin(2 * np.pi * 5 * time) + 0.5 * np.random.normal(size=len(time))

# Apply the filter to the input signal
output_signal = signal.lfilter(numerator, denominator, input_signal)

# Plot the original and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, input_signal, label='Original Signal')
plt.title('Original Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, output_signal, label='Filtered Signal')
plt.title('Filtered Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
