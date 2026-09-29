import json
import os

import joblib
import pandas as pd
import paho.mqtt.client as mqtt


# ============================================================
# RYGAR SENTINEL - LIVE AI ENGINE
# ============================================================

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "rygar/state"


MODEL_DIR = os.path.expanduser(
    "~/rygar-ai/model"
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "isolation_forest.joblib"
)

SCALER_FILE = os.path.join(
    MODEL_DIR,
    "scaler.joblib"
)


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


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    MODEL_FILE
)

scaler = joblib.load(
    SCALER_FILE
)


print("============================================")
print(" RYGAR SENTINEL - LIVE AI ENGINE")
print("============================================")
print("Model loaded")
print("MQTT topic:", TOPIC)
print("============================================")


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_features(data):

    node = data.get("node2", {})

    values = {
        "temperature":
            node.get("temperature"),

        "humidity":
            node.get("humidity"),

        "mq2":
            node.get("mq2"),

        "mq135":
            node.get("mq135"),

        "water":
            node.get("water"),

        "acs":
            node.get("acs"),

        "pir1":
            node.get("pir1"),

        "pir2":
            node.get("pir2"),

        "parking1":
            node.get("parking1"),

        "parking2":
            node.get("parking2"),

        "fire":
            node.get("fire"),

        "buzzer":
            node.get("buzzer"),

        "fan":
            node.get("fan"),

        "light":
            node.get("light")
    }

    return values


# ============================================================
# MQTT
# ============================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("MQTT CONNECTED")

        client.subscribe(TOPIC)

        print(
            "Subscribed:",
            TOPIC
        )

    else:

        print(
            "MQTT CONNECTION FAILED:",
            rc
        )


def on_message(client, userdata, msg):

    try:

        data = json.loads(
            msg.payload.decode()
        )

        values = extract_features(data)


        if any(
            value is None
            for value in values.values()
        ):

            return


        # Create DataFrame with feature names.
        # This avoids the sklearn feature-name warning.

        frame = pd.DataFrame(
            [values],
            columns=FEATURES
        )


        scaled = scaler.transform(
            frame
        )


        prediction = model.predict(
            scaled
        )[0]


        score = model.decision_function(
            scaled
        )[0]


        if prediction == -1:

            print(
                "SENTINEL AI: "
                f"ANOMALY DETECTED "
                f"(score={score:.4f})"
            )

            print(
                "Reason: unusual combination "
                "of sensor readings"
            )

        else:

            print(
                "SENTINEL AI: "
                f"NORMAL "
                f"(score={score:.4f})"
            )


    except Exception as e:

        print(
            "AI ERROR:",
            e
        )


# ============================================================
# START
# ============================================================

client = mqtt.Client(
    client_id="rygar_ai_engine"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

client.loop_forever()