import json
import time
import urllib.request
import paho.mqtt.client as mqtt

# ============================================================
# RYGAR SENTINEL - UNO Q → RASPBERRY PI MQTT BRIDGE
# ============================================================

FLASK_STATE = "http://127.0.0.1:5000/state"

PI_IP = "10.148.119.4"

MQTT_TOPIC = "rygar/state"

client = mqtt.Client(
    client_id="rygar_state_bridge"
)

print("============================================")
print(" RYGAR SENTINEL - MQTT STATE BRIDGE")
print("============================================")
print("Pi MQTT :", PI_IP)
print("Topic   :", MQTT_TOPIC)
print("============================================")


# ------------------------------------------------------------
# CONNECT TO PI MQTT BROKER
# ------------------------------------------------------------

try:

    client.connect(
        PI_IP,
        1883,
        60
    )

    client.loop_start()

    print("MQTT CONNECTED")

except Exception as e:

    print("MQTT CONNECTION FAILED:", e)

    raise SystemExit


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

while True:

    try:

        with urllib.request.urlopen(
            FLASK_STATE,
            timeout=2
        ) as response:

            data = json.loads(
                response.read().decode()
            )

        payload = json.dumps(
            data,
            separators=(",", ":")
        )

        result = client.publish(
            MQTT_TOPIC,
            payload,
            qos=0,
            retain=True
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:

            print("STATE SENT")

        else:

            print(
                "MQTT PUBLISH ERROR:",
                result.rc
            )

    except Exception as e:

        print(
            "STATE ERROR:",
            e
        )

    time.sleep(2)