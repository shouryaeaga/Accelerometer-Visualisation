import argparse
from pyray import *
import serial
from ahrs.filters import Madgwick
import numpy as np
from ahrs.common.orientation import q2euler

ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0


dt = 0.05

madgwick = Madgwick()


def main():
    parser = argparse.ArgumentParser(description="Python script to visualise incoming serial data about acceleration and rotation")
    parser.add_argument("--port", type=str, required=True, help="Serial port to connect to (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")

    args = parser.parse_args()

    print(f"Connecting to serial port {args.port} at {args.baudrate} baud...")

    ser = serial.Serial(args.port, args.baudrate)

    screen_width = 1280
    screen_height = 720
    init_window(screen_width, screen_height, b"Serial Data Visualisation")

    camera = Camera3D()
    camera.position = Vector3(20, 20, 0)
    camera.target = Vector3(0, 0, 0)
    camera.up = Vector3(0, 1, 0)
    camera.fovy = 45.0
    camera.projection = CameraProjection.CAMERA_PERSPECTIVE

    cubeMesh = gen_mesh_cube(1.0, 1.0, 1.0)
    cubeModel = load_model_from_mesh(cubeMesh)
    


    cubePosition = Vector3(0, 0, 0)

    q = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)  # Initial quaternion

    set_target_fps(20)

    while not window_should_close():
        # Update
        update_camera(camera, CameraMode.CAMERA_FREE)

        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                print(f"Received line: {line}")
                data = line.split(',')
                print(f"Parsed data: {data}")
                raw_ax = float(data[0])
                raw_ay = float(data[1])
                raw_az = float(data[2])
                print(f"Raw Data: ax={raw_ax}, ay={raw_ay}, az={raw_az}")
                gx = float(data[3])
                gy = float(data[4])
                gz = float(data[5])
                # print(f"Acceleration: ax={ax}, ay={ay}, az={az} | Gyroscope: gx={gx}, gy={gy}, gz={gz}")
                # Swap axes y and z due to the coordinate system differences

                acc = np.array([raw_ax, raw_ay, raw_az])
                gyro = np.array([gx, gy, gz])

                q = madgwick.updateIMU(q, gyro, acc)

                roll, pitch, yaw = q2euler(q)
                print(f"Orientation: Roll={roll:.2f}, Pitch={pitch:.2f}, Yaw={yaw:.2f}")
            except IndexError or ValueError:
                print(f"Error parsing line: {line}")
                continue
        else:
            ax = ay = az = 0
        
        # Update cube position based on orientation




        
        cubeModel.transform = matrix_rotate_xyz(Vector3(-pitch, -yaw, -roll))

        # Draw
        begin_drawing()
        clear_background(RAYWHITE)
        
        begin_mode_3d(camera)
        draw_model_ex(cubeModel, cubePosition, Vector3(0, 0, 1), 1.0, Vector3(1.0, 1.0, 1.0), RED)
        draw_grid(10, 1.0)
        end_mode_3d()

        end_drawing()
    
    ser.close()
    close_window()  # Close window and OpenGL context
    
if __name__ == "__main__":
    main()