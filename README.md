# RadarSensorArduino

## Arduino Radar Data Analyzer

I built this project to take in data from an arduino board, which gets data from a radar sensor and rotates with user input. The arduino board is coded in it's embedded C++ language, the data is parsed through with a simple Python script to a C++ analyzer, which is controlled by a Python application.

## Features
### C++ Programming
A 2D coordinate plane is created by multiplying distance, gained from the sensor, and angle, gained from user input. Input is constantly fed into the Python script which logs it into a .csv, which is then given to the C++ program. The C++ program passes data through a 2D Kalman filter and finds the furthest and closest distances, then logs the distances and time in its own .csv.

### Python Application
This application makes it easier to run and stop the Python/C++ script by incorporating PyQt5's push buttons. There is also a graph segment in order to plot and better visualize the data gained from the sensor. It also plots the max and min values obtained by the C++ program by showing it in different colors.

## Tech Stack
- Arduino C++
- C++ 20
- Python 3
  - PyQt5
  - Matplotlib
  - Pandas
