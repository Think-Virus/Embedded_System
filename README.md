# **NUCLEO-L476RG Sensor Data Monitoring System**

## **📌 Project Overview**
This project utilizes the **NUCLEO-L476RG** board to **collect sensor data** and visualize it in real-time on a **Python-based dashboard**.  
The system is built on **FreeRTOS**, processes sensor data, and transmits it to a PC via **UART**, where it is displayed using a Kivy-based GUI.

### 🚧 **[Ongoing Project]** 🚧  
This project is **still in progress** and is being continuously updated.  
Development is currently happening on the `develop` branch, and it will be merged into `main` once the first phase is completed.  
Some features may be incomplete as development and optimizations are ongoing. 🚀  

---

## **🛠 Hardware Configuration**
- **NUCLEO-L476RG** development board  
- **4 Sensors** (ADC1 - Channels 9, 10, 11, 12)  
- **UART Communication (115200 baud)** - Data transmission between the board and PC  
- **GPIO Control (Button input, LED output)**  
- **DMA** for efficient ADC data processing  

---

## **📂 Project Structure**

### **📌 Firmware (STM32, C - FreeRTOS-based)**
📌 **[Core/Src]**
- **`main.c`**: System initialization and FreeRTOS startup  
- **`freertos.c`**: FreeRTOS task definitions (sensor data processing, UART transmission)  
- **`adc.c`**: ADC1 initialization and DMA integration  
- **`usart.c`**: UART2 communication setup and data transmission (`uart_send_data()`)  
- **`gpio.c`**: Button input and LED output pin configuration  
- **`dma.c`**: DMA setup (transfer ADC data to memory)  
- **`stm32l4xx_it.c`**: Interrupt handlers (DMA, TIM3, etc.)  
- **`stm32l4xx_hal_timebase_tim.c`**: TIM3-based system timer configuration  
- **`stm32l4xx_hal_msp.c`**, **`system_stm32l4xx.c`**: STM32 system and clock configuration  

---

### **📌 Python Dashboard (Kivy-based)**
📌 **[Dashboard Code]**
- **`main.py`**  
  - Kivy-based GUI application  
  - Automatic STM board detection (`get_port()`)  
  - UART data reception and processing (`thread_init()`, `get_sensor_data()`)  
  - Real-time dashboard UI updates (`update_dashboard_ui()`)  
  - Includes login/sign-up features  

- **Kivy KV Files**  
  - **`main.kv`**: Main screen layout  
  - **`dashboardscreen.kv`**: Sensor data display  
  - **`loginscreen.kv`**: Login screen  
  - **`signupscreen.kv`**: Sign-up screen  

---

## **📡 Data Flow**
1. **NUCLEO-L476RG board collects sensor data via ADC**  
2. **Data is transmitted using DMA and processed by FreeRTOS tasks**  
3. **Python dashboard on PC receives data via UART**  
4. **Kivy-based UI visualizes the data in real-time**  

---

## **🚀 How to Run**

### **📌 Running the Firmware (STM32 Board)**
1. Flash the firmware to the board using **STM32CubeIDE**  
2. Connect the **NUCLEO-L476RG board** to the PC via USB  
3. Verify sensor data transmission via **UART (115200 baud)**  

### **📌 Running the Dashboard (PC)**
1. Set up the Python environment and install required packages  
   ```bash
   pip install kivy pyserial
   ```
2. Run the Python GUI  
   ```bash
   python main.py
   ```

---

## **✅ Currently Implemented Features**
✔ **FreeRTOS-based sensor data collection**  
✔ **Efficient ADC processing using DMA**  
✔ **Real-time data transmission via UART**  
✔ **Kivy-based GUI development**  

---

## **📌 TODO (Upcoming Features)**
- ⏳ **Update dashboard UI to reflect sensor data**  
- ⏳ **Implement noise filtering for sensor data**  
- ⏳ **Support additional sensors and extended functionalities**  

---

## **🔀 Branch Management**
- Development is currently being carried out on the `develop` branch.  
  Once the first phase is completed, it will be merged into the `main` branch.
- Major updates will be tested on `develop` before being pushed to `main`.

---

## **📄 License**
This project is distributed under **STMicroelectronics' open-source license**.  
