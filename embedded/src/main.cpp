#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

// calibrated from my sensor, you may need to change these values
const float offset_AX = -0.3327;
const float offset_AY = -0.0045;
const float offset_AZ = 10.9307 - 9.80665;
const float offset_GX = -0.0573;
const float offset_GY = 0.01;
const float offset_GZ = -0.01;

void setup(void)
{
	Serial.begin(115200);
	while (!Serial)
		delay(10); // will pause Zero, Leonardo, etc until serial console opens

	Serial.println("Adafruit MPU6050 test!");

	// Try to initialize!
	if (!mpu.begin())
	{
		Serial.println("Failed to find MPU6050 chip");
		while (1)
		{
			delay(10);
		}
	}
	Serial.println("MPU6050 Found!");

	mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
	Serial.print("Accelerometer range set to: ");
	switch (mpu.getAccelerometerRange())
	{
	case MPU6050_RANGE_2_G:
		Serial.println("+-2G");
		break;
	case MPU6050_RANGE_4_G:
		Serial.println("+-4G");
		break;
	case MPU6050_RANGE_8_G:
		Serial.println("+-8G");
		break;
	case MPU6050_RANGE_16_G:
		Serial.println("+-16G");
		break;
	}
	mpu.setGyroRange(MPU6050_RANGE_500_DEG);
	Serial.print("Gyro range set to: ");
	switch (mpu.getGyroRange())
	{
	case MPU6050_RANGE_250_DEG:
		Serial.println("+- 250 deg/s");
		break;
	case MPU6050_RANGE_500_DEG:
		Serial.println("+- 500 deg/s");
		break;
	case MPU6050_RANGE_1000_DEG:
		Serial.println("+- 1000 deg/s");
		break;
	case MPU6050_RANGE_2000_DEG:
		Serial.println("+- 2000 deg/s");
		break;
	}

	mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
	Serial.print("Filter bandwidth set to: ");
	switch (mpu.getFilterBandwidth())
	{
	case MPU6050_BAND_260_HZ:
		Serial.println("260 Hz");
		break;
	case MPU6050_BAND_184_HZ:
		Serial.println("184 Hz");
		break;
	case MPU6050_BAND_94_HZ:
		Serial.println("94 Hz");
		break;
	case MPU6050_BAND_44_HZ:
		Serial.println("44 Hz");
		break;
	case MPU6050_BAND_21_HZ:
		Serial.println("21 Hz");
		break;
	case MPU6050_BAND_10_HZ:
		Serial.println("10 Hz");
		break;
	case MPU6050_BAND_5_HZ:
		Serial.println("5 Hz");
		break;
	}

	Serial.println("");

	

	delay(100);
}

void loop()
{
	/* Get new sensor events with the readings */
	sensors_event_t a, g, temp;
	mpu.getEvent(&a, &g, &temp);

	// Apply offsets to the sensor data
	a.acceleration.x -= offset_AX;
	a.acceleration.y -= offset_AY;
	a.acceleration.z -= offset_AZ;
	g.gyro.x -= offset_GX;
	g.gyro.y -= offset_GY;
	g.gyro.z -= offset_GZ;

	/* Print out all the values separated by commas for gyro and acceleration */
	Serial.print(a.acceleration.x);
	Serial.print(",");
	Serial.print(a.acceleration.y);
	Serial.print(",");
	Serial.print(a.acceleration.z);
	Serial.print(",");
	Serial.print(g.gyro.x);
	Serial.print(",");
	Serial.print(g.gyro.y);
	Serial.print(",");
	Serial.print(g.gyro.z);
	Serial.print("\n");
	delay(50);
}