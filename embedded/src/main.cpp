#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup(void) {
	Serial.begin(115200);

	// Try to initialize!
	if (!mpu.begin()) {
		Serial.println("Failed to find MPU6050 chip");
		while (1) {
		  delay(10);
		}
	}
	Serial.println("MPU6050 Found!");

	// set accelerometer range to +-8G
	mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

	// set gyro range to +- 500 deg/s
	mpu.setGyroRange(MPU6050_RANGE_500_DEG);

	// set filter bandwidth to 21 Hz
	mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

	delay(100);
}

void loop() {
	/* Get new sensor events with the readings */
	sensors_event_t a, g, temp;
	mpu.getEvent(&a, &g, &temp);

	/* Print out the values */
	Serial.print(">Acceleration X:");
  Serial.println(a.acceleration.x);
  Serial.print(">Acceleration Y:");
  Serial.println(a.acceleration.y);
  Serial.print(">Acceleration Z:");
  Serial.println(a.acceleration.z);

	Serial.print(">Gyroscope X:");
  Serial.println(g.gyro.x);
  Serial.print(">Gyroscope Y:");
  Serial.println(g.gyro.y);
  Serial.print(">Gyroscope Z:");
  Serial.println(g.gyro.z);

	Serial.print(">Temperature:");
  Serial.print(temp.temperature);

	Serial.println("");
	delay(50);
}