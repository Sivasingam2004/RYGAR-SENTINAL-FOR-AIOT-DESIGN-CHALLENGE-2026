\# RYGAR SENTINAL

\## Unified Edge Appliance for Secure AIoT Infrastructure Management



\### AIoT Design Challenge 2026



\---



\## 1. Project Overview



Rygar Sentinal is a local-first Unified Edge Appliance designed to

integrate security, environmental monitoring, occupancy sensing,

infrastructure monitoring, local data processing, AI-based anomaly

detection and remote visualization into a unified system.



Instead of treating every sensor, security system and monitoring

application as an isolated subsystem, Rygar Sentinal brings their

data together at the edge.



The prototype demonstrates this concept using an entrance access

control node, an edge sensor node, an Arduino UNO Q coordinator and a

Raspberry Pi 5 Sentinel Core.



\---



\## 2. Problem Statement



Modern small offices and facilities can contain multiple independent

systems:



\- Access control

\- Security sensors

\- Environmental sensors

\- Occupancy monitoring

\- Parking monitoring

\- Electrical/load monitoring

\- CCTV

\- Data storage

\- Remote-access systems



These systems can become fragmented when each subsystem operates

independently.



Rygar Sentinal addresses this fragmentation by creating a unified

edge layer capable of collecting and correlating information from

different subsystems.



\---



\## 3. Proposed Solution



Rygar Sentinal provides a centralized local architecture consisting

of:



\- Distributed sensing nodes

\- Wireless communication

\- Central edge coordination

\- Local MQTT messaging

\- Raspberry Pi computing

\- Web-based monitoring

\- CCTV integration

\- Local AI anomaly detection

\- Secure remote access

\- Local safety responses



The system is designed to continue providing core local functions

without requiring cloud processing for every event.



\---



\## 4. Prototype Architecture



```text

&#x20;                 RYGAR SENTINAL

&#x20;             UNIFIED EDGE APPLIANCE



&#x20;                        │

&#x20;         ┌──────────────┴──────────────┐

&#x20;         │                             │

&#x20;         ▼                             ▼



&#x20;  ENTRANCE NODE                 EDGE SENSOR NODE

&#x20;  Arduino UNO                  Arduino UNO + Sensors

&#x20;         │                             │

&#x20;         ▼                             ▼

&#x20;     ESP32                         Heltec V1

&#x20;         │                             │

&#x20;         └──────────────┬──────────────┘

&#x20;                        │

&#x20;                        │ Wi-Fi

&#x20;                        ▼

&#x20;                 Arduino UNO Q

&#x20;                 Central Edge

&#x20;                 Coordinator

&#x20;                        │

&#x20;                        │ MQTT

&#x20;                        ▼

&#x20;                Raspberry Pi 5

&#x20;                Sentinel Core

&#x20;                        │

&#x20;         ┌──────────────┼──────────────┐

&#x20;         │              │              │

&#x20;         ▼              ▼              ▼

&#x20;     Dashboard          AI            CCTV

&#x20;                        │

&#x20;                        ▼

&#x20;                 Anomaly Detection

