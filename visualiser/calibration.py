import argparse
from pyray import *
import serial

ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0
axValues = []
ayValues = []
azValues = []
gxValues = []
gyValues = []
gzValues = []
def calc_mean(values):
    return sum(values) / len(values) if values else 0


def main():
    samples = 0

    parser = argparse.ArgumentParser(description="Python script to visualise incoming serial data about acceleration and rotation")
    parser.add_argument("--port", type=str, required=True, help="Serial port to connect to (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")

    args = parser.parse_args()

    print(f"Connecting to serial port {args.port} at {args.baudrate} baud...")

    ser = serial.Serial(args.port, args.baudrate)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            data = line.split(',')
            ax = float(data[0])
            ay = float(data[1])
            az = float(data[2])
            gx = float(data[3])
            gy = float(data[4])
            gz = float(data[5])
            print(f"Acceleration: ({ax}, {ay}, {az}), Gyroscope: ({gx}, {gy}, {gz})")
            axValues.append(ax)
            ayValues.append(ay)
            azValues.append(az)
            gxValues.append(gx)
            gyValues.append(gy)
            gzValues.append(gz)
            samples += 1

        if is_key_pressed(KEY_ESCAPE):
            print("Exiting...")
            break

        if samples == 100:
            break
    
    print("Calculating means...")
    ax_mean = calc_mean(axValues)
    ay_mean = calc_mean(ayValues)
    az_mean = calc_mean(azValues)
    gx_mean = calc_mean(gxValues)
    gy_mean = calc_mean(gyValues)
    gz_mean = calc_mean(gzValues)
    print(f"Mean Acceleration: ({ax_mean}, {ay_mean}, {az_mean}), Mean Gyroscope: ({gx_mean}, {gy_mean}, {gz_mean})")

    ser.close()
    
if __name__ == "__main__":
    main()