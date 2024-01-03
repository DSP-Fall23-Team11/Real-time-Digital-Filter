import numpy as np
import matplotlib.pyplot as plt

# Original signal with zeros and poles
original_signal = [1, 2, 3, 1, 2, 1, 5, 1, 7, 0, 1, 2]

# Parameters for the all-pass filter
a = 0.9  # Adjust the value of 'a' based on your design

# Calculate the transfer function of the all-pass filter
def all_pass_filter(omega, a):
    return (np.exp(-1j * omega) - np.conjugate(a)) / (1 - a * np.exp(-1j * omega))

# Apply the all-pass filter to the signal
omega_values = np.linspace(0, np.pi, len(original_signal))
all_pass_response = all_pass_filter(omega_values, a)

modified_signal = original_signal * np.exp(1j * np.angle(all_pass_response))

# Plot the original and modified signals
plt.figure(figsize=(10, 4))
plt.subplot(2, 1, 1)
plt.plot(omega_values, np.abs(original_signal)+1, label='Original Magnitude')
plt.plot(omega_values, np.abs(modified_signal), label='Modified Magnitude')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(omega_values, np.angle(original_signal), label='Original Phase')
plt.plot(omega_values, np.angle(modified_signal), label='Modified Phase')
plt.xlabel('Frequency')
plt.ylabel('Phase')
plt.legend()

plt.tight_layout()
plt.show()
