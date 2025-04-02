# Intelligent Fleet Management System 🚛

![Fleet Monitoring Dashboard](https://github.com/user-attachments/assets/160482cd-83f6-4719-b1a5-b3079e1acf57)

## Overview
This project is designed to improve fleet management by monitoring delivery vehicles in real-time using IoT sensors, cloud computing, and a web-based dashboard. The system detects unsafe driving behaviors, tracks vehicle performance, and sends alerts to fleet managers for better decision-making.

## 🚀 Key Features
- **Real-Time Monitoring:** Tracks unsafe driving events like harsh braking, sharp turns, and rapid acceleration.
- **Violation Trends:** Analyzes unsafe driving patterns over time with visualized data.
- **Alerts & Notifications:** Sends real-time alerts for risky driving behavior.
- **Reports & Export:** Allows filtering data by driver/date and exporting reports in CSV/PDF format.


## 🛠 System Components & Technologies
| Component | Purpose |
|-----------|---------|
| **ESP32 / Raspberry Pi Pico** | Microcontroller for data processing & communication |
| **MPU6050 (Accelerometer & Gyro)** | Detects harsh braking, acceleration, and sharp turns |
| **Cloud Database (Firebase / Google sheets)** | Stores real-time data from vehicles |
| **Web Dashboard (Streamlit / Flask )** | Displays unsafe driving events, violations, and reports |

## 📊 Fleet Monitoring Dashboard
The web-based dashboard provides real-time insights into fleet operations, allowing managers to make data-driven decisions. Key dashboard functionalities:
- **Live Driver Monitoring** – Displays unsafe driving actions in real-time.
- **Violation Trends Over Time** – Graphs & charts for analyzing unsafe driving behavior.
- **Alerts & Notifications** – Sends alerts if violations exceed a set threshold.
- **Filtering & Reports** – Allows date-wise and driver-wise filtering & report export (PDF/CSV).

### 🔗 Dashboard Access
🌐 **[Fleet Monitoring Dashboard](https://fleet-manager.streamlit.app/)**
- **Username:** `admin`
- **Password:** `fleet`

### Wokwi Simulation
🌐 **[Wokwi Simulator for hardware ](https://wokwi.com/projects/425977014448937985)**


## 🖥 Tech Stack
- **Hardware:** ESP32 / Raspberry Pi Pico, MPU6050 (Accelerometer & Gyro)
- **Software & Cloud:** MicroPython, Python (Flask/Streamlit), Google Sheets (Data Storage)

## 🛠 How It Works
1. **Each Delivery vehicle has ESP32 microcontroller which is running micropython code, collects sensor data** from MPU6050.
2. **Based on Threshold values of coordinates from MPU6050 sensor**, It detects the driving violation activity.
3. **Unsafe driving events** (harsh braking, acceleration) trigger alerting mechanism (buzzer/LED/OLED Screen).
4. **Data is sent to the cloud** (Firebase/Google sheets) for storage & real-time updates.
5. **Fleet managers view reports** on the web dashboard.

## 📌 Expected Impact
✅ **Reduced accidents** due to real-time unsafe driving detection.  
✅ **Better operational efficiency** for fleet managers.  


## 📫 Contact & Contributions
Want to contribute or have suggestions? Feel free to create a pull request or reach out! 🚀
