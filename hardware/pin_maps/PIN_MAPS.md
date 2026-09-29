\# RYGAR SENTINAL — Pin Maps



\## 1. Entrance Access Control



\### Arduino UNO R3



| Arduino Pin | Connected Component | Function |

|---|---|---|

| D2 | 4×4 Keypad R1 | Keypad Row 1 |

| D3 | 4×4 Keypad R2 | Keypad Row 2 |

| D4 | 4×4 Keypad R3 | Keypad Row 3 |

| D5 | 4×4 Keypad R4 | Keypad Row 4 |

| D6 | SG90 Servo | Door Lock Control |

| D7 | 4×4 Keypad C1 | Keypad Column 1 |

| D8 | 4×4 Keypad C2 | Keypad Column 2 |

| D9 | 4×4 Keypad C3 | Keypad Column 3 |

| D10 | 4×4 Keypad C4 | Keypad Column 4 |

| D11 | MC-38 Reed Switch | Door State Detection |

| D12 | Buzzer | Access Alarm |

| D1 / TX | ESP32 RX | UART Data to ESP32 |

| D0 / RX | ESP32 TX | UART Return Path |

| 5V | Servo / logic supply | +5V |

| GND | Common Ground | Ground |



\### UART Level Shifter



The Arduino UNO operates at 5V logic while the ESP32 uses 3.3V logic.



The UNO TX line uses a resistor divider:



```text

Arduino UNO D1/TX

&#x20;      |

&#x20;     1kΩ

&#x20;      |

&#x20;      +---------- ESP32 RX

&#x20;      |

&#x20;     2kΩ

&#x20;      |

&#x20;     GND

