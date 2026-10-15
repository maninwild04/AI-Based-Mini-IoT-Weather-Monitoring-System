# AI-Based Mini IoT Weather Monitoring System

## Project Overview
This project is an AI-based IoT weather monitoring system that collects environmental data using sensors, uploads the readings to ThingSpeak Cloud, and applies machine learning to detect abnormal weather conditions.

The system uses an ESP32 microcontroller, DHT22 temperature and humidity sensor, BMP280 pressure sensor, and Python-based anomaly detection.

## Objectives
- Monitor temperature, humidity, and atmospheric pressure.
- Collect environmental data using ESP32 and sensors.
- Upload sensor readings to ThingSpeak Cloud.
- Detect abnormal readings using machine learning.
- Automatically upload anomaly alerts to the cloud.

## Hardware Requirements
- ESP32 Development Board
- DHT22 Temperature and Humidity Sensor
- BMP280 Pressure Sensor
- Connecting Wires
- USB Cable

## Software and Technologies
- Arduino IDE
- Python
- ThingSpeak Cloud
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Requests Library

## Working Methodology
1. The DHT22 sensor measures temperature and humidity.
2. The BMP280 sensor measures atmospheric pressure.
3. The ESP32 collects sensor readings.
4. The readings are uploaded to ThingSpeak Cloud.
5. Python retrieves the data for analysis.
6. The Isolation Forest algorithm identifies potential anomalies.
7. Anomaly alerts are automatically uploaded to ThingSpeak.

## Machine Learning Algorithm
The project uses the Isolation Forest algorithm, an unsupervised machine learning technique for anomaly detection.

It identifies readings that differ significantly from normal patterns in the collected weather data.

## Cloud Integration
ThingSpeak is used to store and visualize sensor readings and to record anomaly alerts.

## Applications
- IoT-based weather monitoring
- Environmental data analysis
- Smart agriculture
- Remote environmental monitoring
- Abnormal weather data detection

## Future Improvements
- Real-time notification through email or mobile applications
- Improved anomaly detection using additional data
- Weather forecasting using historical data
- Integration with additional environmental sensors

## Conclusion
This project combines IoT, cloud computing, and machine learning to develop a weather monitoring system capable of identifying abnormal sensor readings and automatically uploading alerts.

## Author
B.Tech Electronics and Communication Engineering Student
