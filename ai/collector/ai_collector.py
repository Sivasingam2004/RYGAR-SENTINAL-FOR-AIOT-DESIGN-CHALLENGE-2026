import csv
import json
import os

import paho.mqtt.client as mqtt

# ============================================================
# RYGAR SENTINEL - AI DATA COLLECTOR
# ============================================================

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "rygar/state"

OUTPUT_FILE = os.path.expanduser(
    "~/rygar-ai/normal_data.csv"
)

MAX_SAMPLES = 100


FEATURES = [
    "temperature",
    "humidity",
    "mq2",
    "mq135",
    "water",
    "acs",
    "pir1",
    "pir2",
    "parking1",
    "parking2",
    "fire",
    "buzzer",
    "fan",
    "light"
]

samples = []


# ============================================================
# MQTT
# ============================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("MQTT CONNECTED")

        client.subscribe(TOPIC)

        print("Subscribed:", TOPIC)

    else:

        print("MQTT CONNECTION FAILED:", rc)


def extract_features(data):

    node = data.get("node2", {})

    return [
        node.get("temperature"),
        node.get("humidity"),
        node.get("mq2"),
        node.get("mq135"),
        node.get("water"),
        node.get("acs"),
        node.get("pir1"),
        node.get("pir2"),
        node.get("parking1"),
        node.get("parking2"),
        node.get("fire"),
        node.get("buzzer"),
        node.get("fan"),
        node.get("light")
    ]


def on_message(client, userdata, msg):

    global samples

    try:

        data = json.loads(
            msg.payload.decode()
        )

        values = extract_features(data)

        if any(value is None for value in values):
            return

        samples.append(values)

        print(
            f"AI DATA: {len(samples)} samples collected"
        )

        if len(samples) >= MAX_SAMPLES:

            os.makedirs(
                os.path.dirname(OUTPUT_FILE),
                exist_ok=True
            )

            with open(
                OUTPUT_FILE,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow(FEATURES)

                writer.writerows(samples)

            print()
            print(
                "AI DATA COLLECTION COMPLETE"
            )

            print(
                "Saved:",
                OUTPUT_FILE
            )

            client.disconnect()


# ============================================================
# START
# ============================================================

client = mqtt.Client(
    client_id="rygar_ai_collector"
)

client.on_connect = on_connect
client.on_message = on_message

print("============================================")
print(" RYGAR SENTINEL - AI DATA COLLECTOR")
print("============================================")

client.connect(
    BROKER,
    PORT,
    60
)

client.loop_forever()