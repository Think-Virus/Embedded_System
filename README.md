# 🌱 IoT Dashboard with STM32 & Firebase

A real-time IoT dashboard system that visualizes sensor data collected from an STM32 board via FreeRTOS, integrated with a Python-based GUI and Firebase for user authentication and data synchronization.

---

## ✅ Features

### 🔐 Authentication
- User **Sign Up / Sign In** using **Firebase Authentication**
- Firebase Realtime Database initializes user-specific data upon sign up

### 📊 Dashboard (Python + Kivy)
- **Live Sensor Data Visualization** from STM32 (via USB serial)
- **Temperature / Pressure / Battery** values updated every second
- Visual icons dynamically updated based on value range
- **Switch Control**: Toggle output pins on STM board from dashboard
- **Data Sync with Firebase**: Realtime update to Firebase DB (once per second)

### 🔌 STM32 Board (NUCLEO-L476RG + FreeRTOS)
- 4 potentiometers used as simulated analog sensors
- **FreeRTOS Thread 1**: Read ADC (PA4–PA7), send via UART
- **FreeRTOS Thread 2**: Receive UART commands to control GPIO outputs (PB6, PB7)
- **Push Button** status read from PC13

---

### 📌 STM32 Pin Configuration

The firmware was initialized and configured using **STM32CubeMX**, where the essential pin functions were assigned for sensors, UART communication, button input, and GPIO outputs for actuators.

#### 🧩 Pin Assignments

| Function             | Pin   | Description                         |
|----------------------|--------|-------------------------------------|
| ADC Input - SENSOR1  | PA4    | Potentiometer 1                     |
| ADC Input - SENSOR2  | PA5    | Potentiometer 2                     |
| ADC Input - SENSOR3  | PA6    | Potentiometer 3                     |
| ADC Input - SENSOR4  | PA7    | Potentiometer 4                     |
| UART2 TX             | PA2    | Serial communication to PC          |
| UART2 RX             | PA3    | Serial communication from PC        |
| GPIO Output - LED 1  | PB7    | Controlled by switch from dashboard |
| GPIO Output - LED 2  | PB6    | Controlled by switch from dashboard |
| GPIO Output - LED 3  | PB5    | (Unused in this project)            |
| GPIO Output - LED 4  | PB4    | (Unused in this project)            |
| Button Input         | PC13   | User button                         |

---

#### 🖼️ Pin Mapping Diagram

> This pinout was configured using STM32CubeMX as the initial setup reference:
![image](https://github.com/user-attachments/assets/6baa5edf-c58c-4fb3-bb8e-f9f15a1c5c87)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Kivy (Python GUI) |
| Backend | Firebase (Auth + Realtime Database) |
| Embedded | STM32L476RG + FreeRTOS |
| Communication | UART Serial via USB |
| Sensors | Potentiometers (simulate analog input) |

---

## 🚀 Getting Started

### 🖥️ Python Dashboard
1. Install dependencies:
   ```bash
   pip install kivy requests pyserial
   ```
2. Run the app:
   ```bash
   python main.py
   ```

### 🔧 STM32 Firmware
1. Use STM32CubeMX to generate the base project with:
   - ADC1 (PA4–PA7)
   - UART2 (PA2, PA3)
   - GPIO outputs: PB6, PB7
   - Input: PC13 (button)
   - FreeRTOS with 2 threads + mutex

2. Flash the firmware via STM32CubeIDE.

---

## 📂 Project Structure

```
.
├── main.py                  # Main Python application
├── main.kv                 # Kivy root GUI layout
├── dashboardscreen.kv      # Dashboard UI
├── signinscreen.kv         # Sign-in UI
├── signupscreen.kv         # Sign-up UI
├── freertos.c              # FreeRTOS code for STM32 (C)
├── fonts/                  # fonts for label, text input
└── icons/                  # UI icons for battery, temperature, switches
```

---

## 📝 TODO / Future Improvements

- [ ] **Replace potentiometers** with real sensors (e.g., temperature, humidity)
- [ ] **Firebase to Python** realtime listener for bidirectional sync
- [ ] **Graph Visualization** of sensor data over time
- [ ] **Firebase Database Security Rules** to restrict access per user
- [ ] **Push Button Sync**: Send GPIO input status to Firebase/Python
- [ ] **Modularize Python Code** into MVC or component-based structure

---

### 📸 Demo

#### 1. **📷 Hardware Setup**

> Here's the actual hardware setup using NUCLEO-L476RG board and 4 potentiometers.
![KakaoTalk_20250331_153057022_01](https://github.com/user-attachments/assets/1e621dff-2249-402b-9ddd-f79cd107ec64)

---

#### 2. **🎥 Full System in Action**

> Real-time sensor data collection, dashboard sync, and switch control demonstration:

📺 [Watch Full System Demo](https://1drv.ms/v/c/699aeea76de52c4e/EZp8qDKOB0VFqA4tf8uv-BoBuNwjbmRGses0U4OlfTF3OA?e=ugCv2w)

---

#### 3. **🖥️ Dashboard GUI Only**

> Clean view of Kivy-based dashboard UI:

📺 [Watch GUI Demo](https://1drv.ms/v/c/699aeea76de52c4e/EYIgCt4N3HFNkYgWh006nUoBHKu16AX5AHyZ6bM8jS_wug?e=0nOwKM)

---

## 📜 License  
MIT License  
Feel free to use and modify this project, but be sure to follow personal data protection guidelines and comply with Firebase usage policies.
