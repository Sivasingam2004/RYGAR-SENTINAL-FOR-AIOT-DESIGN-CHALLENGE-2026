\# Rygar Sentinal — Schematics



This directory contains the electrical schematics used for the Rygar Sentinal

AIoT Design Challenge 2026 prototype.



\## Included Designs



\### 1. Entrance Access Control



The entrance subsystem contains:



\- Arduino UNO R3

\- ESP32-WROOM-32E

\- 4×4 keypad

\- Reed switch / MC-38 door sensor

\- SG90 servo motor

\- Buzzer

\- UART communication between Arduino UNO and ESP32

\- 1kΩ / 2kΩ voltage-divider level shifting for UNO TX → ESP32 RX



\### 2. Edge Sensor Node



The edge sensor subsystem contains:



\- Arduino UNO R3

\- ESP32 / Heltec WiFi LoRa 32 V1

\- MQ-2 gas sensor

\- MQ-135 air-quality sensor

\- DHT11

\- ACS712 current sensor

\- Water sensor

\- PIR sensors

\- Parking IR sensors

\- Flame sensor

\- Buzzer

\- 4-channel relay module

\- 12V DC fan

\- Room-light LEDs



\### 3. Central Edge Controller



The Arduino UNO Q provides:



\- Central node coordination

\- Data aggregation

\- 16×2 I²C LCD interface

\- Communication with the Raspberry Pi Sentinel Core



\## Revision Note



The competition schematic and the final working prototype may contain

component-placement or interface differences.



The final prototype architecture takes the following form:



ESP32 Entrance Node

&#x20;       ↓

&#x20;   Arduino UNO Q

&#x20;       ↑

ESP32 / Heltec Edge Node

&#x20;       ↓

Raspberry Pi 5 Sentinel Core



The final working prototype uses the 16×2 I²C LCD as the common display

connected to the Arduino UNO Q.



\## File Naming



Recommended schematic files:



\- `entrance\_access\_control.pdf`

\- `edge\_sensor\_node.pdf`

\- `system\_architecture.pdf`



Source schematic files should be retained where available.

