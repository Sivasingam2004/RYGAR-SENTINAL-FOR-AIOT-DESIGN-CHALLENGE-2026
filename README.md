\# RYGAR SENTINAL



\## Unified Edge Appliance for Secure AIoT Infrastructure Management



\*\*AIoT Design Challenge 2026\*\*



\---



\## Overview



Rygar Sentinal is a local-first Unified Edge Appliance designed to

integrate security, environmental monitoring, occupancy sensing,

infrastructure monitoring, edge computing, AI-based anomaly detection,

CCTV and secure remote access into a unified system.



The prototype connects distributed sensor and access-control nodes to an

Arduino UNO Q central coordinator and a Raspberry Pi 5 Sentinel Core.



The system follows the principle:



> \*\*Connect → Observe → Collect → Correlate → Detect → Explain → Act → Store\*\*



\---



\## System Architecture



```text

&#x20;                        RYGAR SENTINAL

&#x20;                    UNIFIED EDGE APPLIANCE



&#x20;                             │

&#x20;             ┌───────────────┴───────────────┐

&#x20;             │                               │

&#x20;             ▼                               ▼



&#x20;      ENTRANCE NODE                    EDGE SENSOR NODE

&#x20;      Arduino UNO                     Arduino UNO

&#x20;             │                               │

&#x20;             ▼                               ▼

&#x20;        ESP32 Wi-Fi                     Heltec V1

&#x20;             │                               │

&#x20;             └──────────── Wi-Fi ────────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                      ┌─────────────┐

&#x20;                      │  Arduino    │

&#x20;                      │    UNO Q    │

&#x20;                      │    Edge     │

&#x20;                      │ Coordinator │

&#x20;                      └──────┬──────┘

&#x20;                             │

&#x20;                             │ MQTT

&#x20;                             ▼

&#x20;                      ┌─────────────┐

&#x20;                      │ Raspberry   │

&#x20;                      │    Pi 5     │

&#x20;                      │ Sentinel    │

&#x20;                      │    Core     │

&#x20;                      └──────┬──────┘

&#x20;                             │

&#x20;              ┌──────────────┼──────────────┐

&#x20;              │              │              │

&#x20;              ▼              ▼              ▼

&#x20;          Dashboard         AI            CCTV

&#x20;                             │

&#x20;                             ▼

&#x20;                      Anomaly Detection

