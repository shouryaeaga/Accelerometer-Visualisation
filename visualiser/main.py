import argparse
from pyray import *
import serial

ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0

def main():
    parser = argparse.ArgumentParser(description="Python script to visualise incoming serial data about acceleration and rotation")
    parser.add_argument("--port", type=str, required=True, help="Serial port to connect to (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")

    args = parser.parse_args()

    print(f"Connecting to serial port {args.port} at {args.baudrate} baud...")

    ser = serial.Serial(args.port, args.baudrate)

    screen_width = 800
    screen_height = 450
    init_window(screen_width, screen_height, b"Serial Data Visualisation")

    camera = Camera3D()
    camera.position = Vector3(10, 10, 0)
    camera.target = Vector3(0, 0, 0)
    camera.up = Vector3(0, 1, 0)
    camera.fovy = 45.0
    camera.projection = CameraProjection.CAMERA_PERSPECTIVE

    cubeVelocity = Vector3(0, 0, 0)

    cubePosition = Vector3(0, 0, 0)

    set_target_fps(20)

    while not window_should_close():
        # Update
        update_camera(camera, CameraMode.CAMERA_FREE)

        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                data = line.split(',')
                ax = round(float(data[0]), 2)
                ay = round(float(data[1]), 2)
                az = round(float(data[2]), 2)
                gx = round(float(data[3]), 2)
                gy = round(float(data[4]), 2)
                gz = round(float(data[5]), 2)
                # print(f"Acceleration: ax={ax}, ay={ay}, az={az} | Gyroscope: gx={gx}, gy={gy}, gz={gz}")
                # Swap axes y and z due to the coordinate system differences
                temp = ay
                ay = az
                az = temp
            except:
                print(f"Error parsing line: {line}")
                continue
        else:
            ax = ay = az = 0
        

        # Make sure y is negative
        ay = -ay
        ay += 9.79  # Adjust for gravity
        print(f"Adjusted Acceleration: ax={ax}, ay={ay}, az={az}")

        cubeVelocity.x += ax * 0.05
        cubeVelocity.y += ay * 0.05
        cubeVelocity.z += az * 0.05
        
        # print(f"Cube Velocity: {cubeVelocity.x}, {cubeVelocity.y}, {cubeVelocity.z}")

        cubePosition.x += cubeVelocity.x * 0.05
        cubePosition.y += cubeVelocity.y * 0.05
        cubePosition.z += cubeVelocity.z * 0.05

        # Draw
        begin_drawing()
        clear_background(RAYWHITE)
        
        begin_mode_3d(camera)
        draw_cube(cubePosition, 1.0, 1.0, 1.0, RED)
        draw_cube_wires(cubePosition, 1.0, 1.0, 1.0, MAROON)
        draw_grid(10, 1.0)
        end_mode_3d()

        end_drawing()
    
    ser.close()
    close_window()  # Close window and OpenGL context
    
if __name__ == "__main__":
    main()