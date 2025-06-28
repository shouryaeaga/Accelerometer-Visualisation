# Accelerometer Visualisation

This project reads data from an MPU6050 accelerometer using an ESP32 and sends it over a serial connection. The C++ code (in a PlatformIO project) runs on the ESP32 to stream sensor data.

Python scripts are used to:

- Calibrate the sensor by calculating offsets from serial data
- Visualise the 3D orientation using raylib
- Control the mouse using the sensor's rotation

