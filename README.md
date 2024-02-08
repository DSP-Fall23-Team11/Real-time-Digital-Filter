# Realtime Digital Filter Design Application

## Overview

This desktop application allows users to design custom digital filters by placing zeros and poles on the z-plane. The interactive interface provides real-time visualization of the filter's frequency response and enables users to apply the designed filter to lengthy signals with customizable temporal resolution.

## Live Demo

https://github.com/DSP-Fall23-Team11/DSP-task6/assets/83988379/5e7776e7-e54f-4e7e-ac48-0e33a67497a9

## Features

### Z-Plane Plot

- **Interactive Plotting:** Users can place zeros and poles on the z-plane.
- **Dynamic Modifications:** Zeros/poles can be modified by dragging them.
- **Deletion:** Clicking on a zero or pole allows users to delete it.
- **Clear Options:** Users can clear all zeros, all poles, or clear everything on the plot.
- **Conjugates:** Option to add or remove conjugates for complex elements.

### Frequency Response Plot

- **Magnitude and Phase Response:** Visual representation of the filter's frequency response.
- **Real-time Updates:** The plots update as users modify the filter design.

### Real-time Filtering

- **Lengthy Signal Processing:** Apply the filter to a signal with a minimum of 10,000 points in real-time.
- **Temporal Control:** Adjustable speed/temporal-resolution via a slider.
- **Mouse Input:** Users can input real-time signals by moving the mouse, with the speed affecting signal frequencies.

### Phase Correction with All-Pass Filters

- **All-Pass Filter Library:** Visualize and select from a library of all-pass filters.
- **Custom All-Pass:** Users can create their own all-pass filters by specifying "a," and the website calculates its phase response.
- **Enable/Disable Controls:** Users can toggle the added all-pass elements.

## Examples

Explore the functionality with the provided examples:

- [Pole-Zero Placement](https://www.earlevel.com/main/2013/10/28/pole-zero-placement-v2/)
- [Filter Frequency Response Grapher](https://www.earlevel.com/main/2016/12/08/filter-frequency-response-grapher/)

## Getting Started

To get started with the application, follow these steps:

1. Clone the repository.
2. Open the `index.html` file in your preferred web browser.

## Notes

- Examples are provided for reference, and you are encouraged to implement your own design.
- Consider user-friendliness in your design to ensure ease of use for all users.

Feel free to contribute, report issues, or suggest enhancements. Happy filtering!
