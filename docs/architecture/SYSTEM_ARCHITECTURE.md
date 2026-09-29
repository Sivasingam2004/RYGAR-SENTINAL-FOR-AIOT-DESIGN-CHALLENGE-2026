\# RYGAR SENTINAL — System Architecture



\## AIoT Design Challenge 2026



\---



\## 1. System Overview



Rygar Sentinal is a unified edge appliance designed to combine

physical security, environmental sensing, occupancy monitoring,

infrastructure monitoring, local data processing and AI-based anomaly

detection into a single local-first system.



The prototype consists of:



\- Entrance Access Control Node

\- Edge Sensor Node

\- Arduino UNO Q Central Coordinator

\- Raspberry Pi 5 Sentinel Core

\- Local MQTT communication

\- Web dashboard

\- CCTV integration

\- Local AI anomaly detection

\- Secure remote access through Tailscale



\---



\## 2. High-Level Architecture



```text

&#x20;                   RYGAR SENTINAL

&#x20;               UNIFIED EDGE APPLIANCE

&#x20;                        │

&#x20;       ┌────────────────┼────────────────┐

&#x20;       │                │                │

&#x20;       ▼                ▼                ▼



&#x20;┌──────────────┐ ┌──────────────┐ ┌──────────────┐

&#x20;│   Entrance   │ │ Edge Sensor  │ │   CCTV       │

&#x20;│     Node     │ │     Node     │ │    Laptop    │

&#x20;└──────┬───────┘ └──────┬───────┘ └──────┬───────┘

&#x20;       │                 │                │

&#x20;       │ UART            │ UART           │ HTTP/MJPEG

&#x20;       ▼                 ▼                │

&#x20;┌──────────────┐ ┌──────────────┐         │

&#x20;│ Entrance     │ │ Heltec V1    │         │

&#x20;│ ESP32        │ │ Wi-Fi Node   │         │

&#x20;└──────┬───────┘ └──────┬───────┘         │

&#x20;       │                 │                 │

&#x20;       └──────── Wi-Fi ──┤                 │

&#x20;                         ▼                 │

&#x20;                   ┌──────────────┐        │

&#x20;                   │ Arduino      │        │

&#x20;                   │ UNO Q        │        │

&#x20;                   │ Central      │        │

&#x20;                   │ Coordinator  │        │

&#x20;                   └──────┬───────┘        │

&#x20;                          │                │

&#x20;                          │ MQTT           │

&#x20;                          ▼                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │      Raspberry Pi 5       │

&#x20;                   │      Sentinel Core        │

&#x20;                   │                          │

&#x20;                   │  MQTT Broker             │

&#x20;                   │  State Processing        │

&#x20;                   │  Dashboard               │

&#x20;                   │  AI Anomaly Detection    │

&#x20;                   │  Storage                 │

&#x20;                   │  Remote Access           │

&#x20;                   └──────────────────────────┘

